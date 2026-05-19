#!/usr/bin/env python3
# ============================================================================
# 8.0 - Provision Devices to Site
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
  GET /dna/intent/api/v1/network-device?managementIpAddress=<ip>
  GET /dna/intent/api/v1/sda/provisionDevices?siteId=<uuid>&limit=500
  POST /dna/intent/api/v1/sda/provisionDevices   (new devices)
  PUT  /dna/intent/api/v1/sda/provisionDevices   (already provisioned + force)
  GET  /api/v1/task/<taskId>                      (async task polling)

Reads device_list entries from settings.json, groups them by site hierarchy
path, and provisions each device to its target site.

Idempotency
-----------
  - Devices not yet provisioned at a site → POST
  - Already provisioned, CATC_FORCE_REPROVISION=false (default) → skipped
  - Already provisioned, CATC_FORCE_REPROVISION=true  → PUT (re-provision)

Environment
-----------
  CATC_HOST=198.18.129.100
  CATC_USERNAME=admin
  CATC_PASSWORD=<password>
  CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  CATC_FORCE_REPROVISION=false                           # default: skip
  DEBUG=false                                            # extra output

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  python3 provision_devices.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "8.0"

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

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
FORCE_REPROVISION = os.getenv("CATC_FORCE_REPROVISION", "false").lower() == "true"

PROVISION_API = f"{helpers.BASE_URL}/dna/intent/api/v1/sda/provisionDevices"
SITE_API      = f"{helpers.BASE_URL}/dna/intent/api/v1/site"
DEVICE_API    = f"{helpers.BASE_URL}/dna/intent/api/v1/network-device"


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Input loading
# ─────────────────────────────────────────────────────────────────────────────

def load_settings():
    """Load and validate settings.json."""
    path = os.getenv("CATC_SETTINGS_JSON", DEFAULT_SETTINGS)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    project = data.get("project", [])
    if not project:
        raise RuntimeError("settings.json has no project entries")
    return path, project


def site_name_from_entry(entry):
    """Reconstruct the full CatC hierarchy path from a settings.json entry."""
    parent = entry.get("HierarchyParent", "Global")
    area   = entry.get("HierarchyArea")
    bldg   = entry.get("HierarchyBldg")
    floor  = entry.get("HierarchyFloor")

    if floor:
        return f"{parent}/{area}/{bldg}/{floor}"
    if bldg:
        return f"{parent}/{area}/{bldg}"
    if area:
        return f"{parent}/{area}"
    return parent


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Build per-site device map
# ─────────────────────────────────────────────────────────────────────────────

def build_site_device_map(project):
    """
    Walk every settings.json entry that has a non-empty device_list and group
    management IPs by their target site path.

    Returns: { "<site/path>": ["ip1", "ip2", ...], ... }
    """
    mapping = {}
    for entry in project:
        raw = entry.get("device_list")
        if not raw:
            continue
        site = site_name_from_entry(entry)
        ips  = [ip.strip() for ip in raw.split(",") if ip.strip()]
        mapping.setdefault(site, [])
        mapping[site].extend(ips)

    # Deduplicate while preserving first-seen order per site
    for site in mapping:
        seen = set()
        deduped = []
        for ip in mapping[site]:
            if ip not in seen:
                seen.add(ip)
                deduped.append(ip)
        mapping[site] = deduped

    return mapping


# ─────────────────────────────────────────────────────────────────────────────
# Step 3a — Resolve site UUID
# ─────────────────────────────────────────────────────────────────────────────

def resolve_site_uuid(token, site_path):
    """
    GET /dna/intent/api/v1/site?name=<path>

    The 'name' parameter accepts the full slash-delimited hierarchy path.
    Returns the UUID of the first matching site entry.
    """
    import urllib.parse
    url  = f"{SITE_API}?name={urllib.parse.quote(site_path, safe='')}"
    resp = helpers.http("GET", url, token=token)
    entries = resp.get("response", [])
    if not entries:
        raise RuntimeError(
            f"Site '{site_path}' not found in Catalyst Center. "
            "Ensure the site hierarchy was created by playbook 1.0 first."
        )
    return entries[0]["id"]


# ─────────────────────────────────────────────────────────────────────────────
# Step 3b — Resolve device UUIDs
# ─────────────────────────────────────────────────────────────────────────────

def resolve_device_uuids(token, ips):
    """
    GET /dna/intent/api/v1/network-device?managementIpAddress=<ip>

    Returns: { "<ip>": {"uuid": "<id>", "hostname": "<name>"}, ... }
    """
    device_map = {}
    for ip in ips:
        url  = f"{DEVICE_API}?managementIpAddress={ip}"
        resp = helpers.http("GET", url, token=token)
        devices = resp.get("response", [])
        if not devices:
            raise RuntimeError(
                f"Device '{ip}' not found in Catalyst Center inventory. "
                "Ensure device discovery (playbook 4.0) completed successfully."
            )
        d = devices[0]
        device_map[ip] = {
            "uuid":     d["id"],
            "hostname": d.get("hostname", ip),
        }
        if DEBUG:
            print(f"    [device] {ip} → {d['id']}  ({d.get('hostname', '')})")
    return device_map


# ─────────────────────────────────────────────────────────────────────────────
# Step 3c — Fetch already-provisioned devices
# ─────────────────────────────────────────────────────────────────────────────

def fetch_provisioned_devices(token, site_uuid):
    """
    GET /dna/intent/api/v1/sda/provisionDevices?siteId=<uuid>&limit=500

    Returns two structures:
      - provisioned_ids  : set of device UUIDs already provisioned at this site
      - record_id_map    : { networkDeviceId: provisionRecord.id }
                           needed for PUT (re-provision) payloads
    """
    url  = f"{PROVISION_API}?siteId={site_uuid}&limit=500"
    resp = helpers.http("GET", url, token=token)
    records = resp.get("response", [])

    provisioned_ids = {r["networkDeviceId"] for r in records}
    record_id_map   = {r["networkDeviceId"]: r["id"] for r in records}
    return provisioned_ids, record_id_map


# ─────────────────────────────────────────────────────────────────────────────
# Step 3d — Submit provision requests
# ─────────────────────────────────────────────────────────────────────────────

def submit_provision(token, site_path, site_uuid, ips, device_map,
                     provisioned_ids, record_id_map):
    """
    Build POST (new) and PUT (re-provision) payloads based on the current
    provisioned state, submit them, and return the parent task IDs.

    CatC returns NCHS20405 if POST is used on an already-provisioned device —
    the Ansible playbook uses PUT for those cases (force_reprovision=true).
    """
    post_payload = []
    put_payload  = []
    skipped_ips  = []

    for ip in ips:
        d = device_map[ip]
        if d["uuid"] not in provisioned_ids:
            post_payload.append({"networkDeviceId": d["uuid"], "siteId": site_uuid})
        elif FORCE_REPROVISION:
            put_payload.append({
                "id":              record_id_map[d["uuid"]],
                "networkDeviceId": d["uuid"],
                "siteId":          site_uuid,
            })
        else:
            skipped_ips.append(ip)

    if skipped_ips:
        print(f"  Skipping {len(skipped_ips)} already-provisioned device(s) "
              f"(set CATC_FORCE_REPROVISION=true to override): "
              f"{', '.join(skipped_ips)}")

    if DEBUG:
        print(f"  POST payload: {json.dumps(post_payload, indent=2)}")
        print(f"  PUT  payload: {json.dumps(put_payload,  indent=2)}")

    post_task_id = ""
    put_task_id  = ""

    if post_payload:
        print(f"  POST {PROVISION_API}  ({len(post_payload)} device(s))")
        r = helpers.http("POST", PROVISION_API, token=token, body=post_payload)
        post_task_id = r.get("response", {}).get("taskId", "")
        if not post_task_id:
            raise RuntimeError(
                f"No taskId returned from POST provisionDevices for site '{site_path}'"
            )

    if put_payload:
        print(f"  PUT  {PROVISION_API}  ({len(put_payload)} device(s))")
        r = helpers.http("PUT", PROVISION_API, token=token, body=put_payload)
        put_task_id = r.get("response", {}).get("taskId", "")
        if not put_task_id:
            raise RuntimeError(
                f"No taskId returned from PUT provisionDevices for site '{site_path}'"
            )

    return post_task_id, put_task_id, post_payload, put_payload, skipped_ips


# ─────────────────────────────────────────────────────────────────────────────
# Step 3e — Poll parent tasks and fetch child task results
# ─────────────────────────────────────────────────────────────────────────────

def poll_provision_task(token, task_id, label):
    """
    Poll a single provision parent task until it finishes.

    Unlike the generic helpers.poll_task, CatC provisioning tasks remain
    'in progress' for extended periods — wait for endTime to be set rather
    than relying on a specific progress keyword.

    Returns the final task 'response' dict.
    """
    url = f"{helpers.TASK_API}/{task_id}"
    for attempt in range(1, helpers.POLL_RETRIES + 1):
        resp     = helpers.http("GET", url, token=token)
        result   = resp.get("response", {})
        is_error = result.get("isError", False)
        has_end  = bool(result.get("endTime"))
        progress = result.get("progress", "")

        if is_error:
            fr = result.get("failureReason", progress)
            raise RuntimeError(f"Provision task '{label}' failed — {fr}")
        if has_end:
            print(f"    [{label}] Complete ✓  {progress[:120]}")
            return result

        print(f"    [{label}] [{attempt}/{helpers.POLL_RETRIES}]  {progress[:80]}")
        time.sleep(helpers.POLL_DELAY_SEC)

    raise RuntimeError(
        f"Provision task '{label}' did not complete within "
        f"{helpers.POLL_RETRIES * helpers.POLL_DELAY_SEC}s"
    )


def extract_child_task_ids(progress):
    """
    The parent task progress field embeds child task IDs as semicolon-separated
    tokens.  Extract any token that looks like a UUID (8-4-4-4-12 format).

    Example progress:
      "Provisioning Devices\\nStatus: successful\\n2 child operation(s)\\n
       abc1-...-def;abc2-...-ghi"
    """
    ids = []
    for token in progress.split(";"):
        t = token.strip()
        # A UUID is exactly 36 characters with hyphens at positions 8, 13, 18, 23
        candidate = t[-36:] if len(t) > 36 else t
        if (len(candidate) == 36
                and candidate[8] == "-"
                and candidate[13] == "-"
                and candidate[18] == "-"
                and candidate[23] == "-"):
            ids.append(candidate)
    return ids


def fetch_child_tasks(token, task_id):
    """Query child task IDs embedded in a parent provision task's progress."""
    url    = f"{helpers.TASK_API}/{task_id}"
    resp   = helpers.http("GET", url, token=token)
    result = resp.get("response", {})
    return extract_child_task_ids(result.get("progress", ""))


def report_child_tasks(token, child_ids, label):
    """Fetch and print each child task result."""
    if not child_ids:
        return
    print(f"\n  ── Child task results ({len(child_ids)} device(s)) [{label}] ──")
    for i, cid in enumerate(child_ids, 1):
        url    = f"{helpers.TASK_API}/{cid}"
        resp   = helpers.http("GET", url, token=token)
        result = resp.get("response", {})
        status = "FAILURE" if result.get("isError") else "SUCCESS"
        detail = (result.get("failureReason") or result.get("progress", ""))
        detail = detail.replace("\\n", " | ")[:120]
        print(f"  [{i}/{len(child_ids)}] taskId: {cid} | {status} | {detail}")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — Process one site
# ─────────────────────────────────────────────────────────────────────────────

def provision_site(token, site_path, ips):
    """
    Full provisioning workflow for a single site:
      a. Resolve site UUID
      b. Resolve device UUIDs
      c. Check already-provisioned state
      d. Build POST / PUT payloads (idempotency)
      e. Submit requests and collect task IDs
      f. Poll parent tasks to completion
      g. Report per-device child task results
    """
    print(f"\n  ── Site: {site_path} ({len(ips)} device(s)) ──")

    # a. Site UUID
    site_uuid = resolve_site_uuid(token, site_path)
    if DEBUG:
        print(f"  Site UUID: {site_uuid}")

    # b. Device UUIDs
    print(f"  Resolving UUIDs for: {', '.join(ips)}")
    device_map = resolve_device_uuids(token, ips)

    # c. Already-provisioned check
    provisioned_ids, record_id_map = fetch_provisioned_devices(token, site_uuid)
    if DEBUG:
        print(f"  Already provisioned ({len(provisioned_ids)}): {sorted(provisioned_ids)}")

    # d / e. Build payloads and submit
    post_task_id, put_task_id, post_payload, put_payload, skipped = submit_provision(
        token, site_path, site_uuid, ips, device_map, provisioned_ids, record_id_map
    )

    any_submitted = bool(post_task_id or put_task_id)

    if not any_submitted:
        print(f"  Status: SKIPPED — all {len(ips)} device(s) already provisioned at this site")
        return len(skipped), 0, 0

    # f. Poll parent tasks
    if post_task_id:
        post_result = poll_provision_task(token, post_task_id, label="POST provision")
        child_ids   = extract_child_task_ids(post_result.get("progress", ""))
        report_child_tasks(token, child_ids, label="POST")

    if put_task_id:
        put_result  = poll_provision_task(token, put_task_id, label="PUT re-provision")
        child_ids   = extract_child_task_ids(put_result.get("progress", ""))
        report_child_tasks(token, child_ids, label="PUT")

    return len(skipped), len(post_payload), len(put_payload)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Provision Devices to Site")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON : {settings_path}")
    print(f"  Force reprov  : {FORCE_REPROVISION}")

    # Build { site_path: [ip, ...] }
    site_device_map = build_site_device_map(project)
    if not site_device_map:
        raise RuntimeError("No entries with device_list were found in settings.json")

    total_devices  = sum(len(v) for v in site_device_map.values())
    print(f"  Sites found   : {len(site_device_map)}")
    print(f"  Devices total : {total_devices}")
    for site, ips in site_device_map.items():
        print(f"    {site}: {', '.join(ips)}")

    token = helpers.get_token()

    total_skipped = 0
    total_post    = 0
    total_put     = 0

    for site_path, ips in site_device_map.items():
        skipped, posted, put = provision_site(token, site_path, ips)
        total_skipped += skipped
        total_post    += posted
        total_put     += put

    print(f"\n{'=' * 60}")
    print(f"  Summary")
    print(f"{'=' * 60}")
    print(f"  Sites processed    : {len(site_device_map)}")
    print(f"  Newly provisioned  : {total_post}")
    print(f"  Re-provisioned     : {total_put}")
    print(f"  Skipped (existing) : {total_skipped}")
    print()
    print("  Next step -> 9.0-Cisco-Catalyst-Center-Provision-Deploy-Composite/")
    print()


if __name__ == "__main__":
    main()
