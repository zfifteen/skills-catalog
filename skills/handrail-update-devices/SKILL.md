---
name: handrail-update-devices
description: >
  Build and install the Handrail iOS app on connected physical iPhone and iPad devices using the project's deterministic release tooling. 
  Use when the user asks to update, refresh, deploy, install, or push the Handrail app to an attached iPhone, iPad, or both from the /Users/velocityworks/IdeaProjects/handrail project.
when-to-use: "User wants to push the latest Handrail build to real iOS devices attached to the Mac. 'update handrail on my phone', 'install handrail on the iPad', 'deploy the app to my devices', 'handrail device update'."
allowed-tools: ["run_terminal_cmd", "read_file"]
argument-hint: "[--repo /path/to/handrail]"
metadata:
  short-description: "iOS physical device build + install for the Handrail project (xcrun devicectl + xcodebuild)"
  source: "Codex 'handrail-update-devices' skill (ported 2026-05-24)"
---

# Handrail Device Update (Grok Port)

## Purpose

Build and install the Handrail iOS app on connected physical iPhone and iPad devices.

**Use the repository release/update script for this workflow.** Do not hand-write a parallel build or install sequence.

## Primary Workflow (per original contract)

1. Run the canonical repository script:
   `/Users/velocityworks/IdeaProjects/handrail/tools/release/update_ios_release.py`

   (This is the authoritative script that performs the full release dance: version bump, build number increment, `HANDRAIL_LAST_UPDATED` stamp, git commit, tag push, GitHub release creation, build, and device install.)

2. The script discovers candidate physical devices via `xcrun devicectl list devices --json-output`.
3. It queries details for each candidate so CoreDevice can establish tunnels and unavailable devices are rejected early.
4. It performs the release metadata work, builds `ios/Handrail/Handrail.xcodeproj` with Release configuration for `generic/platform=iOS`.
5. It installs the resulting `Handrail.app` on every install-ready physical iPhone/iPad discovered.
6. Report version, devices updated, and any skipped devices with the exact reason printed by the script.

## Supporting Script (also ported)

This skill also ships the original supporting device-update script for cases where only the build+install step (without the full release/tag flow) is desired:

`<SKILL_DIR>/scripts/update_handrail_devices.py`

It can be invoked directly:
```bash
python3 "<SKILL_DIR>/scripts/update_handrail_devices.py" --repo /path/to/handrail
```

It has the same strict behavior: exits non-zero when no physical install-ready iPhone or iPad is present. It does not boot simulators, does not choose unavailable devices, does not launch the app after install, and does not create GitHub releases.

## Grok Usage Notes

- This is a highly environment-specific skill (macOS + Xcode + physical Apple devices + the exact Handrail repo layout).
- Invoke via `run_terminal_cmd`. The output of the script is the primary deliverable.
- Because the work mutates a live iOS project and talks to physical hardware, always confirm with the user before running.

## Boundaries (strict — preserved)

- The script intentionally fails when no suitable physical devices are connected.
- No simulator support.
- No automatic fallback or retry loops invented by the agent.
- The repository's own release script is the source of truth for the full flow.

## Success Criteria

- The exact devices that received the build are listed with their names and types.
- Any skipped devices have the precise reason the script emitted.
- The version/build metadata in the installed app matches what the release script produced.
- No simulators were used, no unavailable devices were forced.

This port keeps the original's "do not hand-write parallel sequences" discipline and ships both the primary guidance and the supporting device script as real, runnable artifacts.
