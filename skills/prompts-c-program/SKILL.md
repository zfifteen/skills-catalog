---
name: prompts-c-program
description: >
  Apply the "C Program" prompt-library workflow: given a task description or mathematical/computational
  problem, scaffold a disciplined, self-contained C-program workspace under src/c/<name>/ (or equivalent
  project-appropriate location). The scaffold must include a Makefile that integrates with any parent
  build for GMP/MFPR large-number support (no new external dependencies introduced), a demonstration
  shell script, full build that produces a working executable, and clear documentation inside the folder only.
  Never modify artifacts outside the new folder.
  Use when the user says "scaffold a C program for...", "create C workspace for this problem", "use the
  C Program prompt on this task", "set up disciplined C project with GMP", or runs /prompts-c-program.
when-to-use: "Scaffolding a new, well-isolated C implementation for large-integer or high-precision numerical work. Triggers: 'C program', 'C workspace', 'GMP/MFPR', 'disciplined C scaffold', 'src/c/ folder'. Especially relevant for prime-gap or number-theoretic experiments."
argument-hint: "<task description or mathematical problem to implement in disciplined C>"
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "run_terminal_cmd"]
metadata:
  short-description: "Scaffold disciplined C workspace with GMP/MFPR, Makefile, demo script (self-contained)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-c-program/SKILL.md"
  version: "1.0.0"
---

# C Program — Grok Port

Scaffold a production-quality, minimal-dependency C workspace that respects large-number arithmetic conventions used in this project (GMP + MPFR) while keeping every artifact strictly inside its own folder.

## Purpose

The original prompt enforces workspace hygiene and build discipline for C experiments that deal with "insanely large numbers". This Grok port turns the prompt into an active scaffolder that actually creates the folder, Makefile, demo script, and build artifacts using the available tools.

## Invocation

```
/prompts-c-program <description of the C task or algorithm to implement>
```

The description (plus any additional constraints from the conversation) becomes the `{shortcut_input}` / task specification.

## Core Contract (Preserved from Original)

- Create a **new folder** under `src/c/` (or the nearest equivalent conventional location for the current project) for **all** artifacts and documentation.
- **Do not modify any artifacts outside** of the new folder.
- Create a **Makefile** that includes the parent Makefile for all dependencies.
- The new Makefile **must not introduce any new dependencies**.
- **Always use GMP/MPFR** as we work in insanely large numbers.
- Invoke the parent to build shared libs.
- Include a **shell script to demonstrate** usage.
- Ensure `make` builds the executable.

## Grok Scaffolding Workflow

1. **Determine Target Location**
   - Inspect the workspace with `list_dir` at root and common source areas.
   - Default target: `src/c/<kebab-case-task-name>/`
   - If the project already has a different convention (e.g. `c-experiments/`), adapt intelligently but still isolate everything inside one new subfolder.
   - Create the directory by writing the first file into it (the tools will create parents as needed).

2. **Design the Minimal Interface**
   - From the task description, identify the core computation, required inputs/outputs, and any CLI or library entry points.
   - Keep the public surface tiny (one or two .c files + header if library).

3. **Create the Scaffold Files** (using `write` or `search_replace` with empty old for new files)

   Required files (all inside the new folder only):
   - `README.md` — purpose, build instructions, how to run the demo, GMP/MPFR notes.
   - `Makefile` — includes parent (e.g. `include ../../Makefile` or correct relative path), declares GMP/MPFR linkage (`-lgmp -lmpfr`), builds the executable from the .c sources, has `clean` and `demo` targets.
   - `main.c` (or `taskname.c`) — skeleton with includes for gmp.h / mpfr.h, basic error handling, CLI argument parsing (getopt or simple), clear "TODO: implement core logic here" section.
   - `demo.sh` — executable shell script that builds (if needed) and runs the program with representative inputs, shows output, exits non-zero on failure. Includes `#!/bin/bash` and `set -euo pipefail`.
   - `FINDINGS.md` or `NOTES.md` (optional but recommended) — for recording results of the C run.

4. **Parent Makefile Integration**
   - The child Makefile must invoke or extend the parent so that `make -C src/c/<name>` works and shared libs from the project root are available.
   - Document the exact invocation in the README.

5. **Build & Verify**
   - After writing files, run `make` (via `run_terminal_cmd` if available, or instruct the user) from inside the new folder or with correct `-C`.
   - Confirm the executable is produced and the demo script runs successfully.
   - If build fails, fix the scaffold immediately using search_replace.

6. **Documentation Discipline**
   - Every file inside the folder must be self-documenting or have clear comments.
   - No external dependencies beyond what the parent already provides + GMP/MPFR (assumed present in the environment).

## Output Contract

After scaffolding:

- Report the absolute path of the created folder.
- Show a tree or list of created files.
- Provide the exact commands to build and run the demo.
- Include a one-paragraph summary of the intended implementation task inside the folder's README.
- If the task description contained mathematical invariants or PGS objects, note them explicitly in the code skeleton and README so the C implementation starts from the correct native frame (per AGENTS.md).

## Success Criteria

- A new isolated folder exists containing only the scaffold for this task.
- `make` succeeds and produces a runnable executable.
- `demo.sh` runs and demonstrates the program (even if the core algorithm is still a stub).
- No files were created or modified outside the designated folder.
- The scaffold is ready for an implementer (human or agent) to fill in the actual algorithm without fighting the build system.
- GMP/MPFR headers and linkage are correctly referenced.

## Guardrails

- **Hygiene is non-negotiable.** If the environment prevents creating the folder in the ideal location, ask the user for explicit approval before using any other location.
- Do not add new third-party libraries, build systems (Meson, CMake unless the parent already uses them), or package managers.
- The demo script must be robust (proper quoting, error propagation).
- For PGS-related C work: the skeleton must include comments reminding the implementer to reason from PGS objects/invariants first.

## Example Generated Structure (for reference)

```
src/c/prime-gap-counter/
├── README.md
├── Makefile
├── main.c
├── demo.sh
└── NOTES.md
```

This skill gives Grok the ability to turn a high-level numerical task into a ready-to-code, correctly-built C experiment harness while strictly honoring the original workspace-isolation and large-number conventions.
