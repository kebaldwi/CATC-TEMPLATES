# Provisioning Devices

In this final module we run two playbooks. **8.0 Provision Devices** anchors each device to its site by pushing the site-level network settings (AAA, syslog, NTP, SNMP, netflow) and licensing — this is the prerequisite that allows Day-N templates to be applied. **9.0 Composite Deploy** then deploys the BGP-EVPN composite template (built in Module 4 and bound to sites in Module 5) to those provisioned devices.

> References:
> * [8.0 Provision Devices — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/8.0-Cisco-Catalyst-Center-Provision-Devices/README.md)
> * [9.0 Composite Deploy — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/9.0-Cisco-Catalyst-Center-Provision-Composite/README.md)

## Why Two Playbooks?

Provisioning and template deployment are separate operations in Catalyst Center:

| Concern | Catalyst Center API | Ansible playbook |
|---------|---------------------|-------------------|
| Push site settings + license + apply Network Profile binding | `POST /v1/sda/provisionDevices` | **8.0** `provision_devices.yml` |
| Push Day-N composite template body to running config | `POST /v2/template-programmer/template/deploy` | **9.0** `deploy_composite_template.yml` |

A device must be *provisioned* (8.0) before any template can be *deployed* (9.0) — Catalyst Center will refuse the deploy otherwise.

## What 8.0 Does

`provision_devices.yml` uses direct REST (`ansible.builtin.uri`) end-to-end because the v1 SDA `provisionDevices` endpoint is not yet wrapped by a Workflow Manager module. The flow is:

| Step | API call |
|------|----------|
| Authenticate | `POST /dna/system/api/v1/auth/token` |
| Resolve site UUID | `GET /v1/site?name=<encoded path>` |
| Resolve device UUIDs | `GET /v1/network-device?managementIpAddress=<ip>` |
| Check already-provisioned state (idempotency) | `GET /v1/sda/provisionDevices?siteId=<uuid>&limit=500` |
| Submit provision batch | `POST /v1/sda/provisionDevices` |
| Poll task | `GET /v1/task/<taskId>` until `endTime` set |

Devices already provisioned at the target site are skipped via Jinja2 set-difference, so re-runs are no-ops.

## What 9.0 Does

`deploy_composite_template.yml` similarly uses direct REST against the v2 deploy endpoint because the `cisco.dnac.template_workflow_manager` does not yet handle composite deploy with `copyingConfig: true`. The flow is:

| Step | API call |
|------|----------|
| Authenticate | `POST /dna/system/api/v1/auth/token` |
| List templates in the project (find latest version IDs) | `GET /v1/template-programmer/template?projectNames=<name>` |
| Fetch composite detail (extract member templates) | `GET /v1/template-programmer/template/<id>` |
| Resolve device UUIDs | `GET /v1/network-device?managementIpAddress=<ip>` |
| Build `memberTemplateDeploymentInfo` | `set_fact` |
| Deploy composite | `POST /v2/template-programmer/template/deploy` (with `copyingConfig: true`) |
| Poll deploy task | `GET /v1/task/<taskId>` (parses `progress.failureReason` for the authoritative result) |

Which composites get deployed is driven by `DayNTemplateNames` entries in `settings.json` that are marked `DeployTemplate: true`:

```json
"DayNTemplateNames": [
  {
    "TemplateName": "BGP-EVPN-BUILD",
    "ProjectName": "TECOPS-2599",
    "DeployTemplate": true,
    "TargetDevices": ["198.18.10.2", "198.18.20.2"]
  }
]
```

## What You Will Do

1. Encrypt `vault.yml` in both `8.0-...-Provision-Devices` and `9.0-...-Provision-Composite` directories.
2. Run `provision_devices.yml`. Verify in **Provision → Inventory** that each device's *Provisioning Status* turns green.
3. Run `deploy_composite_template.yml`. Verify the Day-N config shows up on the device via `show running-config` and in CatC's deployment history.

> **Prerequisites:** Modules 1–5 complete. Devices in inventory at their assigned sites; Network Profile bound; templates synced.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)
