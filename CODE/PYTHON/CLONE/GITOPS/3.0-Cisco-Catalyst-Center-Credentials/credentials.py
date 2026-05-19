#!/usr/bin/env python3
# ============================================================================
# 3.0 - Configure Global Credentials
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
  GET  /dna/intent/api/v1/global-credential?credentialSubType=<type>
  POST /dna/intent/api/v1/global-credential/<credential-type-endpoint>
  GET  /api/v1/task/<taskId>

Creates missing global credentials from settings.json for:
- CLI
- SNMPv2 read
- SNMPv2 write
- NETCONF

The script is idempotent by credential description.

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 credentials.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "3.0"

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

CREDENTIAL_MODELS = {
    "cli_credential": {
        "subtype": "CLI",
        "endpoint": "cli",
        "description_key": "description",
        "build": lambda c: {
            "description": c["description"],
            "username": c["username"],
            "password": c["password"],
            "enablePassword": c.get("enable_password") or c["password"],
        },
    },
    "snmp_v2c_read": {
        "subtype": "SNMPV2_READ_COMMUNITY",
        "endpoint": "snmpv2-read-community",
        "description_key": "description",
        "build": lambda c: {
            "description": c["description"],
            "readCommunity": c["read_community"],
        },
    },
    "snmp_v2c_write": {
        "subtype": "SNMPV2_WRITE_COMMUNITY",
        "endpoint": "snmpv2-write-community",
        "description_key": "description",
        "build": lambda c: {
            "description": c["description"],
            "writeCommunity": c["write_community"],
        },
    },
    "netconf_credential": {
        "subtype": "NETCONF",
        "endpoint": "netconf",
        "description_key": "description",
        "build": lambda c: {
            "description": c["description"],
            "port": int(c.get("netconf_port", "830")),
        },
    },
}


def load_settings():
    path = os.getenv("CATC_SETTINGS_JSON", DEFAULT_SETTINGS)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    project = data.get("project", [])
    if not project:
        raise RuntimeError("settings.json has no project entries")
    return path, project


def collect_credentials(project):
    result = {k: [] for k in CREDENTIAL_MODELS}
    seen = {k: set() for k in CREDENTIAL_MODELS}

    for entry in project:
        dc = entry.get("device_credentials") or {}
        for key in CREDENTIAL_MODELS:
            item = dc.get(key)
            if not item:
                continue
            desc = item.get("description")
            if not desc or desc in seen[key]:
                continue
            seen[key].add(desc)
            result[key].append(item)
    return result


def existing_descriptions(token, subtype):
    url = f"{helpers.BASE_URL}/dna/intent/api/v1/global-credential?credentialSubType={subtype}"
    resp = helpers.http("GET", url, token=token)
    names = set()
    for item in resp.get("response", []):
        desc = item.get("description")
        if desc:
            names.add(desc)
    return names


def create_credential(token, endpoint_suffix, payload, label):
    url = f"{helpers.BASE_URL}/dna/intent/api/v1/global-credential/{endpoint_suffix}"
    print(f"  POST /global-credential/{endpoint_suffix}  -> {label}")
    resp = helpers.http("POST", url, token=token, body=payload)
    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label=f"credential {label}")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Configure Catalyst Center Global Credentials")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    token = helpers.get_token()
    grouped = collect_credentials(project)

    created = 0
    skipped = 0

    for key, model in CREDENTIAL_MODELS.items():
        candidates = grouped[key]
        if not candidates:
            continue

        existing = existing_descriptions(token, model["subtype"])
        for item in candidates:
            description = item[model["description_key"]]
            if description in existing:
                print(f"  SKIP {key} -> {description} (already exists)")
                skipped += 1
                continue

            payload = model["build"](item)
            create_credential(token, model["endpoint"], payload, description)
            created += 1

    print(f"\n  Credentials created: {created}")
    print(f"  Credentials skipped: {skipped}")
    print("\n  Next step -> 4.0-Cisco-Catalyst-Center-Device-Discovery/")
    print()


if __name__ == "__main__":
    main()
