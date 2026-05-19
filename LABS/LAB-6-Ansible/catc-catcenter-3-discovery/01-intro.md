# Device Discovery and Site Assignment

In this module we run two playbooks: **4.0 Device Discovery** discovers the pod devices over SSH and adds them to Catalyst Center's inventory; **5.0 Assign To Site** then moves each device from `Global` (where everything lands by default) into its correct hierarchy position.

> References:
> * [4.0 Device Discovery — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/4.0-Cisco-Catalyst-Center-Device-Discovery/README.md)
> * [5.0 Assign To Site — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/5.0-Cisco-Catalyst-Center-Assign-To-Site/README.md)

## Why Two Playbooks?

Catalyst Center's discovery flow has two distinct outcomes:

1. **Inventory** — the device exists in Catalyst Center, has been authenticated, and its facts (model, OS, interfaces, neighbors) are known.
2. **Site placement** — the device is anchored to a specific Area / Building / Floor in the hierarchy.

Running discovery alone is enough to manage a device's inventory state but **not** to provision it — site placement is required for credentials, settings, templates, and Day-N config. The two responsibilities are split because real-world workflows often discover first (read-only) and place later (after a human approves the inventory).

## What 4.0 Discovery Does

`device_discovery.yml` is a thin wrapper around the high-level `cisco.dnac.discovery_workflow_manager` module. The Workflow Manager module hides the four-step CatC discovery API set (`POST /v1/discovery`, `GET /v1/discovery/{id}/...`, `DELETE /v1/discovery/{id}` etc.) behind a single idempotent task.

The flow is:

| Step | Mechanism |
|------|-----------|
| Read `device_list` from every project entry in `settings.json` | Jinja2 |
| Reconstruct each entry's site path from `HierarchyParent/Area/Bldg/Floor` | Jinja2 (deepest non-null wins) |
| Split comma-separated IPs into per-pod lists | `split(',') \| map('trim')` |
| Submit one **MULTI RANGE** discovery job per pod | `cisco.dnac.discovery_workflow_manager state=merged` |
| Track each job to completion | Module-internal polling |

Catalyst Center then reaches each IP using SSH against the global credentials created in 3.0, validates them, and adds the reachable devices to **Provision → Inventory**.

The relevant `settings.json` fragment:

```json
{
  "HierarchyParent": "Global",
  "HierarchyArea": "NA",
  "HierarchyBldg": "Pod-1",
  "device_list": "198.18.140.1, 198.18.10.2, 198.18.20.2"
}
```

## What 5.0 Assign To Site Does

`assign_to_site.yml` reads the same `device_list` entries, groups IPs by their reconstructed site path, resolves each site's UUID via `cisco.dnac.site_info`, and calls `cisco.dnac.assign_device_to_site` once per site with the full IP list.

| Step | Module |
|------|--------|
| Group device IPs by target site path | `set_fact` (Jinja2 dict accumulation) |
| Resolve site name → UUID | `cisco.dnac.site_info` |
| Move IP list under that site UUID | `cisco.dnac.assign_device_to_site` |

The operation is idempotent — devices that are already at the correct site are skipped silently.

## What You Will Do

1. Encrypt `vault.yml` in both `4.0-...-Device-Discovery` and `5.0-...-Assign-To-Site` directories.
2. Run `device_discovery.yml`. Verify in **Provision → Inventory** that devices appear with status *Reachable* / *Managed*.
3. Run `assign_to_site.yml`. Verify each device's site column reflects its `settings.json` position.

> **Prerequisites:** Modules 1 (Hierarchy) and 2 (Settings + Credentials) are complete. The CLI / SNMP / NETCONF credentials assigned to the site **must** match the actual device credentials, otherwise discovery will mark the device *Unreachable*.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)
