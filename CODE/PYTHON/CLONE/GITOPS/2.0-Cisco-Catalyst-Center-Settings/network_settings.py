#!/usr/bin/env python3
# ============================================================================
# 2.0 - Apply Network Settings
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
  PUT /dna/intent/api/v1/network/<siteId>
  GET /dna/intent/api/v1/execution-status/<executionId>  (if returned)
  GET /api/v1/task/<taskId>                               (if returned)

Builds the composite network settings payload from settings.json and applies it
per site. Only non-null fields are sent.

Usage
-----
  export CATC_HOST=198.18.129.100
  export CATC_USERNAME=admin
  export CATC_PASSWORD=<password>
  export CATC_SETTINGS_JSON=/absolute/path/to/settings.json    # optional
  python3 network_settings.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import helpers

STEP = "2.0"
POLL_RETRIES = 20
POLL_DELAY_SEC = 3

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


def fetch_site_map(token):
    resp = helpers.http("GET", f"{helpers.BASE_URL}/dna/intent/api/v1/site", token=token)
    result = {}
    for site in resp.get("response", []):
        hierarchy = site.get("nameHierarchy")
        if hierarchy:
            result[hierarchy] = site.get("id")
    return result


def maybe_add(dst, key, value):
    if value is None:
        return
    if isinstance(value, (list, dict)) and not value:
        return
    dst[key] = value


def build_network_payload(raw):
    payload = {}

    maybe_add(payload, "dhcpServer", raw.get("dhcp_server"))
    maybe_add(payload, "ntpServer", raw.get("ntp_server"))
    maybe_add(payload, "timezone", raw.get("timezone"))

    dns_raw = raw.get("dns_server") or {}
    dns = {}
    maybe_add(dns, "domainName", dns_raw.get("domain_name"))
    maybe_add(dns, "primaryIpAddress", dns_raw.get("primary_ip_address"))
    maybe_add(dns, "secondaryIpAddress", dns_raw.get("secondary_ip_address"))
    maybe_add(payload, "dnsServer", dns)

    motd_raw = raw.get("message_of_the_day") or {}
    motd = {}
    maybe_add(motd, "bannerMessage", motd_raw.get("banner_message"))
    if motd_raw.get("retain_existing_banner") is not None:
        motd["retainExistingBanner"] = str(motd_raw.get("retain_existing_banner")).lower()
    maybe_add(payload, "messageOfTheday", motd)

    syslog_raw = raw.get("syslog_server") or {}
    syslog = {}
    maybe_add(syslog, "configureDnacIP", syslog_raw.get("configure_dnac_ip"))
    maybe_add(syslog, "ipAddresses", syslog_raw.get("ip_addresses"))
    maybe_add(payload, "syslogServer", syslog)

    snmp_raw = raw.get("snmp_server") or {}
    snmp = {}
    maybe_add(snmp, "configureDnacIP", snmp_raw.get("configure_dnac_ip"))
    maybe_add(snmp, "ipAddresses", snmp_raw.get("ip_addresses"))
    maybe_add(payload, "snmpServer", snmp)

    netflow_raw = raw.get("netflow_server") or {}
    netflow = {}
    maybe_add(netflow, "configureDnacIP", netflow_raw.get("configure_dnac_ip"))
    maybe_add(netflow, "ipAddress", netflow_raw.get("ip_address"))
    if netflow_raw.get("port") is not None:
        netflow["port"] = int(netflow_raw.get("port"))
    maybe_add(payload, "netflowcollector", netflow)

    network_aaa = raw.get("network_aaa") or {}
    if network_aaa:
        naaa = {}
        maybe_add(naaa, "servers", network_aaa.get("server_type"))
        maybe_add(naaa, "ipAddress", network_aaa.get("primary_server_address"))
        maybe_add(naaa, "network", network_aaa.get("pan_address"))
        maybe_add(naaa, "protocol", network_aaa.get("protocol"))
        maybe_add(naaa, "sharedSecret", network_aaa.get("shared_secret"))
        maybe_add(payload, "network_aaa", naaa)

    endpoint_aaa = raw.get("client_and_endpoint_aaa") or {}
    if endpoint_aaa:
        eaaa = {}
        maybe_add(eaaa, "servers", endpoint_aaa.get("server_type"))
        maybe_add(eaaa, "ipAddress", endpoint_aaa.get("primary_server_address"))
        maybe_add(eaaa, "network", endpoint_aaa.get("pan_address"))
        maybe_add(eaaa, "protocol", endpoint_aaa.get("protocol"))
        maybe_add(eaaa, "sharedSecret", endpoint_aaa.get("shared_secret"))
        maybe_add(payload, "clientAndEndpoint_aaa", eaaa)

    return payload


def poll_execution_status(token, execution_id, label):
    url = f"{helpers.BASE_URL}/dna/intent/api/v1/execution-status/{execution_id}"
    for attempt in range(1, POLL_RETRIES + 1):
        resp = helpers.http("GET", url, token=token)
        status = (resp.get("executionStatus") or "").upper()
        message = resp.get("message") or status
        print(f"    [{label}] [{attempt}/{POLL_RETRIES}] {message[:100]}")
        if status in {"SUCCESS", "FAILURE"}:
            if status == "FAILURE":
                raise RuntimeError(f"Execution failed for {label}: {message}")
            return
        time.sleep(POLL_DELAY_SEC)
    raise RuntimeError(f"Execution status timeout for {label}")


def apply_network_settings(token, site_name, site_id, payload):
    print(f"  PUT /network/{site_id}  -> {site_name}")
    resp = helpers.http(
        "PUT",
        f"{helpers.BASE_URL}/dna/intent/api/v1/network/{site_id}",
        token=token,
        body=payload,
    )

    task_id = resp.get("response", {}).get("taskId")
    if task_id:
        helpers.poll_task(token, task_id, label=f"network {site_name}")

    execution_id = resp.get("executionId")
    if execution_id:
        poll_execution_status(token, execution_id, label=f"network {site_name}")


def main():
    print(f"\n{'=' * 60}")
    print(f"  {STEP} - Apply Catalyst Center Network Settings")
    print(f"{'=' * 60}\n")

    settings_path, project = load_settings()
    print(f"  Settings JSON: {settings_path}")

    token = helpers.get_token()
    site_map = fetch_site_map(token)

    changed = 0
    skipped = 0
    for entry in project:
        raw = entry.get("network_settings") or {}
        if not raw:
            skipped += 1
            continue

        site_name = site_name_from_entry(entry)
        site_id = site_map.get(site_name)
        if not site_id:
            raise RuntimeError(f"Site not found in Catalyst Center: {site_name}")

        payload = build_network_payload(raw)
        if not payload:
            skipped += 1
            continue

        apply_network_settings(token, site_name, site_id, payload)
        changed += 1

    print(f"\n  Sites updated: {changed}")
    print(f"  Entries skipped: {skipped}")
    print("\n  Next step -> 3.0-Cisco-Catalyst-Center-Credentials/")
    print()


if __name__ == "__main__":
    main()
