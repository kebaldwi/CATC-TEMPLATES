#!/usr/bin/env python3
# ============================================================================
# 1.0 - Build Site Hierarchy
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
  GET  /dna/intent/api/v1/site
  POST /dna/intent/api/v1/site
  GET  /api/v1/task/<taskId>

Builds area/building/floor hierarchy from settings.json in parent-before-child order.
The script is idempotent: existing paths are skipped.

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 site_hierarchy.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "1.0"

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

DEFAULT_BUILDING_ADDRESS = "300 E Tasman Dr, Bldg 10, San Jose, CA 95134"
DEFAULT_FLOOR = {
    "rfModel": "Cubes And Walled Offices",
    "width": 100,
    "length": 100,
    "height": 10,
    "floorNumber": 1,
}


def load_settings():
    path = os.getenv("CATC_SETTINGS_JSON", DEFAULT_SETTINGS)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    project = data.get("project", [])
    if not project:
        raise RuntimeError("settings.json has no project entries")
    return path, project


def path_depth(path):
    return len([p for p in path.split("/") if p])


def synthesize_site_entries(project):
    entries = {}
    for item in project:
        parent = item.get("HierarchyParent", "Global")
        area = item.get("HierarchyArea")
        bldg = item.get("HierarchyBldg")
        floor = item.get("HierarchyFloor")

        if area:
            area_path = f"{parent}/{area}"
            entries.setdefault(area_path, {"siteType": "area"})

        if area and bldg:
            bldg_path = f"{parent}/{area}/{bldg}"
            entries.setdefault(
                bldg_path,
                {
                    "siteType": "building",
                    "address": item.get("HierarchyBldgAddress") or DEFAULT_BUILDING_ADDRESS,
                },
            )

        if area and bldg and floor:
            floor_path = f"{parent}/{area}/{bldg}/{floor}"
            entries.setdefault(floor_path, {"siteType": "floor", **DEFAULT_FLOOR})

    return entries


def expand_with_intermediate_paths(site_entries):
    expanded = {}
    for path, meta in site_entries.items():
        parts = [p for p in path.split("/") if p]
        for i in range(2, len(parts) + 1):
            sub = "/".join(parts[:i])
            if sub not in expanded:
                if sub in site_entries:
                    expanded[sub] = site_entries[sub]
                else:
                    depth = path_depth(sub)
                    expanded[sub] = {
                        "siteType": "area" if depth < 4 else "building",
                    }
    return dict(sorted(expanded.items(), key=lambda kv: path_depth(kv[0])))


def fetch_existing_sites(token):
    resp = helpers.http("GET", f"{helpers.BASE_URL}/dna/intent/api/v1/site", token=token)
    existing = set()
    for site in resp.get("response", []):
        hierarchy = site.get("nameHierarchy")
        if hierarchy:
            existing.add(hierarchy)
    existing.add("Global")
    return existing


def build_site_payload(path, metadata):
    parts = path.split("/")
    site_type = metadata["siteType"]
    parent = "/".join(parts[:-1])
    name = parts[-1]

    if site_type == "area":
        return {
            "type": "area",
            "site": {
                "area": {
                    "name": name,
                    "parentName": parent,
                }
            },
        }

    if site_type == "building":
        return {
            "type": "building",
            "site": {
                "building": {
                    "name": name,
                    "parentName": parent,
                    "address": metadata.get("address", DEFAULT_BUILDING_ADDRESS),
                }
            },
        }

    if site_type == "floor":
        return {
            "type": "floor",
            "site": {
                "floor": {
                    "name": name,
                    "parentName": parent,
                    "rfModel": metadata.get("rfModel", DEFAULT_FLOOR["rfModel"]),
                    "width": int(metadata.get("width", DEFAULT_FLOOR["width"])),
                    "length": int(metadata.get("length", DEFAULT_FLOOR["length"])),
                    "height": int(metadata.get("height", DEFAULT_FLOOR["height"])),
                    "floorNumber": int(
                        metadata.get("floorNumber", DEFAULT_FLOOR["floorNumber"])
                    ),
                }
            },
        }

    raise RuntimeError(f"Unsupported site type: {site_type}")


def create_site(token, path, metadata):
    payload = build_site_payload(path, metadata)
    print(f"  POST /site  -> {path} ({metadata['siteType']})")
    resp = helpers.http(
        "POST",
        f"{helpers.BASE_URL}/dna/intent/api/v1/site",
        token=token,
        body=payload,
    )
    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label=f"create {path}")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Build Catalyst Center Site Hierarchy")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    token = helpers.get_token()
    existing = fetch_existing_sites(token)

    source_entries = synthesize_site_entries(project)
    ordered_entries = expand_with_intermediate_paths(source_entries)

    print(f"\n  Planned hierarchy entries: {len(ordered_entries)}")

    created = 0
    skipped = 0
    for path, metadata in ordered_entries.items():
        if path in existing:
            print(f"  SKIP /site  -> {path} (already exists)")
            skipped += 1
            continue
        create_site(token, path, metadata)
        created += 1

    print(f"\n  Created: {created}")
    print(f"  Skipped: {skipped}")
    print("\n  Next step -> 2.0-Cisco-Catalyst-Center-Settings/")
    print()


if __name__ == "__main__":
    main()
