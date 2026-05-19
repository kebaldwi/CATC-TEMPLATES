#!/usr/bin/env python3
# ============================================================================
# 7.0 - Build or Apply Switching Network Profiles
# ============================================================================
# Authors
# ============================================================================
# | Name            | Role                              | Contact              |
# |-----------------|-----------------------------------|----------------------|
# | Igor Manassypov | Systems Engineer                  | imanassy@cisco.com   |
# Copyright (c) 2024-2026 Cisco Systems, Inc. All rights reserved.
# ============================================================================
"""
Demonstrates:
  Build switching network profile payloads from settings.json
  Optionally POST payloads to a user-supplied endpoint

Why optional apply mode?
The workflow-manager endpoint used by the Ansible collection can vary by
Catalyst Center release. This script always builds deterministic payloads and
prints them. If you provide an endpoint path, it can submit them too.

Environment
-----------
  CATC_APPLY_NETWORK_PROFILE=false        # default: preview only
  CATC_NETWORK_PROFILE_ENDPOINT=...       # required when apply=true

Example endpoint value:
  /dna/intent/api/v1/network-profile/switching

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 network_profile.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "7.0"

DEFAULT_SETTINGS = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        "Projects",
        "BGP_EVPN",
        "Settings",
        "settings.json",
    )
)


def load_settings():
    path = os.getenv("CATC_SETTINGS_JSON", DEFAULT_SETTINGS)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    project = data.get("project", [])
    if not project:
        raise RuntimeError("settings.json has no project entries")
    return path, project


def site_name_from_entry(entry):
    parent = entry.get("HierarchyParent", "Global")
    area = entry.get("HierarchyArea")
    bldg = entry.get("HierarchyBldg")
    floor = entry.get("HierarchyFloor")

    if floor:
        return f"{parent}/{area}/{bldg}/{floor}"
    if bldg:
        return f"{parent}/{area}/{bldg}"
    if area:
        return f"{parent}/{area}"
    return parent


def build_profile_list(project):
    profiles = []
    for entry in project:
        np = entry.get("network_profile")
        if not np:
            continue

        profile_name = np.get("profile_name")
        if not profile_name:
            continue

        site_path = site_name_from_entry(entry)

        day_n = []
        for item in np.get("DayNTemplateNames", []):
            name = item.get("TemplateName")
            if name:
                day_n.append(name)

        day_0 = []
        for item in np.get("Day0TemplateNames", []):
            name = item.get("TemplateName")
            if name:
                day_0.append(name)

        cfg = {
            "profile_name": profile_name,
            "site_names": [site_path],
        }
        if day_n:
            cfg["day_n_templates"] = day_n
        if day_0:
            cfg["onboarding_templates"] = day_0

        profiles.append(cfg)

    return profiles


def maybe_apply_profiles(token, profiles):
    apply_enabled = os.getenv("CATC_APPLY_NETWORK_PROFILE", "false").lower() == "true"
    endpoint = os.getenv("CATC_NETWORK_PROFILE_ENDPOINT", "").strip()

    if not apply_enabled:
        print("\n  Apply mode disabled (CATC_APPLY_NETWORK_PROFILE=false).")
        print("  Preview complete; no API changes were made.")
        return

    if not endpoint:
        raise RuntimeError(
            "CATC_APPLY_NETWORK_PROFILE is true but CATC_NETWORK_PROFILE_ENDPOINT is not set"
        )

    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    body = {"config": profiles, "state": "merged"}
    print(f"\n  POST {endpoint}")
    resp = helpers.http(
        "POST",
        f"{helpers.BASE_URL}{endpoint}",
        token=token,
        body=body,
    )

    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label="network profile")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Build or Apply Switching Network Profiles")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    profiles = build_profile_list(project)
    if not profiles:
        raise RuntimeError("No entries with network_profile were found")

    print(f"\n  Profiles built: {len(profiles)}")
    print("  Payload preview:")
    print(json.dumps(profiles, indent=2))

    token = helpers.get_token()
    maybe_apply_profiles(token, profiles)

    print("\n  Next step -> 8.0-Cisco-Catalyst-Center-Provision-Devices/")
    print()


if __name__ == "__main__":
    main()
