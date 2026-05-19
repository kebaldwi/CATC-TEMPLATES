#!/usr/bin/env python3
# ============================================================================
# 6.2 — Create Project
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
  GET  /dna/intent/api/v1/template-programmer/project?name=<name>
  POST /dna/intent/api/v1/template-programmer/project

A Catalyst Center "project" is a namespace container for templates.
Templates created in step 3.0 and 4.0 must belong to a project.

This step is idempotent: if the project already exists, its UUID is returned
unchanged — no duplicate is created.

The project UUID is needed by steps 3.0 and 4.0 when POSTing new templates
to the project endpoint:
  POST /template-programmer/project/<projectId>/template

API reference
─────────────
  GET  /dna/intent/api/v1/template-programmer/project?name=<name>
  ← [] if not found, or [{"id": "<uuid>", "name": "...", ...}] if present

  POST /dna/intent/api/v1/template-programmer/project
    {"name": "<name>", "description": "..."}
  ← {"response": {"taskId": "<uuid>", "url": "..."}}
    Task data field carries the new project UUID on completion.

Usage
─────
  export CATC_HOST=198.18.129.100
  export CATC_PASSWORD=<password>
  export CATC_PROJECT=DEBUG-PROJECT   # optional, defaults to DEBUG-PROJECT
  python3 create_project.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "6.2"


def get_or_create_project(token):
    """
    Return the UUID of the target project, creating it if it does not exist.

    CatC creates projects asynchronously — the POST returns a taskId which
    must be polled.  The task 'data' field carries the new project UUID.
    """
    name = helpers.PROJECT_NAME

    print(f"  GET /template-programmer/project?name={name}")
    resp = helpers.http(
        "GET",
        f"{helpers.TEMPLATE_API}/project?name={name}",
        token=token,
    )

    if isinstance(resp, list) and resp:
        pid = resp[0]["id"]
        print(f"  ↳ Already exists — reusing id: {pid}")
        return pid

    print("  ↳ Not found")
    print(f"\n  POST /template-programmer/project")
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
    print(f"  ↳ Created — id: {pid}")
    return pid


def main():
    print(f"\n{'='*60}")
    print(f"  {STEP} — Create Project")
    print(f"  Host   : {helpers.CATC_HOST}:{helpers.CATC_PORT}")
    print(f"  Project: {helpers.PROJECT_NAME}")
    print(f"{'='*60}\n")

    token      = helpers.get_token()
    project_id = get_or_create_project(token)

    print(f"\n  ✓  Project ready")
    print(f"  Project UUID: {project_id}")
    print()
    print("  How it works:")
    print("    1. GET checks whether the project already exists by name")
    print("    2. If missing, POST creates it — returns a taskId (async operation)")
    print("    3. Task is polled until complete; task.data carries the new project UUID")
    print("    4. The project UUID is required when POSTing templates in step 3.0")
    print()
    print("  Next step → 6.3-Cisco-Catalyst-Center-Templates-Create-Member-Template/")
    print()


if __name__ == "__main__":
    main()
