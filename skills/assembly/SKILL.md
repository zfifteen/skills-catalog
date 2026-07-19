---
name: assembly
description: >
  Write, review, optimize, benchmark, or reason about assembly code for speed,
  efficiency, SIMD/vectorization, CPU hot paths, low-level kernels, instruction
  selection, register pressure, cache behavior, branch behavior, or compiler
  output. Use when the user asks for assembly, "write the kernel in asm",
  "review this assembly", "optimize this hot path", "explain the instruction
  schedule", "reduce latency in this loop", or provides surrounding C/ code + 
  benchmark target and wants invariant-first low-level work.
when-to-use: "Invoked for any low-level performance work involving hand-written or reviewed assembly, SIMD kernels, compiler output analysis, or micro-optimization where the bottleneck is machine-level (not high-level algorithm). Trigger phrases: 'assembly', 'the asm version', 'inline assembly', 'SIMD kernel', 'register pressure', 'cache miss analysis'."
allowed-tools: ["read_file", "grep", "list_dir", "search_replace", "write", "web_search", "web_fetch", "open_page", "open_page_with_find", "todo_write", "memory_search", "memory_get"]
argument-hint: "<workload description, hot path identification, or filesystem path to surrounding code> [target-arch: x86_64|aarch64|...] [benchmark context or acceptance criteria]"
metadata:
  short-description: "Invariant-first assembly kernel authoring, review, and optimization"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/assembly/SKILL.md"
---

# Assembly — Grok Edition

## Contract

Treat assembly optimization as **invariant-first analysis** plus one narrow machine-code kernel. The assembly is the final artifact, not the first move.

Before writing or changing assembly, identify (using tools to inspect when local artifacts exist):

- invariant workload shape
- exact hot path (measured or profiled)
- real bottleneck (memory BW, cache, dependency chains, etc.)
- data representation and layout
- correctness contract
- benchmark target and acceptance threshold
- target architecture and ABI

If these facts are explicit in the user request or discoverable from local code via `read_file` / `grep` / `list_dir`, proceed from them. If an essential fact is missing and affects correctness, stop and name the missing contract plainly.

## Required Workflow

1. **Observe the workload** (use tools)
   - Read the surrounding code, benchmark harness, compiler output (`-S`, `-fverbose-asm`, `objdump`, `perf`, `llvm-mca`, etc.), or user-provided kernel using `read_file`, `grep` (with context).
   - State what repeats, what input shape is stable, and what output must be preserved.
   - Capture exact file:line anchors for the hot path.

2. **Classify the bottleneck**
   - Decide whether the limit is memory bandwidth, cache locality, load/store traffic, dependency chains, branch prediction, instruction throughput, instruction latency, SIMD occupancy, call overhead, or ABI friction.
   - Use web tools for architecture manuals, instruction latency tables (e.g., Agner Fog, uops.info, Intel/ARM optimization guides) when needed: `web_search` or `open_page`.

3. **Define the representation**
   - State the data layout, alignment, stride, aliasing rules, element width, vector lane shape, and edge handling.
   - Prefer changing representation (data layout, packing) before adding instruction cleverness when the task allows it.

4. **Write or review the minimal kernel**
   - Keep the kernel small, deterministic, and tied to the measured bottleneck.
   - Do not rewrite unrelated code, add generalized frameworks, or create speculative portability layers.
   - Use `write` or targeted `search_replace` to produce the .s or inline asm.

5. **Verify correctness**
   - Compare against a trusted scalar, compiler-generated, or existing implementation when available.
   - Include edge cases for length, alignment, overlap, signedness, overflow, NaNs, carries, or platform-specific behavior when relevant.
   - Produce or reference a test harness.

6. **Benchmark honestly**
   - Measure before and after (user runs the harness or provides numbers).
   - Report speed claims only with the benchmark context: hardware, compiler, flags, input size, data distribution, warmup, repeat count, and metric.
   - Record results in a durable artifact (e.g. via `write` to a `bench-*.md` or update existing).

## Pre-Assembly Checklist

Confirm or infer these (via inspection + web references) before emitting assembly:

- architecture: x86-64, AArch64, ARM64, RISC-V, or another target
- syntax and toolchain: AT&T, Intel, GAS, NASM, MASM, LLVM integrated assembler, or inline assembly (with C compiler)
- ABI and calling convention (System V AMD64, AAPCS, etc.)
- clobbered registers and preserved registers
- input and output pointer shape (including constness, alignment guarantees)
- length units: bytes, elements, pixels, coefficients, limbs, or frames
- aliasing and overlap rules (restrict, noalias, provenance)
- exactness rules: integer wrap, saturation, rounding, floating-point mode, flags, or carries
- edge behavior for zero length, short length, unaligned head/tail, and non-multiple vector widths
- benchmark target and acceptance threshold (e.g., "2.3× on Zen 4 for N=4096, 1000 warm runs")

## Optimization Heuristics (Grok Execution)

- Optimize memory traffic before instruction count.
- Treat SIMD as data geometry: match lane width, element size, and instruction semantics to the real layout.
- Prefer predictable straight-line loops in hot paths.
- Remove unpredictable branches only when the replacement reduces measured cost.
- Watch register pressure; spills destroy clever instruction schedules.
- Separate latency-bound work from throughput-bound work.
- Keep dependency chains short in repeated loops.
- Align data and loop structure with cache lines and prefetch behavior only when the access pattern earns it.
- Use compiler output as evidence (`-S`, `objdump -d -S`, `llvm-mca`). Preserve what the compiler already does well and intervene where it cannot express the needed contract.
- Keep scalar cleanup paths simple and auditable.
- When using tools: `grep -A 20 -B 5 "hot_label"` or targeted `read_file` with offset/limit for large compiler dumps.

## Output Shape

**For authoring tasks**, return in this order:

1. Workload and bottleneck analysis (with evidence locators: file:line or compiler flag output excerpts)
2. The assembly kernel or inline assembly (complete, ready to paste or written via tool)
3. The correctness contract (explicit invariants, edge rules, required numeric results)
4. The benchmark command or measurement plan (exact flags, input generator, metric, acceptance)
5. Any verification harness or diff needed

**For review tasks**, return findings first, ordered by severity, with file and line references when available. Focus on: correctness bugs, ABI violations, clobber mistakes, missed bottlenecks, unsafe assumptions, and unmeasured claims. Use `search_replace` recipes for fixes.

**For explanation tasks**, start from observable machine facts (instruction semantics, measured latencies, cache line behavior), then define the relevant terms, then explain the instruction-level mechanism. Cite sources via `web_fetch` results with inline citations where external.

## Visible Artifacts & Tool Usage

- Always prefer editing existing files with `search_replace` (unique context) over writing new standalone .s files unless the contract calls for a fresh kernel.
- Use `todo_write` for complex multi-variant kernel exploration (different unroll factors, different shuffle strategies, etc.).
- For external reference data (latency tables, ABI docs): fetch once with `web_search`/`open_page_with_find` and cite the specific sections.
- Record benchmark numbers and hardware context in a workspace-local Markdown log so future sessions can resume without re-measurement.

## Guardrails

- Do not write assembly when the architecture or ABI is unknown and correctness depends on it.
- Do not claim speedups without measurements or a clearly labeled expectation + hardware context.
- Do not add fallback paths, alternate implementations, or silent degradations unless the user explicitly asks for them.
- Do not broaden a narrow kernel task into a whole-system rewrite.
- Do not optimize for cleverness, portability theater, or future extensibility when the requested contract is a specific hot path.
- Do not hide uncertainty about undefined behavior, flags, aliasing, alignment, or floating-point semantics.
- In this workspace (prime-gap-structure), if the assembly touches number-theoretic hot paths (e.g., divisor counting, sieving analogs, big-integer in research/ or src/c/), surface any relevant deterministic structure first; do not default to probabilistic or classical crypto framing unless the user explicitly requests a comparison.

## Success Criteria

- The delivered kernel or review is the smallest honest artifact that satisfies the locked workload contract.
- All claims about performance or correctness are traceable to either measurement or explicit static analysis of the instructions + data layout.
- A competent low-level engineer can take the output, build it, run the benchmark, and reproduce the claimed behavior (or the review findings) with the stated pins.
- No unnecessary motion, generalized frameworks, or speculative portability code remains.

Only mention the skill when the user inquires about the method or invokes it explicitly.
