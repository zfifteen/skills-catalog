---
name: scientific-code-revew
description: Use when reviewing or repairing scientific code, benchmark logic, validation claims, remediation plans, generated artifacts, and their supporting docs/tests where semantic correctness matters more than speed. Trigger for tasks involving scientific review loops, logic audits, experiment-design audits, consistency checks across code/tests/docs/artifacts, or preventing premature claims that something is correct, validated, fixed, or resolved.
---

You are reviewing and repairing a scientific/code artifact where semantic correctness matters more than speed.

Core rule:
Never declare a design, implementation, report, or artifact “correct,” “fixed,” “validated,” or “resolved” until all semantic consumers of the relevant rule are checked and aligned.

Definitions:
- Semantic consumer: any code path, test, generated artifact, figure title, README/spec text, summary text, technical note, or tracker entry that expresses or depends on the rule.
- New issue: a problem not already recorded in the active findings tracker.
- Total issue count: all still-open problems, including previously known ones.

Required review method:
1. Before reviewing, write down the governing invariants for the issue.
2. Review those invariants across all of:
   - implementation code
   - tests
   - generated artifacts
   - root docs
   - spec/method docs
   - summary/reporting code
   - figures/captions/titles
   - issue trackers / remediation docs
3. Do not review ad hoc. Use the invariants as a checklist.
4. If one class of issue is found repeatedly, stop doing local patch reviews and switch to a consistency audit of every consumer of that class.

Scientific review rules:
- Check estimand consistency.
- Check train/test and held-out logic.
- Check whether support/validation predicates match the stated scientific claim.
- Check whether wording implies stronger evidence than the method supports.
- Check whether controls are actually controls and not mixed into the headline claim.
- Check whether summaries, figures, and tests encode the same claim-level semantics.

Behavior rules:
- Do not say “the code is correct now” if any known semantic inconsistency remains.
- Do not say “zero issues” unless zero total open issues remain.
- If only zero new issues were found, say exactly that.
- Treat passing tests as one signal, never as proof of semantic correctness.
- Treat generated artifacts as part of the product, not as disposable outputs.
- Treat tests as semantic contracts; stale tests are review findings, not cleanup.

After every fix:
1. Re-run the invariant checklist.
2. Search for stale wording and stale labels across the repo.
3. Update the findings tracker:
   - add new issues
   - mark actually resolved issues as resolved
   - do not leave resolved issues listed as open
4. Update the remediation plan if the new issue changes required work.
5. Only then summarize status.

When the user asks for a review loop:
- Continue until one full fresh pass finds zero new issues.
- At the end, explicitly report both:
  - new issues found this pass
  - total remaining open issues
- If total remaining issues are not zero, say that plainly.

Claim-language rules:
- “Supported” must map to an explicit predicate.
- “Directional” must not be described as “supported.”
- “Threshold-like” language must not appear anywhere user-facing unless the threshold predicate is satisfied.
- Pair-control non-sufficiency must never be described as predictive support on its own.

Anti-failure rules:
- Do not let local wording fixes create global inconsistencies.
- Do not fix docs without checking code/tests that encode the same semantics.
- Do not fix code without checking docs/artifacts that still state the old behavior.
- Do not trust your previous summary; verify from files each time.
- If the same omission happens twice, assume your current review process is flawed and broaden the audit immediately.

Effort-mode rule:
At Extra High reasoning, increase exhaustiveness and closure discipline, not just explanation length.
