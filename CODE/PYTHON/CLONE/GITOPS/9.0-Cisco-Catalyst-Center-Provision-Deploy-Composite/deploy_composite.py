#!/usr/bin/env python3
# ============================================================================
# 8.0 — Deploy a Composite Template
# ============================================================================
# Authors
# ============================================================================
# | Name            | Role                              | Contact              |
# |-----------------|-----------------------------------|----------------------|
# | Igor Manassypov | Systems Engineer                  | imanassy@cisco.com   |
# Copyright © 2024-2026 Cisco Systems, Inc. All rights reserved.
# ============================================================================
"""
Demonstrates:
  GET  /dna/intent/api/v1/template-programmer/template?projectNames=<name>
  GET  /dna/intent/api/v1/template-programmer/template/<rootId>
  GET  /dna/intent/api/v1/network-device?managementIpAddress=<ip>
  POST /dna/intent/api/v2/template-programmer/template/deploy
  GET  /api/v1/task/<taskId>

Deploy payload rules
────────────────────
The CatC v2 deploy API (TemplateDeploymentInfo DTO) accepts exactly 8 fields:
  templateId                     — composite VERSION UUID (latest committed snapshot)
  mainTemplateId                 — composite ROOT UUID    (permanent, never changes)
  isComposite                    — true
  copyingConfig                  — true  ← push rendered config to device NOW
  forcePushTemplate              — true  ← deploy even if CatC considers device current
  targetInfo                     — list of device target entries (MUST be here)
  memberTemplateDeploymentInfo   — per-member deploy specs (each with own targetInfo)
  responseMsg                    — (optional, informational)

targetInfo structure (ResourceParam schema):
  Each entry contains resourceParams with three RUNTIME-scoped entries so CatC
  can identify the device by UUID, IP, or hostname at deploy time:
    [{type: MANAGED_DEVICE_UUID,     value: <uuid>,     scope: RUNTIME},
     {type: MANAGED_DEVICE_IP,       value: <mgmt_ip>,  scope: RUNTIME},
     {type: MANAGED_DEVICE_HOSTNAME, value: <hostname>, scope: RUNTIME}]

Critical notes
──────────────
  • copyingConfig=true MUST appear at both the composite level AND inside each
    member entry — without it CatC accepts the deploy but never pushes config.

  • targetInfo MUST appear at the composite level — without it CatC returns:
    NCTP10028 "At least one device should data should be provided"

  • The Cisco DNAC Ansible/SDK module cannot send copyingConfig=true at the
    top level — it silently drops the field.  Always use direct REST calls.

  • versionsInfo is returned by CatC in RANDOM order — sort by versionTime
    (Unix-millisecond timestamp) descending to select the latest version.

  • On CatC 2.3.7.9 the task progress string contains the deployment result:
    "Template Deployemnt Id: <id> | failureReason: <reason>"
    (CatC's own typo: "Deployemnt").  Empty failureReason = SUCCESS.

Requires: Steps 6.3 and 6.4 to have run first.

Usage
─────
  export CATC_HOST=198.18.129.100
  export CATC_PASSWORD=<password>
  export CATC_DEVICE_IP=198.19.1.1
  python3 deploy_composite.py
"""

import json
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "8.0"


# ─────────────────────────────────────────────────────────────────────────────
# Template ID resolution
# ─────────────────────────────────────────────────────────────────────────────

def build_template_version_map(token):
    """
    Fetch all templates in the project and build a name → {rootId, versionId} map.

    versionsInfo is returned by CatC in RANDOM order.  Sorting by versionTime
    (Unix-millisecond timestamp) descending selects the latest committed version.

    Returns
    -------
    dict  {template_name: {"rootId": str, "versionId": str}, ...}
    """
    resp = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/template?projectNames={helpers.PROJECT_NAME}",
        token=token,
    )
    version_map = {}
    for tpl in (resp if isinstance(resp, list) else []):
        root_id  = tpl["templateId"]
        versions = sorted(
            tpl.get("versionsInfo", []),
            key=lambda v: v.get("versionTime", 0),
            reverse=True,
        )
        version_id = versions[0]["id"] if versions else root_id
        version_map[tpl["name"]] = {"rootId": root_id, "versionId": version_id}
    return version_map


# ─────────────────────────────────────────────────────────────────────────────
# Device resolution
# ─────────────────────────────────────────────────────────────────────────────

def resolve_device(token, mgmt_ip):
    """
    GET /dna/intent/api/v1/network-device?managementIpAddress=<ip>

    Returns (device_uuid, hostname).
    The device must be discovered and managed by Catalyst Center.
    """
    print(f"\n  GET /network-device?managementIpAddress={mgmt_ip}")
    resp    = helpers.http(
        "GET",
        f"{helpers.DEVICE_API}?managementIpAddress={mgmt_ip}",
        token=token,
    )
    devices = resp.get("response", [])
    if not devices:
        raise RuntimeError(
            f"No managed device found for IP {mgmt_ip}.\n"
            "Ensure the device is discovered in Catalyst Center before deploying."
        )
    device   = devices[0]
    uuid     = device["id"]
    hostname = device.get("hostname", mgmt_ip)
    print(f"  ↳ hostname: {hostname}   uuid: {uuid}")
    return uuid, hostname


# ─────────────────────────────────────────────────────────────────────────────
# Deploy payload helpers
# ─────────────────────────────────────────────────────────────────────────────

def _target_info(device_uuid, device_ip, hostname):
    """
    Build a single targetInfo entry for the deploy payload.

    resourceParams carries three RUNTIME-scoped entries so CatC can resolve
    the device at deploy time using any of its identifiers.
    Structure matches References/task-composite-submission-request.json.
    """
    return {
        "hostName": hostname,
        "id":       device_uuid,
        "params":   {},
        "type":     "MANAGED_DEVICE_UUID",
        "resourceParams": [
            {"scope": "RUNTIME", "type": "MANAGED_DEVICE_UUID",     "value": device_uuid},
            {"scope": "RUNTIME", "type": "MANAGED_DEVICE_IP",       "value": device_ip},
            {"scope": "RUNTIME", "type": "MANAGED_DEVICE_HOSTNAME", "value": hostname},
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Deploy
# ─────────────────────────────────────────────────────────────────────────────

def deploy_composite(token, version_map, device_uuid, device_ip, hostname):
    """
    POST /dna/intent/api/v2/template-programmer/template/deploy

    Submits the composite deploy payload and returns the CatC task ID.
    """
    composite_root_id    = version_map[helpers.COMPOSITE_NAME]["rootId"]
    composite_version_id = version_map[helpers.COMPOSITE_NAME]["versionId"]
    member_root_id       = version_map[helpers.MEMBER_NAME]["rootId"]
    member_version_id    = version_map[helpers.MEMBER_NAME]["versionId"]

    target = _target_info(device_uuid, device_ip, hostname)

    payload = {
        # ── Composite-level fields ─────────────────────────────────────────
        "copyingConfig":     True,   # push rendered config to device NOW
        "forcePushTemplate": True,   # deploy even if CatC thinks device is current
        "isComposite":       True,
        "mainTemplateId":    composite_root_id,    # permanent root UUID
        "templateId":        composite_version_id, # latest version UUID
        # targetInfo MUST appear here — not just inside memberTemplateDeploymentInfo
        "targetInfo":        [target],
        # ── Member-level fields ────────────────────────────────────────────
        "memberTemplateDeploymentInfo": [
            {
                "copyingConfig":     True,   # required here too
                "forcePushTemplate": True,
                "isComposite":       False,
                "mainTemplateId":    member_root_id,
                "templateId":        member_version_id,
                "targetInfo":        [target],
            }
        ],
    }

    print(f"\n  POST /dna/intent/api/v2/template-programmer/template/deploy")
    print(f"  Payload:\n{json.dumps(payload, indent=4)}")

    resp    = helpers.http("POST", helpers.DEPLOY_API_V2, token=token, body=payload)
    task_id = resp.get("response", {}).get("taskId")
    if not task_id:
        raise RuntimeError(f"Deploy did not return a taskId: {resp}")
    print(f"\n  ↳ Accepted — taskId: {task_id}")
    return task_id


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print(f"  {STEP} — Deploy Composite Template")
    print(f"  Host     : {helpers.CATC_HOST}:{helpers.CATC_PORT}")
    print(f"  Project  : {helpers.PROJECT_NAME}")
    print(f"  Composite: {helpers.COMPOSITE_NAME}")
    print(f"  Device   : {helpers.TARGET_DEVICE_IP}")
    print(f"{'='*60}\n")

    token = helpers.get_token()

    # ── Step 7a: build template version map ──────────────────────────────────
    print("[Step 7a] Resolve template IDs from project")
    print(f"  GET /template-programmer/template?projectNames={helpers.PROJECT_NAME}")
    version_map = build_template_version_map(token)

    for name in (helpers.COMPOSITE_NAME, helpers.MEMBER_NAME):
        if name not in version_map:
            raise RuntimeError(
                f"Template '{name}' not found in project '{helpers.PROJECT_NAME}'.\n"
                "Ensure steps 6.3 and 6.4 have been run first."
            )
        m = version_map[name]
        print(f"  ↳ {name}")
        print(f"     mainTemplateId (root):    {m['rootId']}")
        print(f"     templateId (version):     {m['versionId']}")

    # ── Step 7b: verify containingTemplates ──────────────────────────────────
    composite_root_id = version_map[helpers.COMPOSITE_NAME]["rootId"]
    print(f"\n[Step 7b] Verify composite containingTemplates list")
    print(f"  GET /template-programmer/template/{composite_root_id}")
    detail  = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/template/{composite_root_id}",
        token=token,
    )
    members = detail.get("containingTemplates", [])
    print(f"  ↳ containingTemplates: {[m.get('name', m.get('id', '?')) for m in members]}")

    # ── Step 7c: resolve target device ───────────────────────────────────────
    print(f"\n[Step 7c] Resolve device UUID by management IP")
    device_uuid, hostname = resolve_device(token, helpers.TARGET_DEVICE_IP)

    # ── Step 8: build and submit deploy payload ───────────────────────────────
    print(f"\n[Step 8] Submit composite deploy payload")
    task_id = deploy_composite(token, version_map, device_uuid, helpers.TARGET_DEVICE_IP, hostname)

    # ── Step 9: poll task until complete ─────────────────────────────────────
    print(f"\n[Step 9] Poll deployment task")
    print(f"  GET /api/v1/task/{task_id}")
    result = helpers.poll_task(token, task_id, label="deploy")

    # Parse deployment result from task progress string.
    # CatC 2.3.7.9 format: "Template Deployemnt Id: <id> | failureReason: <reason>"
    # (Note CatC's own typo: "Deployemnt" not "Deployment")
    progress       = result.get("progress", "")
    fr_match       = re.search(r"\| failureReason: (.*)$", progress)
    failure_reason = fr_match.group(1).strip() if fr_match else ""
    deploy_result  = "SUCCESS ✓" if not failure_reason else f"FAILURE ✗  {failure_reason}"

    print(f"\n{'='*60}")
    print(f"  {STEP} — Deploy Composite Template — Complete")
    print(f"  Result  : {deploy_result}")
    print(f"  Device  : {helpers.TARGET_DEVICE_IP} ({hostname})")
    print(f"  Progress: {progress[:300]}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
