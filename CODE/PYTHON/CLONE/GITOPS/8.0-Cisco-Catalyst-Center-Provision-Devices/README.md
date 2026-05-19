# 8.0 - Cisco Catalyst Center Provision Devices

This example provisions managed devices to their target site in Catalyst Center.
It is the Python equivalent of Ansible playbook `8.0-Cisco-Catalyst-Center-Provision-Devices`.

## Script

`provision_devices.py` reads `device_list` entries from `settings.json`, groups them
by site hierarchy path, and provisions each device to its site using the SDA
provisioning REST API.

**What it demonstrates:**

| Step | API endpoint | Purpose |
|------|-------------|---------|
| 1 | `POST /dna/system/api/v1/auth/token` | Authenticate — obtain JWT |
| 2 | `GET /dna/intent/api/v1/site?name=<path>` | Resolve site UUID |
| 3 | `GET /dna/intent/api/v1/network-device?managementIpAddress=<ip>` | Resolve device UUIDs |
| 4 | `GET /dna/intent/api/v1/sda/provisionDevices?siteId=<uuid>&limit=500` | Check already-provisioned devices |
| 5 | `POST /dna/intent/api/v1/sda/provisionDevices` | Provision new devices |
| 6 | `PUT /dna/intent/api/v1/sda/provisionDevices` | Re-provision existing devices (force mode) |
| 7 | `GET /api/v1/task/<taskId>` | Poll async task to completion |

Shared utilities (authentication, HTTP, task polling) are imported from
`../common/helpers.py` via the `common` package.

## Idempotency

- **Not yet provisioned** → `POST` to add the device to the site
- **Already provisioned, `CATC_FORCE_REPROVISION=false`** (default) → skipped
- **Already provisioned, `CATC_FORCE_REPROVISION=true`** → `PUT` to re-provision

This mirrors the `force_reprovision` flag in the Ansible inventory.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 provision_devices.py
```

**Optional overrides:**

```bash
export CATC_SETTINGS_JSON=/path/to/settings.json   # default: Projects/BGP_EVPN/Settings/settings.json
export CATC_FORCE_REPROVISION=true                  # re-provision already-provisioned devices
export DEBUG=true                                   # print UUIDs and full payloads
```

## Outcome

Each device in `device_list` is provisioned to its target site. The script prints
a per-site summary showing how many devices were newly provisioned, re-provisioned,
or skipped. Per-device child task results (matching Catalyst Center task IDs) are
displayed for every submitted request.
