#!/usr/bin/env python3
# ============================================================================
# 4.0 - Run Device Discovery
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
  POST /dna/intent/api/v1/discovery
  GET  /api/v1/task/<taskId>

Builds discovery requests from settings.json device_list entries and submits one
job per site path.

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 device_discovery.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "4.0"

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


def build_discovery_jobs(project):
    jobs = []
    for entry in project:
        raw = entry.get("device_list")
        if not raw:
            continue

        ips = [ip.strip() for ip in raw.split(",") if ip.strip()]
        if not ips:
            continue

        site = site_name_from_entry(entry)
        jobs.append(
            {
                "name": site,
                "discoveryType": "MULTI RANGE",
                "ipAddressList": ips,
                "protocolOrder": "ssh",
                "retry": 5,
                "timeout": 3,
                "preferredMgmtIpMethod": "UseLoopBack",
                "globalCredential": {
                    "cliCredential": [{"description": "CLI-net-admin", "username": "net-admin"}],
                    "snmpV2Read": [{"description": "RO"}],
                    "snmpV2Write": [{"description": "RW"}],
                    "netconf": [{"description": "NETCONF-netadmin"}],
                },
            }
        )
    return jobs


def submit_discovery(token, job):
    print(f"  POST /discovery  -> {job['name']} ({len(job['ipAddressList'])} IPs)")
    resp = helpers.http(
        "POST",
        f"{helpers.BASE_URL}/dna/intent/api/v1/discovery",
        token=token,
        body=job,
    )
    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label=f"discovery {job['name']}")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Run Catalyst Center Device Discovery")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    jobs = build_discovery_jobs(project)
    if not jobs:
        raise RuntimeError("No entries with device_list were found")

    token = helpers.get_token()

    for job in jobs:
        submit_discovery(token, job)

    total_devices = sum(len(j["ipAddressList"]) for j in jobs)
    print(f"\n  Discovery jobs submitted: {len(jobs)}")
    print(f"  Total target IPs: {total_devices}")
    print("\n  Next step -> 5.0-Cisco-Catalyst-Center-Assign-To-Site/")
    print()


if __name__ == "__main__":
    main()
