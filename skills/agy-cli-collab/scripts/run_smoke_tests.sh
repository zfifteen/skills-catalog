#!/usr/bin/env bash
set -euo pipefail

SCRATCH="${SCRATCH:-/tmp/agy-cli-collab-smoke}"
REPO="${REPO:-/Users/velocityworks/IdeaProjects/prime-gap-structure}"
HELPER="$(cd "$(dirname "$0")" && pwd)/agy_cli.py"
AGY="${AGY:-/Users/velocityworks/.local/bin/agy}"

mkdir -p "$SCRATCH"
: > "$SCRATCH/results.tsv"
PASS=0
FAIL=0

record() {
  local id="$1"
  local status="$2"
  local note="$3"
  printf '%s|%s|%s\n' "$id" "$status" "$note" >> "$SCRATCH/results.tsv"
  if [[ "$status" == "PASS" ]]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
  fi
}

run_expect_stdout() {
  local id="$1"
  local expected="$2"
  shift 2
  local out
  out="$("$@" 2>"$SCRATCH/${id}.err" | tr -d '\r' | sed '/^$/d' | tail -1)"
  echo "$out" > "$SCRATCH/${id}.out"
  if [[ "$out" == "$expected" ]]; then
    record "$id" "PASS" "stdout=$out"
  else
    record "$id" "FAIL" "expected=$expected got=$out"
  fi
}

# Phase 1 gate
[[ "$(which agy)" == "$AGY" ]] && record A-01 PASS "which agy" || record A-01 FAIL "which agy"
run_expect_stdout A-04 AGY_SMOKE_OK bash -c "cd '$REPO' && '$AGY' --dangerously-skip-permissions -p 'Reply with exactly: AGY_SMOKE_OK' --print-timeout 2m"

python3 -m py_compile "$HELPER" && record A-PY PASS py_compile || record A-PY FAIL py_compile

echo 'Reply with exactly: AGY_HELPER_NORMAL_OK' > "$SCRATCH/prompt-normal.md"
python3 "$HELPER" --cwd "$REPO" --mode start --new-project \
  --log-file "$SCRATCH/normal.log" --state-file "$SCRATCH/conv-id.txt" \
  --prompt-file "$SCRATCH/prompt-normal.md" >"$SCRATCH/helper-normal.out" 2>"$SCRATCH/helper-normal.err" || true
OUT=$(tail -1 "$SCRATCH/helper-normal.out" | tr -d '\r')
[[ "$OUT" == "AGY_HELPER_NORMAL_OK" ]] && record H-NORMAL PASS "$OUT" || record H-NORMAL FAIL "$OUT"

CONV_ID=$(cat "$SCRATCH/conv-id.txt")
echo 'Reply with exactly: AGY_HELPER_CONV_OK' > "$SCRATCH/prompt-conv.md"
python3 "$HELPER" --cwd "$REPO" --mode conversation --conversation "$CONV_ID" \
  --prompt-file "$SCRATCH/prompt-conv.md" >"$SCRATCH/helper-conv.out" 2>"$SCRATCH/helper-conv.err" || true
OUT=$(tail -1 "$SCRATCH/helper-conv.out" | tr -d '\r')
[[ "$OUT" == "AGY_HELPER_CONV_OK" ]] && record H-CONV PASS "$OUT" || record H-CONV FAIL "$OUT"

echo 'Reply with exactly: AGY_HELPER_CONTINUE_T1' > "$SCRATCH/prompt-cont-t1.md"
python3 "$HELPER" --cwd "$REPO" --mode start --new-project \
  --log-file "$SCRATCH/continue.log" --state-file "$SCRATCH/continue-id.txt" \
  --prompt-file "$SCRATCH/prompt-cont-t1.md" >"$SCRATCH/cont-t1.out" 2>/dev/null || true
echo 'Reply with exactly: AGY_HELPER_CONTINUE_OK' > "$SCRATCH/prompt-cont-t2.md"
python3 "$HELPER" --cwd "$REPO" --mode continue \
  --log-file "$SCRATCH/continue-resume.log" \
  --prompt-file "$SCRATCH/prompt-cont-t2.md" >"$SCRATCH/cont-t2.out" 2>/dev/null || true
OUT=$(tail -1 "$SCRATCH/cont-t2.out" | tr -d '\r')
[[ "$OUT" == "AGY_HELPER_CONTINUE_OK" ]] && record H-CONTINUE PASS "$OUT" || record H-CONTINUE FAIL "$OUT"

# Empty prompt (helper guard before agy spawn)
: > "$SCRATCH/empty-prompt.md"
if python3 "$HELPER" --cwd "$REPO" --mode clean \
  --prompt-file "$SCRATCH/empty-prompt.md" >"$SCRATCH/empty.out" 2>"$SCRATCH/empty.err"; then
  record C-02 FAIL "empty prompt should fail"
else
  grep -qi "empty prompt" "$SCRATCH/empty.err" && record C-02 PASS "empty prompt rejected" || record C-02 FAIL "wrong error"
fi

# Timeout (agy may emit error on stdout)
if cd "$REPO" && "$AGY" --dangerously-skip-permissions -p "Reply with exactly: SLOW" --print-timeout 1s \
  >"$SCRATCH/timeout.out" 2>"$SCRATCH/timeout.err"; then
  record G-01 FAIL "expected timeout"
else
  COMBINED=$(cat "$SCRATCH/timeout.out" "$SCRATCH/timeout.err")
  echo "$COMBINED" | grep -qi "timeout waiting for response" \
    && record G-01 PASS "timeout error" || record G-01 FAIL "wrong error"
fi

# D-07 / D-08 log markers
grep -q "Created conversation" "$SCRATCH/normal.log" && record D-07 PASS "uuid in log" || record D-07 FAIL "no uuid"
grep -q "resuming conversation" "$SCRATCH/continue-resume.log" && record D-08 PASS "resume in log" || record D-08 FAIL "no resume log"

# E-01 repo read via add-dir
echo 'Read PROOF.md first line only. Reply with exactly that line, nothing else.' > "$SCRATCH/e01.md"
OUT=$(python3 "$HELPER" --cwd "$REPO" --mode clean --prompt-file "$SCRATCH/e01.md" 2>/dev/null | tr -d '\r' | sed '/^$/d' | tail -1)
[[ "$OUT" == "# Proof" ]] && record E-01 PASS "$OUT" || record E-01 FAIL "got=$OUT"

# E-03 / E-04 new-project chain
PROJ="agy-smoke-$(date +%s)"
echo 'Reply with exactly: E03_T1' > "$SCRATCH/e03-t1.md"
python3 "$HELPER" --cwd "$REPO" --mode start --new-project --project "$PROJ" \
  --log-file "$SCRATCH/e03.log" --state-file "$SCRATCH/e03-id.txt" \
  --prompt-file "$SCRATCH/e03-t1.md" >/dev/null 2>/dev/null
echo 'Reply with exactly: E03_T2' > "$SCRATCH/e03-t2.md"
OUT=$(python3 "$HELPER" --cwd "$REPO" --mode continue --project "$PROJ" \
  --prompt-file "$SCRATCH/e03-t2.md" 2>/dev/null | tr -d '\r' | sed '/^$/d' | tail -1)
[[ "$OUT" == "E03_T2" ]] && record E-04 PASS "$OUT" || record E-04 FAIL "got=$OUT"
grep -q "Created conversation" "$SCRATCH/e03.log" && record E-03 PASS "new project conv" || record E-03 FAIL "no conv"

# I-01 / I-08 / K-02 static checks
grep -qi "Never.*MCP\|never.*agy_" /Users/velocityworks/.grok/skills/agy-cli-collab/SKILL.md \
  && record I-01 PASS "mcp forbidden" || record I-01 FAIL "no mcp rule"
grep -qi "read-only" /Users/velocityworks/.grok/skills/agy-cli-collab/SKILL.md \
  && record I-08 PASS "read-only default" || record I-08 FAIL "no read-only"
[[ -f /Users/velocityworks/.grok/skills/agy-cli-collab/SKILL.md \
  && -f /Users/velocityworks/.grok/skills/agy-cli-collab/scripts/agy_cli.py \
  && -f /Users/velocityworks/.grok/skills/agy-cli-collab/references/TEST_PLAN.md ]] \
  && record K-02 PASS "tree ok" || record K-02 FAIL "missing files"

# Pinned recall T1/T3
MARKER="PINNED_RECALL_$(date +%s)"
echo "Reply with exactly: $MARKER" > "$SCRATCH/pinned-t1.md"
python3 "$HELPER" --cwd "$REPO" --mode start --new-project \
  --log-file "$SCRATCH/pinned.log" --state-file "$SCRATCH/pinned-id.txt" \
  --prompt-file "$SCRATCH/pinned-t1.md" >/dev/null 2>/dev/null
PINNED_ID=$(cat "$SCRATCH/pinned-id.txt")
echo "What exact marker text did I ask you to reply with in our first message? Reply with only that marker, nothing else." > "$SCRATCH/pinned-t3.md"
python3 "$HELPER" --cwd "$REPO" --mode conversation --conversation "$PINNED_ID" \
  --prompt-file "$SCRATCH/pinned-t3.md" >"$SCRATCH/pinned-t3.out" 2>/dev/null || true
OUT=$(tail -1 "$SCRATCH/pinned-t3.out" | tr -d '\r')
[[ "$OUT" == "$MARKER" ]] && record D-09 PASS "pinned recall" || record D-09 FAIL "got=$OUT want=$MARKER"

# cwd isolation
MARKER_TMP="CWD_TMP_$(date +%s)"
TMPWS="$SCRATCH/tmpws-$MARKER_TMP"
mkdir -p "$TMPWS"
echo "Reply with exactly: $MARKER_TMP" > "$SCRATCH/cwd-t1.md"
python3 "$HELPER" --cwd "$TMPWS" --mode start --new-project \
  --log-file "$SCRATCH/cwd.log" --state-file "$SCRATCH/cwd-id.txt" \
  --add-dir "$REPO" --prompt-file "$SCRATCH/cwd-t1.md" >/dev/null 2>/dev/null
echo 'Reply with exactly: CWD_REPO_PROBE' > "$SCRATCH/cwd-t2-repo.md"
python3 "$HELPER" --cwd "$REPO" --mode continue \
  --prompt-file "$SCRATCH/cwd-t2-repo.md" >"$SCRATCH/cwd-repo.out" 2>/dev/null || true
OUT=$(tail -1 "$SCRATCH/cwd-repo.out" | tr -d '\r')
[[ "$OUT" == "CWD_REPO_PROBE" ]] && record D-05 PASS "repo cwd separate thread" || record D-05 FAIL "got=$OUT"

echo "PASS=$PASS FAIL=$FAIL"
cat "$SCRATCH/results.tsv"