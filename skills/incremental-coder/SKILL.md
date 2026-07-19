---
name: incremental-coder
description: "Incremental, phase-based implementation workflow for bounded feature work or refactors that benefit from scaffold-first construction, tight validation gates, and traceable commits. Use when Codex should implement a non-trivial code change in small reviewable steps: first create the full structural scaffold with tests and no business logic, then implement only the main entry point, then implement exactly one remaining section per iteration while running the repository's standard build and test commands after each step."
---

# Incremental Coder

Implement the requested change as a strict three-phase sequence. Optimize for traceability, reviewability, and deterministic progress rather than shortest-path coding.

## Start-Up

1. Inspect the repository and define the narrow requested scope.
2. Identify the repository's standard validation commands before editing.
3. Identify the main entry point for the requested change.
4. Define the remaining unimplemented sections as bounded units such as one class, one function, one module, one route handler, or one testable slice of a component.
5. State the chosen validation commands and the first phase in commentary.

- Reuse the repository's existing build, check, lint, and test commands. Do not invent a parallel toolchain.
- If no clear repo-native validation command exists, stop and say that explicitly before implementation.
- Keep the scaffold exact to the request. Do not add speculative modes, abstractions, or extension points.

## Phase One: Scaffold

Create the full structural skeleton of the requested change without implementing business logic.

- Add the files, types, functions, methods, interfaces, routes, or components required for the requested contract.
- Add the matching test files or test cases for each scaffolded unit.
- Leave logic unimplemented with explicit stubs that make the state obvious, such as `TODO`, `NotImplemented`, `throw`, `pass`, or equivalent placeholders.
- Make the code build cleanly if the repository permits scaffold-only builds.
- Keep tests green only by asserting explicit placeholder behavior or by using the repository's normal pending-test mechanism. Do not fake implementation logic.
- Add concise comments or docstrings only where the structure would otherwise be unclear. Explain purpose, expected inputs and outputs, and connections between sections.
- Use end-user intent in tests when the project style allows it. Prefer test names or short comments such as "As a user, I want..." rather than internal-only phrasing.

When commits are allowed for the task, create a phase commit with a conventional-commit prefix, for example `feat: phase one scaffold complete`.

## Phase Two: Main Entry Point

Implement only the main coordinating entry point for the requested change.

- Treat the entry point as the narrow place where control enters the new behavior. This may be a `main()` function, CLI command, route handler, controller action, exported API, top-level React component, or similar coordinator.
- Implement only this entry point and the minimum wiring it needs.
- Leave all downstream sections unimplemented if they were still stubs after Phase One.
- Update the entry-point tests to reflect the intended top-level behavior.
- Add concise comments only for non-obvious orchestration.

Run the repository's standard validation commands. If they fail, fix them before continuing.

When commits are allowed for the task, create a phase commit such as `feat: phase two implement entry point`.

## Phase Three: One Section Per Iteration

Implement the remaining scaffold one bounded section at a time.

For each iteration:

1. Choose exactly one unimplemented section.
2. Implement that section fully.
3. Update the directly relevant tests.
4. Run the repository's standard validation commands.
5. Commit that one section before moving on.

- Never implement more than one remaining section in a single iteration.
- Keep the rest of the scaffold untouched unless a direct interface adjustment is required by the chosen section.
- Use concise comments only for reasoning or behavior that would otherwise be hard to recover from the code itself.
- If a validation command fails, stop, fix the failure, rerun validation, and only then continue to the next section.

When commits are allowed for the task, use a conventional-commit message such as `feat: phase three implement request parser`.

## Validation Rules

- Run the repository's lightweight build or check command when changing focus between artifacts if such a command exists.
- Run the repository's standard test command after each phase and after each Phase Three section.
- Prefer the smallest repo-native command that gives a real signal for the current step.
- Use deterministic commands and deterministic fixtures. Do not add randomness, backup execution paths, or silent degradations just to make incremental progress appear smoother.
- Stop and surface blockers plainly instead of widening scope or inventing alternate implementations.

## Output Discipline

- Label phase transitions clearly in commentary and in the final summary.
- Keep each phase boundary logically complete and easy to review.
- Preserve a straight-line implementation path. The purpose of the skill is not to scaffold a framework; it is to make one requested change traceable from empty structure to complete behavior.
