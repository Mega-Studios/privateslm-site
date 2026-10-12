# Local model benchmark

The code and the raw data behind three blog posts:
[speed on an M5 MacBook Air](https://www.privateslm.dev/blog/local-llm-speed-m5-macbook-air.html),
[how much RAM a local model needs](https://www.privateslm.dev/blog/how-much-ram-local-llm-mac.html) and
[which Mac mini to buy](https://www.privateslm.dev/blog/mac-mini-local-ai.html).

## Files

- `bench.c` — loads one GGUF model through llama.cpp with every layer on Metal and prints one JSON
  object: prompt speed, generation speed, memory, and optionally the generation rate over a long run.
- `run_all.sh` — the measurement plan: two passes over every model in opposite orders, then memory at
  several context sizes, then two five-minute runs.
- `rested.sh` — one more pass with three minutes of idle before each model, on mains power only.
- `results.jsonl` — every run that counts, one JSON object per line.

## Building

`bench.c` includes `<llama/llama.h>`, the way the llama.cpp XCFramework exposes it:

```
clang -O2 -arch arm64 -F <dir with llama.framework> -framework llama \
      -Wl,-rpath,<dir with llama.framework> -o bench bench.c
./bench model.gguf [n_ctx=4096] [n_prompt=512] [n_gen=256] [reps=3] [sustain_seconds=0]
```

Against a plain llama.cpp build, change the include to `"llama.h"` and link `-lllama` instead. The
published numbers were taken with llama.cpp release b10488, the build privateSLM 2.3 ships.

## Reading results.jsonl

| Field | Meaning |
|---|---|
| `run` | `passA` (small to large), `passB` (large to small), `passC` / `passD` (after three minutes of rest), `ctx<N>` (context of N tokens, for memory), `sustained` |
| `prompt_tps`, `gen_tps` | tokens per second, mean of `reps` repetitions; `_sd` is the standard deviation between them |
| `weights_gb` | size of the model's tensors, decimal GB |
| `peak_footprint_gb` | the process's peak memory footprint: working memory, without the memory-mapped weights |
| `max_rss_gb` | peak resident memory, which includes whatever part of the weights was resident — do not read it as "memory needed" |
| `sustained_tps` | tokens per second in consecutive 15-second windows |
| `load1`, `power` | the Mac's one-minute load average and power source when the run started |

Speeds in the `ctx<N>` runs are not speed measurements: those ran back to back on a warm machine and
are there for the memory figures only.

## What is not in the file

Thirteen runs were thrown away. Eight came from a wrapper script that skipped the rest between
models; five were made after the laptop had been unplugged (it switches to Low Power Mode on battery)
and had gone to sleep. One kept run is known to be disturbed — `passC` for Ornith 1.5 9B ran while
the laptop was in use — which is why that model has a `passD`.

The machine: MacBook Air, Apple M5 (10-core CPU, 10-core GPU), 24 GB, macOS 26.5, on mains power, in
an ordinary desktop session with other apps open.

## The posts are generated

`build_posts.py` writes the three posts, their entries in the blog index and `llms.txt`, and the chart
pages, taking every number from `results.jsonl`:

```
python3 bench/build_posts.py bench/results.jsonl . /tmp/charts 19.07
python3 scripts/gen_blog_meta.py
```

The last argument is the GPU memory, in GB, that Metal recommends one app stay within on the test
machine (`MTLDevice.recommendedMaxWorkingSetSize`). The charts come out as 1200×630 HTML pages;
screenshot each into `assets/blogimg/` under the same name with `.png`. Change the wording of a post
in the script, not in the generated HTML, or the next run will undo it.
