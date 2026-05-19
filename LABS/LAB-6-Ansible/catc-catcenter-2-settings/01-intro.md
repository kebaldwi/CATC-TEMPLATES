# Settings and Credentials

In this module we apply two playbooks back-to-back: **2.0 Network Settings** and **3.0 Device Credentials**. Together they finish the *design* phase of Catalyst Center — every site in the hierarchy you built in Module 1 ends up with DNS/NTP/Syslog/SNMP/AAA/banner applied, and the global credential store gains the CLI, SNMPv2c, and NETCONF entries that Catalyst Center will use to log in to discovered devices.

> References:
> * [2.0 Network Settings — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/2.0-Cisco-Catalyst-Center-Settings/README.md)
> * [3.0 Device Credentials — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/3.0-Cisco-Catalyst-Center-Credentials/README.md)

## Why Two Playbooks?

The Catalyst Center API splits "site design" across two surfaces:

| Concept | Where it lives in CatC | Driven by |
|---------|------------------------|-----------|
| Network infrastructure settings (DNS, DHCP, NTP, Syslog, SNMP, AAA, banner) | Per-site (`/v1/network/{siteId}`) | **2.0** `network_settings.yml` |
| Device authentication credentials (CLI, SNMPv2c R/W, NETCONF) | Global credential store, then assigned to sites | **3.0** `credentials.yml` |

The two are independent — running them in either order works — but the *recommended* order is settings first, credentials second, because the credential assignment in 3.0 references site UUIDs that the 1.0 hierarchy run already created.

## What 2.0 Network Settings Does

`network_settings.yml` is built around the v1 site-scoped settings API. The core flow is:

| Step | Mechanism |
|------|-----------|
| Resolve every site path → UUID | `cisco.catalystcenter.sites_info` |
| Authenticate (one-shot JWT) | `ansible.builtin.uri` → `POST /dna/system/api/v1/auth/token` |
| Push settings per site | `ansible.builtin.uri` → `PUT /dna/intent/api/v1/network/{siteId}` (returns 202 Accepted) |
| Poll the async execution | `ansible.builtin.uri` → `GET /dna/intent/api/v1/dnacaap/management/execution-status/{executionId}` until `SUCCESS` or `FAILURE` |

The `network_settings` block in `settings.json` describes what to push:

```json
"network_settings": {
  "dnsServers": ["198.18.133.1"],
  "ntpServers": ["198.18.133.1"],
  "syslogServers": ["198.18.133.28"],
  "snmpServers": ["198.18.133.28"],
  "timezone": "America/Los_Angeles",
  "messageOfTheDay": "TECOPS-2599 LAB POD"
}
```

Operations are fully idempotent — pushing the same payload twice returns success with no functional change.

## What 3.0 Device Credentials Does

`credentials.yml` uses two complementary surfaces:

| Credential type | Module | Why |
|-----------------|--------|-----|
| CLI | `cisco.dnac.device_credential_workflow_manager` | High-level, idempotent — handles create/update/delete + site-assignment in one call |
| SNMPv2c (R/W) | `cisco.dnac.device_credential_workflow_manager` | Same as CLI |
| NETCONF | `ansible.builtin.uri` (+ `cisco.dnac.global_credential_info` / `global_credential_delete`) | The Workflow Manager module does not yet cover NETCONF; direct REST against `/dna/intent/api/v1/global-credential/netconf` is used instead |

Two `settings.json` blocks drive the playbook:

```json
"device_credentials": [
  {"name": "lab-cli", "username": "netadmin", "password": "C1sco12345", "enable_password": "C1sco12345"},
  {"name": "lab-snmp", "snmp_v2c_read":  {"read_community":  "public"}},
  {"name": "lab-snmp", "snmp_v2c_write": {"write_community": "private"}},
  {"name": "lab-netconf", "netconf_port": 830}
],
"assign_credentials": [
  {"site_name": "Global/NA", "cli": "lab-cli", "snmp_v2c_read": "lab-snmp", "snmp_v2c_write": "lab-snmp", "netconf": "lab-netconf"}
]
```

Re-running with the same data is a no-op. Removing an entry and re-running with `state: deleted` removes the corresponding credential cleanly.

## What You Will Do

1. Encrypt `vault.yml` in both the `2.0-...-Settings` and `3.0-...-Credentials` directories (same `admin / C1sco12345`).
2. Run `network_settings.yml`, then verify in **Design → Network Settings**.
3. Run `credentials.yml`, then verify in **Design → Network Settings → Device Credentials**.

> **Prerequisites:** Module 1 (Hierarchy) is complete — every site in `settings.json` exists in Catalyst Center.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)
