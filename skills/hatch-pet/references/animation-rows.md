# Animation Rows (Grok Port)

The target runtime (Codex-style digital pet or compatible) expects one fixed atlas: 8 columns, 9 rows, 192x208 pixels per cell.

| Row | State | Used columns | Durations |
| --- | --- | ---: | --- |
| 0 | idle | 0-5 | 280, 110, 110, 140, 140, 320 ms |
| 1 | running-right | 0-7 | 120 ms each, final 220 ms |
| 2 | running-left | 0-7 | 120 ms each, final 220 ms |
| 3 | waving | 0-3 | 140 ms each, final 280 ms |
| 4 | jumping | 0-4 | 140 ms each, final 280 ms |
| 5 | failed | 0-7 | 140 ms each, final 240 ms |
| 6 | waiting | 0-5 | 150 ms each, final 260 ms |
| 7 | running | 0-5 | 120 ms each, final 220 ms |
| 8 | review | 0-5 | 150 ms each, final 280 ms |

Unused cells after each row's final used column must be fully transparent.

## Row Purposes (Grok Context)

- `idle`: neutral breathing/blinking loop; use as the reduced-motion static frame.
- `running-right` / `running-left`: directional locomotion. Only derive left by mirror when visual inspection + explicit approval confirms the pet is sufficiently symmetric (no one-sided markings, text, props, lighting, or gait asymmetry).
- `waving`, `jumping`, `failed`, `waiting`, `running`, `review`: state-specific readable actions at tiny 192x208 size. Pose and silhouette changes only; no detached effects, speed lines, or shadows (see full transparency rules in SKILL.md and prepare script).

This file is the single source of truth for frame counts and row ordering in any hatch-pet run.
