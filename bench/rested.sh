#!/bin/bash
# A rested pass: three minutes of idle before each model, five repetitions.
#   rested.sh <label> <model.gguf> [<label> <model.gguf> ...]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
while [ $# -ge 2 ]; do
  label="$1"; model="$2"; shift 2
  # mains power only: on battery the numbers are not comparable with the rest
  until pmset -g batt | head -1 | grep -q "AC Power"; do sleep 20; done
  sleep 180
  pmset -g batt | head -1 | grep -q "AC Power" || { echo "on battery again, skipping $(basename "$model")"; continue; }
  load="$(sysctl -n vm.loadavg | awk '{print $2}')"
  power="$(pmset -g batt | head -1 | grep -o "'[^']*'" | tr -d "'")"
  line="$("$HERE/bench" "$model" 4096 512 256 5 2>>"$HERE/errors.log")"
  [ -n "$line" ] || line="{\"file\":\"$(basename "$model")\",\"failed\":true}"
  printf '%s\n' "${line%\}},\"run\":\"$label\",\"at\":\"$(date -u +%H:%M:%S)\",\"load1\":$load,\"power\":\"$power\",\"speed_limit_lines\":0}" >> "$HERE/results.jsonl"
  echo "$(date +%H:%M:%S) $label $(basename "$model"): $(printf '%s' "$line" | grep -o '"gen_tps":[0-9.]*,"gen_tps_sd":[0-9.]*') load $load"
done
echo "rested pass finished"
