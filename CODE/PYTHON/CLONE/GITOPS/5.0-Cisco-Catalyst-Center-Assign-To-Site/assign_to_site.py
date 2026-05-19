#!/usr/bin/env python3
# ============================================================================
# 5.0 - Assign Devices to Site
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
  GET /dna/intent/api/v1/site
  PUT /dna/intent/api/v1/site/<siteId>/device
  GET /api/v1/task/<taskId>

Groups settings.json device_list entries by target hierarchy path and assigns
those devices to each site UUID.

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 assign_to_site.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "5.0"

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


def build_site_device_map(project):
    mapping = {}
    for entry in project:
        raw = entry.get("device_list")
        if not raw:
            continue
        site = site_name_from_entry(entry)
        ips = [ip.strip() for ip in raw.split(",") if ip.strip()]
        mapping.setdefault(site, [])
        mapping[site].extend(ips)

    for site in mapping:
        mapping[site] = sorted(set(mapping[site]))
    return mapping


def fetch_site_map(token):
    resp = helpers.http("GET", f"{helpers.BASE_URL}/dna/intent/api/v1/site", token=token)
    result = {}
    for site in resp.get("response", []):
        hierarchy = site.get("nameHierarchy")
        if hierarchy:
            result[hierarchy] = site.get("id")
    return result


def assign_devices(token, site_name, site_id, ips):
    payload = {"device": [{"ip": ip} for ip in ips]}
    print(f"  PUT /site/{site_id}/device  -> {site_name} ({len(ips)} devices)")
    resp = helpers.http(
        "PUT",
        f"{helpers.BASE_URL}/dna/intent/api/v1/site/{site_id}/device",
        token=token,
        body=payload,
    )
    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label=f"assign {site_name}")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Assign Devices to Site")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    site_device_map = build_site_device_map(project)
    if not site_device_map:
        raise RuntimeError("No entries with device_list were found")

    token = helpers.get_token()
    site_map = fetch_site_map(token)

    total = 0
    for site_name, ips in site_device_map.items():
        site_id = site_map.get(site_name)
        if not site_id:
            raise RuntimeError(f"Site not found in Catalyst Center: {site_name}")
        assign_devices(token, site_name, site_id, ips)
        total += len(ips)

    print(f"\n  Sites processed: {len(site_device_map)}")
    print(f"  Devices assigned: {total}")
    print("\n  Next step -> 6.1-Cisco-Catalyst-Center-Templates-Authenticate/")
    print()


if __name__ == "__main__":
    main()
