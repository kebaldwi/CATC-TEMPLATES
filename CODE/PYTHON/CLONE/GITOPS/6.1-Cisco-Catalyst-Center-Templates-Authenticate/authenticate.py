#!/usr/bin/env python3
# ============================================================================
# 6.1 — Authenticate
# ============================================================================
# Authors
# ============================================================================
# | Name            | Role                              | Contact              |
# |-----------------|-----------------------------------|----------------------|
# | Igor Manassypov | Systems Engineer                  | imanassy@cisco.com   |
# Copyright © 2024-2026 Cisco Systems, Inc. All rights reserved.
# ============================================================================
"""
Demonstrates: POST /dna/system/api/v1/auth/token

Every CatC REST call requires a short-lived JWT obtained via HTTP Basic auth.
The server returns {"Token": "<jwt>"}.  All subsequent steps attach this JWT
as the X-Auth-Token request header.

API reference
─────────────
  POST https://<host>/dna/system/api/v1/auth/token
    Authorization: Basic base64(username:password)
  ← {"Token": "<jwt>"}

Usage
─────
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  python3 authenticate.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "6.1"


def main():
    print(f"\n{'='*60}")
    print(f"  {STEP} — Authenticate")
    print(f"  Host: {helpers.CATC_HOST}:{helpers.CATC_PORT}")
    print(f"  User: {helpers.CATC_USERNAME}")
    print(f"{'='*60}\n")

    print("  POST /dna/system/api/v1/auth/token")
    print("  Auth: HTTP Basic (username + password → base64-encoded)")

    token = helpers.get_token()

    print(f"\n  Token received (first 60 chars): {token[:60]}…")
    print(f"\n  ✓  Authentication successful")
    print()
    print("  How it works:")
    print("    1. Credentials are base64-encoded and sent in Authorization: Basic header")
    print("    2. CatC validates the credentials and returns a short-lived JWT")
    print("    3. Subsequent API calls attach it as:  X-Auth-Token: <jwt>")
    print()
    print("  Next step → 6.2-Cisco-Catalyst-Center-Templates-Create-Project/")
    print()


if __name__ == "__main__":
    main()
