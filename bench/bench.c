// bench.c — speed and memory of one GGUF model through llama.cpp, the way an
// app uses it: one conversation, everything offloaded to Metal.
//
//   bench <model.gguf> [n_ctx=4096] [n_prompt=512] [n_gen=256] [reps=3] [sustain_s=0]
//
// Prints one JSON object. Prompt speed is the time to read n_prompt tokens of
// English text in batches of 512; generation speed is n_gen tokens decoded one
// at a time with greedy sampling. Each repetition starts from an empty context.
// With sustain_s > 0 it then generates continuously for that many seconds and
// reports the rate in 15-second windows, which is what shows thermal throttling.
#include <llama/llama.h>
#include <libproc.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <unistd.h>

static const char *PASSAGE =
    "The lighthouse keeper had lived on the island for thirty years, and in that time he had "
    "learned to read the weather the way other people read a newspaper. A band of pale green "
    "along the horizon at dusk meant wind from the north by morning. Gulls walking on the rocks "
    "instead of flying meant rain. He kept a notebook in which he wrote down the temperature, the "
    "pressure and the direction of the swell twice a day, and when the supply boat came once a "
    "month he sent the pages to the mainland, where somebody he had never met typed them into a "
    "computer. He did not know what the numbers were used for. He liked to imagine a room full of "
    "maps with pins in them. In winter the boat sometimes could not land for six weeks, and then "
    "he ate from tins, repaired the generator with parts he had saved, and repainted the stairs. "
    "There were one hundred and twelve steps to the lamp room and he knew the sound of each one. ";

static double now_s(void) { return (double)llama_time_us() / 1e6; }

static uint64_t footprint(int peak) {
    struct rusage_info_v4 ri;
    if (proc_pid_rusage(getpid(), RUSAGE_INFO_V4, (rusage_info_t *)&ri) != 0) return 0;
    return peak ? ri.ri_lifetime_max_phys_footprint : ri.ri_phys_footprint;
}

// Resident memory at its highest, mapped weights included: what the model
// actually occupies in RAM while it runs. (The footprint leaves the weights
// out, because they are file-backed pages the system could drop.)
static double max_rss(void) {
    struct rusage ru;
    getrusage(RUSAGE_SELF, &ru);
    return (double)ru.ru_maxrss;  // bytes on macOS
}

static void quiet(enum ggml_log_level level, const char *text, void *user) {
    (void)user;
    if (level == GGML_LOG_LEVEL_ERROR) fputs(text, stderr);
}

static int decode(struct llama_context *ctx, llama_token *tokens, int n, int n_batch) {
    for (int i = 0; i < n; i += n_batch) {
        int m = n - i < n_batch ? n - i : n_batch;
        if (llama_decode(ctx, llama_batch_get_one(tokens + i, m)) != 0) return -1;
    }
    return 0;
}

static void stats(const double *v, int n, double *mean, double *sd) {
    double s = 0, q = 0;
    for (int i = 0; i < n; i++) s += v[i];
    *mean = s / n;
    for (int i = 0; i < n; i++) q += (v[i] - *mean) * (v[i] - *mean);
    *sd = n > 1 ? sqrt(q / (n - 1)) : 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: bench model.gguf [n_ctx] [n_prompt] [n_gen] [reps] [sustain_s]\n"); return 2; }
    const char *path = argv[1];
    int n_ctx = argc > 2 ? atoi(argv[2]) : 4096;
    int n_prompt = argc > 3 ? atoi(argv[3]) : 512;
    int n_gen = argc > 4 ? atoi(argv[4]) : 256;
    int reps = argc > 5 ? atoi(argv[5]) : 3;
    int sustain_s = argc > 6 ? atoi(argv[6]) : 0;
    const int n_batch = 512;
    if (reps < 1 || reps > 16 || n_prompt + n_gen + 8 > n_ctx) { fprintf(stderr, "bad arguments\n"); return 2; }

    llama_log_set(quiet, NULL);
    llama_backend_init();

    struct llama_model_params mp = llama_model_default_params();
    mp.n_gpu_layers = 999;
    double t0 = now_s();
    struct llama_model *model = llama_model_load_from_file(path, mp);
    if (!model) { fprintf(stderr, "could not load %s\n", path); return 1; }

    struct llama_context_params cp = llama_context_default_params();
    cp.n_ctx = (uint32_t)n_ctx;
    cp.n_batch = n_batch;
    cp.n_ubatch = n_batch;
    cp.no_perf = true;
    struct llama_context *ctx = llama_init_from_model(model, cp);
    if (!ctx) { fprintf(stderr, "could not create a context of %d tokens\n", n_ctx); return 1; }
    double load_s = now_s() - t0;

    const struct llama_vocab *vocab = llama_model_get_vocab(model);
    // Enough text for the longest prompt asked for.
    size_t len = strlen(PASSAGE), copies = (size_t)n_prompt / 150 + 2;
    char *text = malloc(len * copies + 1);
    text[0] = 0;
    for (size_t i = 0; i < copies; i++) strcat(text, PASSAGE);
    int cap = (int)(len * copies) + 16;
    llama_token *prompt = malloc(sizeof(llama_token) * cap);
    int n_tok = llama_tokenize(vocab, text, (int32_t)strlen(text), prompt, cap, true, false);
    if (n_tok < n_prompt) { fprintf(stderr, "passage gave %d tokens, need %d\n", n_tok, n_prompt); return 1; }

    struct llama_sampler *smpl = llama_sampler_chain_init(llama_sampler_chain_default_params());
    llama_sampler_chain_add(smpl, llama_sampler_init_greedy());

    // Warm-up: the first Metal pass compiles pipelines and faults the weights in.
    if (decode(ctx, prompt, 64, n_batch) != 0) { fprintf(stderr, "decode failed\n"); return 1; }
    llama_token tok = llama_sampler_sample(smpl, ctx, -1);
    for (int i = 0; i < 8; i++) {
        if (llama_vocab_is_eog(vocab, tok)) tok = prompt[1];
        if (llama_decode(ctx, llama_batch_get_one(&tok, 1)) != 0) return 1;
        tok = llama_sampler_sample(smpl, ctx, -1);
    }
    uint64_t loaded = footprint(0);

    double pp[16], tg[16];
    for (int r = 0; r < reps; r++) {
        llama_memory_clear(llama_get_memory(ctx), true);
        double a = now_s();
        if (decode(ctx, prompt, n_prompt, n_batch) != 0) { fprintf(stderr, "decode failed\n"); return 1; }
        tok = llama_sampler_sample(smpl, ctx, -1);
        double b = now_s();
        for (int i = 0; i < n_gen; i++) {
            if (llama_vocab_is_eog(vocab, tok)) tok = prompt[1];  // keep the length fixed
            if (llama_decode(ctx, llama_batch_get_one(&tok, 1)) != 0) { fprintf(stderr, "decode failed\n"); return 1; }
            tok = llama_sampler_sample(smpl, ctx, -1);
        }
        double c = now_s();
        pp[r] = n_prompt / (b - a);
        tg[r] = n_gen / (c - b);
    }
    double pp_mean, pp_sd, tg_mean, tg_sd;
    stats(pp, reps, &pp_mean, &pp_sd);
    stats(tg, reps, &tg_mean, &tg_sd);

    char desc[256] = "";
    llama_model_desc(model, desc, sizeof desc);
    printf("{\"file\":\"%s\",\"desc\":\"%s\",\"params_b\":%.2f,\"weights_gb\":%.2f,"
           "\"n_ctx\":%d,\"n_prompt\":%d,\"n_gen\":%d,\"reps\":%d,\"load_s\":%.2f,"
           "\"prompt_tps\":%.1f,\"prompt_tps_sd\":%.1f,\"gen_tps\":%.1f,\"gen_tps_sd\":%.1f,"
           "\"footprint_gb\":%.2f,\"peak_footprint_gb\":%.2f,\"max_rss_gb\":%.2f",
           strrchr(path, '/') ? strrchr(path, '/') + 1 : path, desc,
           llama_model_n_params(model) / 1e9, llama_model_size(model) / 1e9,
           n_ctx, n_prompt, n_gen, reps, load_s, pp_mean, pp_sd, tg_mean, tg_sd,
           loaded / 1e9, footprint(1) / 1e9, max_rss() / 1e9);

    if (sustain_s > 0) {
        printf(",\"sustained_window_s\":15,\"sustained_tps\":[");
        llama_memory_clear(llama_get_memory(ctx), true);
        decode(ctx, prompt, 64, n_batch);
        tok = llama_sampler_sample(smpl, ctx, -1);
        int pos = 64, in_window = 0, first = 1;
        double start = now_s(), win = start, spent_refill = 0;
        while (now_s() - start < sustain_s) {
            if (pos >= n_ctx - 4) {  // context full: start again, not counted
                double r0 = now_s();
                llama_memory_clear(llama_get_memory(ctx), true);
                decode(ctx, prompt, 64, n_batch);
                tok = llama_sampler_sample(smpl, ctx, -1);
                pos = 64;
                spent_refill += now_s() - r0;
            }
            if (llama_vocab_is_eog(vocab, tok)) tok = prompt[1];
            if (llama_decode(ctx, llama_batch_get_one(&tok, 1)) != 0) break;
            tok = llama_sampler_sample(smpl, ctx, -1);
            pos++; in_window++;
            double t = now_s();
            if (t - win - spent_refill >= 15.0) {
                printf("%s%.1f", first ? "" : ",", in_window / (t - win - spent_refill));
                fflush(stdout);
                first = 0; in_window = 0; win = t; spent_refill = 0;
            }
        }
        printf("]");
    }
    printf("}\n");

    llama_sampler_free(smpl);
    llama_free(ctx);
    llama_model_free(model);
    llama_backend_free();
    return 0;
}
