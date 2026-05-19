#!/usr/bin/env python3
# ============================================================================
# 6.4 — Create and Commit a Composite Template
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
  POST /dna/intent/api/v1/template-programmer/project/<projectId>/template
  POST /dna/intent/api/v1/template-programmer/template/version   (commit)
  GET  /dna/intent/api/v1/template-programmer/template/<id>      (get version)

A composite template is an ordered container (composite=True) whose
containingTemplates list references one or more member templates by root UUID.

Key differences from a member template:
  composite=True          — marks it as a container, not a leaf
  templateContent=""      — body is empty; all rendered config comes from members
  containingTemplates     — list of member root UUIDs in execution order

Like member templates, a composite must be committed before it can be deployed.
The commit creates a versioned snapshot and assigns a version UUID.

Two UUIDs are required by the deploy payload (step 8.0):
  mainTemplateId = composite root UUID    (permanent — never changes)
  templateId     = composite version UUID (latest committed snapshot)

Requires: Step 6.3 to have run first (member template must exist in CatC).

API reference
─────────────
  POST /dna/intent/api/v1/template-programmer/project/<projectId>/template
    { "name": "...", "composite": true,
      "containingTemplates": [{"id": "<memberRootUUID>", "composite": false}],
      "templateContent": "", "deviceTypes": [...] }
  ← {"response": {"taskId": "..."}}   task.data = composite root UUID

  POST /dna/intent/api/v1/template-programmer/template/version
    {"templateId": "<rootId>", "comments": "..."}
  ← {"response": {"taskId": "..."}}

  GET  /dna/intent/api/v1/template-programmer/template/<rootId>
  ← {"versionsInfo": [...], "containingTemplates": [...]}

Usage
─────
  export CATC_HOST=198.18.129.100
  export CATC_PASSWORD=<password>
  python3 create_composite_template.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "6.4"


# ─────────────────────────────────────────────────────────────────────────────
# Template lookup helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get_project_id(token):
    name = helpers.PROJECT_NAME
    resp = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/project?name={name}",
        token=token,
    )
    if isinstance(resp, list) and resp:
        return resp[0]["id"]
    raise RuntimeError(
        f"Project '{name}' not found.  Run 6.3-Cisco-Catalyst-Center-Templates-Create-Member-Template/create_member_template.py first."
    )


def _get_template_root_id(token, template_name):
    """Return root UUID for a named template within the project, or None."""
    resp = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/template?projectNames={helpers.PROJECT_NAME}",
        token=token,
    )
    for t in (resp if isinstance(resp, list) else []):
        if t.get("name") == template_name:
            return t["templateId"]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Step-specific logic
# ─────────────────────────────────────────────────────────────────────────────

def create_composite_template(token, project_id, member_root_id):
    """
    Create the composite template referencing the member by root UUID.
    Returns the composite root UUID.
    """
    name        = helpers.COMPOSITE_NAME
    existing_id = _get_template_root_id(token, name)
    if existing_id:
        print(f"  ↳ Already exists — root id: {existing_id}")
        return existing_id

    print(f"\n  POST /template-programmer/project/{project_id}/template")
    resp = helpers.http(
        "POST",
        f"{helpers.TEMPLATE_API}/project/{project_id}/template",
        token=token,
        body={
            "name":            name,
            "description":     "Minimal composite — wraps DEBUG-MEMBER.j2",
            "language":        "JINJA",
            "softwareType":    "IOS",
            "softwareVariant": "XE",
            # Composite body is empty — all rendered config comes from member templates.
            "templateContent": "",
            "composite":       True,
            # containingTemplates: ordered list of member templates referenced by root UUID.
            # The order here determines the rendering order on the target device.
            "containingTemplates": [
                {"id": member_root_id, "composite": False}
            ],
            "deviceTypes": [
                {
                    "productFamily": "Switches and Hubs",
                    "productSeries": "Cisco Catalyst 9300 Series Switches",
                }
            ],
        },
    )
    result = helpers.poll_task(token, resp["response"]["taskId"], label="create composite")
    cid    = result.get("data")
    if not cid:
        raise RuntimeError(f"Composite creation did not return a UUID: {result}")
    print(f"  ↳ Created — root id: {cid}")
    return cid


def commit_template(token, root_id, label):
    """
    Commit the template and return the latest version UUID.
    versionsInfo is returned in random order — sort by versionTime descending.
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

    print(f"\n  GET /template-programmer/template/{root_id}")
    detail   = helpers.http("GET", f"{helpers.TEMPLATE_API}/template/{root_id}", token=token)
    versions = sorted(
        detail.get("versionsInfo", []),
        key=lambda v: v.get("versionTime", 0),
        reverse=True,
    )
    version_id = versions[0]["id"] if versions else root_id
    members    = detail.get("containingTemplates", [])
    print(f"  ↳ versionsInfo entries    : {len(versions)}")
    print(f"  ↳ Latest version UUID     : {version_id}")
    print(f"  ↳ containingTemplates     : {[m.get('name', m.get('id','?')) for m in members]}")
    return version_id


def main():
    print(f"\n{'='*60}")
    print(f"  {STEP} — Create and Commit Composite Template")
    print(f"  Host     : {helpers.CATC_HOST}:{helpers.CATC_PORT}")
    print(f"  Project  : {helpers.PROJECT_NAME}")
    print(f"  Composite: {helpers.COMPOSITE_NAME}")
    print(f"  Member   : {helpers.MEMBER_NAME}")
    print(f"{'='*60}\n")

    token      = helpers.get_token()
    project_id = _get_project_id(token)
    print(f"  Project UUID: {project_id}")

    # ── Step 6.4a: locate existing member template ───────────────────────────
    print(f"\n[Step 6.4a] Locate member template '{helpers.MEMBER_NAME}'")
    print(f"  GET /template-programmer/template?projectNames={helpers.PROJECT_NAME}")
    member_root_id = _get_template_root_id(token, helpers.MEMBER_NAME)
    if not member_root_id:
        raise RuntimeError(
            f"Member template '{helpers.MEMBER_NAME}' not found in project "
            f"'{helpers.PROJECT_NAME}'.  Run step 6.3 first."
        )
    print(f"  ↳ Member root id: {member_root_id}")

    # ── Step 6.4b: create the composite template ─────────────────────────────
    print(f"\n[Step 6.4b] Create composite template '{helpers.COMPOSITE_NAME}'")
    composite_root_id = create_composite_template(token, project_id, member_root_id)

    # ── Step 6.4c: commit it ──────────────────────────────────────────────────
    print(f"\n[Step 6.4c] Commit composite template")
    composite_version_id = commit_template(token, composite_root_id, label="composite")

    print(f"\n{'='*60}")
    print(f"  ✓  Composite template ready")
    print(f"  Root UUID    (mainTemplateId in deploy): {composite_root_id}")
    print(f"  Version UUID (templateId     in deploy): {composite_version_id}")
    print()
    print("  How it works:")
    print("    1. composite=True marks this as a container — not a leaf template")
    print("    2. containingTemplates lists member templates by root UUID (ordered)")
    print("    3. templateContent is empty — rendered config comes from the members")
    print("    4. Committing works identically to a member template (same API)")
    print("    5. Both root and version UUIDs are needed by the deploy payload")
    print()
    print("  Next step → 8.0-Cisco-Catalyst-Center-Provision-Deploy-Composite/")
    print()


if __name__ == "__main__":
    main()
