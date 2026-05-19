#!/usr/bin/env python3
# ============================================================================
# helpers.py — shared utilities for CatC Python step-by-step examples
# ============================================================================
# Authors
# ============================================================================
# | Name            | Role                              | Contact              |
# |-----------------|-----------------------------------|----------------------|
# | Igor Manassypov | Systems Engineer                  | imanassy@cisco.com   |
# Copyright © 2024-2026 Cisco Systems, Inc. All rights reserved.
# ============================================================================
"""
Shared configuration, HTTP helpers, and CatC utilities used by every step script.

Import from a sibling step directory:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from common import helpers
"""

import json
import os
import ssl
import time
import urllib.request
import urllib.error
from base64 import b64encode

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION  —  override with environment variables (recommended)
# ─────────────────────────────────────────────────────────────────────────────

CATC_HOST       = os.getenv("CATC_HOST",       "198.18.129.100")
CATC_PORT       = int(os.getenv("CATC_PORT",   "443"))
CATC_USERNAME   = os.getenv("CATC_USERNAME",   "admin")
CATC_PASSWORD   = os.getenv("CATC_PASSWORD",   "")       # always set via env var
CATC_VERIFY_TLS = os.getenv("CATC_VERIFY_TLS", "false").lower() == "true"

# Management IP of any device already discovered/managed by Catalyst Center
TARGET_DEVICE_IP = os.getenv("CATC_DEVICE_IP", "198.19.1.1")

# Template project and names used across examples (override to target real templates)
PROJECT_NAME   = os.getenv("CATC_PROJECT",   "DEBUG-PROJECT")
MEMBER_NAME    = os.getenv("CATC_MEMBER",    "DEBUG-MEMBER.j2")
COMPOSITE_NAME = os.getenv("CATC_COMPOSITE", "DEBUG-COMPOSITE.j2")

# ─────────────────────────────────────────────────────────────────────────────
# API base paths
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL      = f"https://{CATC_HOST}:{CATC_PORT}"
TEMPLATE_API  = f"{BASE_URL}/dna/intent/api/v1/template-programmer"
DEVICE_API    = f"{BASE_URL}/dna/intent/api/v1/network-device"
DEPLOY_API_V2 = f"{BASE_URL}/dna/intent/api/v2/template-programmer/template/deploy"
TASK_API      = f"{BASE_URL}/api/v1/task"

# Async task polling settings
POLL_RETRIES   = 15
POLL_DELAY_SEC = 3


# ─────────────────────────────────────────────────────────────────────────────
# SSL context
# ─────────────────────────────────────────────────────────────────────────────

def _ssl_ctx():
    """Return an SSL context — TLS verification disabled by default for lab use."""
    ctx = ssl.create_default_context()
    if not CATC_VERIFY_TLS:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


# ─────────────────────────────────────────────────────────────────────────────
# HTTP helper
# ─────────────────────────────────────────────────────────────────────────────

def http(method, url, token=None, body=None, basic=None):
    """
    Minimal HTTP client using only the Python standard library.

    Parameters
    ----------
    method  : str          — GET / POST / PUT / DELETE
    url     : str          — full URL including scheme + host
    token   : str | None   — X-Auth-Token JWT (mutually exclusive with basic)
    body    : dict | None  — serialised to JSON; sent as application/json
    basic   : tuple | None — (username, password) for HTTP Basic auth

    Returns
    -------
    dict  — parsed JSON response body
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    if token:
        headers["X-Auth-Token"] = token
    elif basic:
        creds = b64encode(f"{basic[0]}:{basic[1]}".encode()).decode()
        headers["Authorization"] = f"Basic {creds}"

    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, context=_ssl_ctx()) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code} {exc.reason}  {method} {url}\n{body_text}"
        ) from exc


# ─────────────────────────────────────────────────────────────────────────────
# Async task polling
# ─────────────────────────────────────────────────────────────────────────────

def poll_task(token, task_id, label="task"):
    """
    GET /api/v1/task/<taskId>

    CatC operations are asynchronous — the API returns a taskId immediately
    and the actual work runs in the background.  Poll until:
      - endTime is set AND progress is not PENDING/IN_PROGRESS  → success
      - isError = true                                           → failure

    Returns the final task 'response' dict on success.
    Raises RuntimeError on task failure or poll timeout.
    """
    url = f"{TASK_API}/{task_id}"
    for attempt in range(1, POLL_RETRIES + 1):
        resp     = http("GET", url, token=token)
        result   = resp.get("response", {})
        progress = result.get("progress", "")
        is_error = result.get("isError", False)
        has_end  = bool(result.get("endTime"))
        pending  = any(kw in progress.upper() for kw in ("PENDING", "IN_PROGRESS"))

        if is_error:
            raise RuntimeError(
                f"Task '{label}' failed — {result.get('failureReason', progress)}"
            )
        if has_end and not pending:
            print(f"    [{label}] Complete ✓  {progress[:120]}")
            return result

        print(f"    [{label}] [{attempt}/{POLL_RETRIES}]  {progress[:80]}")
        time.sleep(POLL_DELAY_SEC)

    raise RuntimeError(
        f"Task '{label}' did not complete within {POLL_RETRIES * POLL_DELAY_SEC}s"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────────────────────────────────────

def get_token():
    """
    POST /dna/system/api/v1/auth/token  (HTTP Basic auth)

    CatC returns a short-lived JWT in the 'Token' field.
    Every subsequent API call must carry it as header: X-Auth-Token

    Raises SystemExit if CATC_PASSWORD is not set.
    """
    if not CATC_PASSWORD:
        raise SystemExit(
            "ERROR: CATC_PASSWORD environment variable is not set.\n"
            "  export CATC_PASSWORD=<your-catc-password>"
        )
    resp  = http(
        "POST",
        f"{BASE_URL}/dna/system/api/v1/auth/token",
        basic=(CATC_USERNAME, CATC_PASSWORD),
    )
    token = resp.get("Token")
    if not token:
        raise RuntimeError("Authentication failed — no Token in response")
    return token