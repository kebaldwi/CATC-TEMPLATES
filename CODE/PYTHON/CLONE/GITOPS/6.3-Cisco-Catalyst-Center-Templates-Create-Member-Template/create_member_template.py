#!/usr/bin/env python3
# ============================================================================
# 6.3 — Create and Commit a Member Template
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
  POST /dna/intent/api/v1/template-programmer/project/<projectId>/template
  POST /dna/intent/api/v1/template-programmer/template/version   (commit)
  GET  /dna/intent/api/v1/template-programmer/template/<id>      (get version)

A member template is a leaf template containing actual Jinja2 content that
renders IOS/IOS-XE/NX-OS configuration lines.

Templates must be committed before they can be:
  • Deployed directly to a device
  • Referenced by a composite template

Committing creates an immutable versioned snapshot.  CatC assigns two UUIDs:

  templateId   (root UUID)    — permanent, never changes across commits
  versionId    (version UUID) — a NEW UUID is created on every commit;
                                 required in the deploy payload

IMPORTANT: CatC returns versionsInfo in RANDOM order — always sort by
versionTime (Unix-millisecond timestamp) descending to get the latest.

Template body
─────────────
"! DEBUG" is a valid IOS-XE comment line.  When rendered and pushed to a
device it produces no configuration change — safe on any managed device.

API reference
─────────────
  POST /dna/intent/api/v1/template-programmer/project/<projectId>/template
    { "name": "...", "language": "JINJA", "composite": false,
      "softwareType": "IOS", "softwareVariant": "XE",
      "templateContent": "! DEBUG\\n", "deviceTypes": [...] }
  ← {"response": {"taskId": "..."}}   task.data = root template UUID

  POST /dna/intent/api/v1/template-programmer/template/version
    {"templateId": "<rootId>", "comments": "..."}
  ← {"response": {"taskId": "..."}}   (no data in task — version is in detail)

  GET  /dna/intent/api/v1/template-programmer/template/<rootId>
  ← {"versionsInfo": [{"id": "<versionUUID>", "versionTime": <ms>, ...}, ...]}

Usage
─────
  export CATC_HOST=198.18.129.100
  export CATC_PASSWORD=<password>
  python3 create_member_template.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "6.3"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers (also re-used by step 6.4)
# ─────────────────────────────────────────────────────────────────────────────

def get_or_create_project(token):
    """Return project UUID, creating it if absent."""
    name = helpers.PROJECT_NAME
    resp = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/project?name={name}",
        token=token,
    )
    if isinstance(resp, list) and resp:
        return resp[0]["id"]

    resp   = helpers.http(
        "POST",
        f"{helpers.TEMPLATE_API}/project",
        token=token,
        body={"name": name, "description": "Automated example project"},
    )
    result = helpers.poll_task(token, resp["response"]["taskId"], label="create project")
    pid    = result.get("data")
    if not pid:
        raise RuntimeError(f"Project creation did not return a UUID: {result}")
    return pid


def commit_template(token, root_id, label):
    """
    Commit the template and return the latest version UUID.

    versionsInfo is returned in random order — sort by versionTime descending
    to identify the snapshot just created.
    """
    print(f"\n  POST /template-programmer/template/version  (commit {label})")
    resp = helpers.http(
        "POST",
        f"{helpers.TEMPLATE_API}/template/version",
        token=token,
        body={
            "templateId": root_id,
            "comments": f"Committed by {label}",
        },
    )
    helpers.poll_task(token, resp["response"]["taskId"], label=f"commit {label}")

    # Retrieve the latest version UUID from the template detail endpoint.
    # versionsInfo order is random — sort descending by versionTime.
    print(f"\n  GET /template-programmer/template/{root_id}")
    detail   = helpers.http("GET", f"{helpers.TEMPLATE_API}/template/{root_id}", token=token)
    versions = sorted(
        detail.get("versionsInfo", []),
        key=lambda v: v.get("versionTime", 0),
        reverse=True,
    )
    version_id = versions[0]["id"] if versions else root_id
    print(f"  ↳ versionsInfo entries : {len(versions)}")
    print(f"  ↳ Latest version UUID  : {version_id}")
    return version_id


# ─────────────────────────────────────────────────────────────────────────────
# Step-specific logic
# ─────────────────────────────────────────────────────────────────────────────

def create_member_template(token, project_id):
    """
    Create the member template if it does not already exist.
    Returns the root template UUID.
    """
    name = helpers.MEMBER_NAME

    print(f"  GET /template-programmer/template?projectNames={helpers.PROJECT_NAME}")
    existing = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/template?projectNames={helpers.PROJECT_NAME}",
        token=token,
    )
    for t in (existing if isinstance(existing, list) else []):
        if t.get("name") == name:
            root_id = t["templateId"]
            print(f"  ↳ Already exists — root id: {root_id}")
            return root_id

    print(f"\n  POST /template-programmer/project/{project_id}/template")
    resp = helpers.http(
        "POST",
        f"{helpers.TEMPLATE_API}/project/{project_id}/template",
        token=token,
        body={
            "name":            name,
            "description":     "Minimal member template — renders a single IOS comment",
            "language":        "JINJA",
            "softwareType":    "IOS",
            "softwareVariant": "XE",
            # "! DEBUG" is a valid IOS-XE comment — produces no config change.
            "templateContent": "! DEBUG\n",
            "composite":       False,
            "deviceTypes": [
                {
                    "productFamily": "Switches and Hubs",
                    "productSeries": "Cisco Catalyst 9300 Series Switches",
                }
            ],
        },
    )
    result  = helpers.poll_task(token, resp["response"]["taskId"], label="create member")
    root_id = result.get("data")
    if not root_id:
        raise RuntimeError(f"Member template creation did not return a UUID: {result}")
    print(f"  ↳ Created — root id: {root_id}")
    return root_id


def main():
    print(f"\n{'='*60}")
    print(f"  {STEP} — Create and Commit Member Template")
    print(f"  Host    : {helpers.CATC_HOST}:{helpers.CATC_PORT}")
    print(f"  Project : {helpers.PROJECT_NAME}")
    print(f"  Template: {helpers.MEMBER_NAME}")
    print(f"{'='*60}\n")

    token      = helpers.get_token()
    project_id = get_or_create_project(token)
    print(f"  Project UUID: {project_id}")

    # ── Step 6.3: create the member template ─────────────────────────────────
    print(f"\n[Step 6.3] Create member template '{helpers.MEMBER_NAME}'")
    root_id = create_member_template(token, project_id)

    # ── Step 6.3b: commit it (creates a versioned snapshot) ──────────────────
    print(f"\n[Step 6.3b] Commit member template")
    version_id = commit_template(token, root_id, label="member")

    print(f"\n{'='*60}")
    print(f"  ✓  Member template ready")
    print(f"  Root UUID    (mainTemplateId in deploy): {root_id}")
    print(f"  Version UUID (templateId     in deploy): {version_id}")
    print()
    print("  How it works:")
    print("    1. POST to project/<id>/template creates the template (async task)")
    print("    2. POST to template/version commits it — creates an immutable snapshot")
    print("    3. GET template/<id> returns versionsInfo — sort by versionTime desc")
    print("       to find the version UUID of the snapshot just created")
    print("    4. BOTH root UUID and version UUID are needed by the deploy payload")
    print()
    print("  Next step → 6.4-Cisco-Catalyst-Center-Templates-Create-Composite-Template/")
    print()


if __name__ == "__main__":
    main()
