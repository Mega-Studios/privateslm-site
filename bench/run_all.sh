#!/bin/bash
# Runs the whole measurement plan and appends one JSON object per run to results.jsonl.
#   run_all.sh <dir with the .gguf files> <path to the 7B model already on disk>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="$1"; EXTRA="$2"
OUT="$HERE/results.jsonl"
COOL="${COOL:-75}"

MODELS=(
  "$DIR/LFM2.5-1.2B-Instruct-Q4_K_M.gguf"
  "$DIR/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
  "$DIR/LiquidAI_LFM2.5-2.6B-Q4_K_M.gguf"
  "$DIR/gemma-2-2b-it-Q4_K_M.gguf"
  "$DIR/ai9stars_G9v3-3B-Q4_K_M.gguf"
  "$DIR/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
  "$DIR/Nanbeige_Nanbeige4.2-3B-IQ4_XS.gguf"
  "$DIR/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf"
  "$EXTRA"
  "$DIR/qwen2.5-coder-7b-instruct-q4_k_m.gguf"
  "$DIR/Ornith-1.5-9B-Q4_K_M.gguf"
  "$DIR/gpt-oss-20b-Q4_K_M.gguf"
)

run() {  # label, model, bench args...
  local label="$1" model="$2"; shift 2
  local load power therm line
  load="$(sysctl -n vm.loadavg | awk '{print $2}')"
  power="$(pmset -g batt | head -1 | grep -o "'[^']*'" | tr -d "'")"
  therm="$(pmset -g therm 2>/dev/null | grep -c 'CPU_Speed_Limit' )"
  line="$("$HERE/bench" "$model" "$@" 2>>"$HERE/errors.log")"
  if [ -z "$line" ]; then
    line="{\"file\":\"$(basename "$model")\",\"failed\":true}"
  fi
  printf '%s\n' "${line%\}},\"run\":\"$label\",\"at\":\"$(date -u +%H:%M:%S)\",\"load1\":$load,\"power\":\"$power\",\"speed_limit_lines\":$therm}" >> "$OUT"
  echo "$(date +%H:%M:%S) $label $(basename "$model") done"
}

: > "$HERE/errors.log"
echo "== pass A (small to large)"
for m in "${MODELS[@]}"; do run passA "$m" 4096 512 256 5; sleep "$COOL"; done

echo "== pass B (large to small)"
for ((i=${#MODELS[@]}-1; i>=0; i--)); do run passB "${MODELS[$i]}" 4096 512 256 5; sleep "$COOL"; done

echo "== memory by context size"
for m in "${MODELS[5]}" "${MODELS[9]}" "${MODELS[10]}" "${MODELS[11]}"; do
  for ctx in 2048 8192 16384 32768; do run "ctx$ctx" "$m" "$ctx" 512 64 1; sleep 20; done
done

echo "== sustained generation, 5 minutes"
sleep 180
run sustained "${MODELS[5]}" 4096 512 64 1 300
sleep 300
run sustained "${MODELS[9]}" 4096 512 64 1 300
echo "== finished"
