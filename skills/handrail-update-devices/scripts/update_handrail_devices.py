#!/usr/bin/env python3
"""
update_handrail_devices.py — Grok-ported helper for building & installing Handrail on physical iOS devices.

Original: ~/.codex/skills/handrail-update-devices/scripts/update_handrail_devices.py
Part of the "handrail-update-devices" Codex skill.

This script is very specific to the Handrail project and a macOS development machine with:
- Xcode + Command Line Tools
- Physical iPhone/iPad devices connected and trusted
- The Handrail repo at a known location

It is **not** a general-purpose iOS deploy tool.

Grok invocation: via run_terminal_cmd. The script intentionally exits non-zero when no install-ready physical devices are found.

Key behaviors preserved:
- Uses xcrun devicectl for device discovery and app install (no simulators).
- Bumps version/build metadata? (see note below)
- Builds with xcodebuild for generic iOS.
- Installs the .app to every qualifying physical device.

NOTE: The primary contract in the skill SKILL.md directs the agent to use the *repository's own* release script
(/Users/velocityworks/IdeaProjects/handrail/tools/release/update_ios_release.py) for the full release + tag + GitHub release flow.
This script is a supporting/legacy implementation focused on the device update portion.

Adapted for Grok: helpful error messages, /tmp paths under a grok- prefix where possible, clear documentation.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# Original temp locations preserved for compatibility with any external tooling that might watch them.
# In a pure Grok port one could namespace under /tmp/grok-handrail-*, but we keep the original names
# so behavior is identical for the Handrail project.
DERIVED_DATA = Path("/tmp/handrail-device-update-derived-data")
DEVICE_LIST_JSON = Path("/tmp/handrail-device-update-devices.json")
INSTALL_APP_FEATURE = "com.apple.coredevice.feature.installapp"
SUPPORTED_DEVICE_TYPES = {"iPhone", "iPad"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and install Handrail on connected physical iPhone/iPad devices.")
    parser.add_argument("--repo", default="/Users/velocityworks/IdeaProjects/handrail", help="Path to the Handrail repository.")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    project = repo / "ios" / "Handrail" / "Handrail.xcodeproj"
    if not project.exists():
        print(f"Handrail Xcode project not found: {project}", file=sys.stderr)
        return 1

    devices, skipped = installable_ios_devices()
    for device in skipped:
        print(f"Skipped {device['name']} ({device['device_type']}): {device['reason']}", file=sys.stderr)

    if not devices:
        print("No install-ready physical iPhone or iPad devices found.", file=sys.stderr)
        return 1

    build_app(repo, project)
    app = DERIVED_DATA / "Build" / "Products" / "Debug-iphoneos" / "Handrail.app"
    if not app.exists():
        print(f"Built app not found: {app}", file=sys.stderr)
        return 1

    for device in devices:
        install_app(device["identifier"], app)
        print(f"Updated {device['name']} ({device['device_type']})")

    return 0


def installable_ios_devices() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    run(["xcrun", "devicectl", "list", "devices", "--json-output", str(DEVICE_LIST_JSON), "--quiet"])
    with DEVICE_LIST_JSON.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    devices = []
    skipped = []
    for device in payload.get("result", {}).get("devices", []):
        hardware = device.get("hardwareProperties", {})
        device_type = hardware.get("deviceType")
        if hardware.get("platform") != "iOS" or device_type not in SUPPORTED_DEVICE_TYPES:
            continue
        if hardware.get("reality") and hardware.get("reality") != "physical":
            continue
        identifier = device.get("identifier")
        if not identifier:
            continue

        detail = device_details(identifier)
        ready_device, skip = installable_device_from_details(detail)
        if ready_device:
            devices.append(ready_device)
        else:
            skipped.append(skip)

    return (
        sorted(devices, key=lambda item: (item["device_type"], item["name"], item["identifier"])),
        sorted(skipped, key=lambda item: (item["device_type"], item["name"], item["identifier"])),
    )


def device_details(identifier: str) -> dict:
    details_json = Path(f"/tmp/handrail-device-update-details-{safe_name(identifier)}.json")
    run([
        "xcrun",
        "devicectl",
        "device",
        "info",
        "details",
        "--device",
        identifier,
        "--json-output",
        str(details_json),
        "--quiet",
    ])
    with details_json.open("r", encoding="utf-8") as handle:
        return json.load(handle).get("result", {})


def installable_device_from_details(device: dict) -> tuple[dict[str, str] | None, dict[str, str]]:
    hardware = device.get("hardwareProperties", {})
    connection = device.get("connectionProperties", {})
    properties = device.get("deviceProperties", {})
    capabilities = {
        capability.get("featureIdentifier")
        for capability in device.get("capabilities", [])
    }
    identifier = device.get("identifier", "")
    name = properties.get("name") or identifier or "unknown device"
    device_type = hardware.get("deviceType") or "unknown"

    result = {"identifier": identifier, "name": name, "device_type": device_type}
    if not identifier:
        return None, result | {"reason": "identifier is missing"}
    if hardware.get("platform") != "iOS" or device_type not in SUPPORTED_DEVICE_TYPES:
        return None, result | {"reason": "device is not an iPhone or iPad"}
    if connection.get("tunnelState") != "connected":
        return None, result | {"reason": f"tunnelState is {connection.get('tunnelState', 'missing')}"}
    if INSTALL_APP_FEATURE not in capabilities:
        return None, result | {"reason": "Install Application capability is not available"}

    return result, {}


def build_app(repo: Path, project: Path) -> None:
    run([
        "xcodebuild",
        "-project",
        str(project),
        "-scheme",
        "Handrail",
        "-configuration",
        "Debug",
        "-destination",
        "generic/platform=iOS",
        "-derivedDataPath",
        str(DERIVED_DATA),
        "-allowProvisioningUpdates",
        "build",
    ], cwd=repo)


def install_app(identifier: str, app: Path) -> None:
    install_json = Path(f"/tmp/handrail-device-update-install-{safe_name(identifier)}.json")
    run([
        "xcrun",
        "devicectl",
        "device",
        "install",
        "app",
        "--device",
        identifier,
        str(app),
        "--json-output",
        str(install_json),
        "--quiet",
    ])


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", value)


if __name__ == "__main__":
    raise SystemExit(main())
