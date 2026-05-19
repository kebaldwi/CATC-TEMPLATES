# Provisioning Devices and Deploying the Composite

In this module, we will use **Cisco Workflows** to **provision** discovered devices to their assigned site and **deploy** the published composite template to each one. This is the culmination of every preceding module — hierarchy, settings, discovery, templates, and the network profile assignment all feed into this final step that activates the configuration on each physical device.

The same GitOps pattern reappears here: *GitHub as the source of truth, Cisco Workflows as the orchestration engine, Catalyst Center as the system of record.*

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Cisco Workflows Overview" style="width:100%; height:auto;">

## Provisioning Background

In Catalyst Center, **provisioning** binds a device to its site within the SDA fabric context and makes it eligible to receive the templates attached to the site's Network Profile. Once a device is provisioned, **template deployment** pushes the actual configuration content (in this lab, the composite template `BGP-EVPN-BUILD.j2`) to the device through the Catalyst Center Service.

A few key concepts:

- **Composite template** — an ordered bundle of regular member templates (assembled in module 4). The workflow deploys the composite as a single unit; Catalyst Center expands it on the device by deploying each member in sequence with its parameters.
- **First-time provisioning vs. re-provisioning** — the workflow checks each device's current SDA provisioning state and chooses `POST` (first-time) or `PUT` (re-provision) automatically. This makes runs safe whether the device has been provisioned before or not.
- **Versioned deployment** — the workflow always resolves the latest **committed** version of the composite. Templates in DRAFT are never deployed.
- **`forcePushTemplate: true`** — the deployment body always carries this flag, so re-running the workflow restores devices to the GitOps-defined state (drift correction).

In this lab we will provision every device listed in `network_profile.DayNTemplateNames[*].TemplateTarget` to the site `Global/PODS/POD x/Building Px/Floor 1`, then deploy the latest committed version of `BGP-EVPN-BUILD.j2` to each device with its full member-template parameter payload.

## Why Cisco Workflows for Provisioning?

The workflow we will run in this module — `GitOps-DeviceProvisioning` — is a generic Catalyst Center workflow that calls the Catalyst Center **Intent API** (`/dna/intent/api/v1/sites`, `/dna/intent/api/v2/template-programmer/project`, `/dna/intent/api/v1/network-device`, `/dna/intent/api/v2/template-programmer/template`, `/dna/intent/api/v1/templates/{id}/versions`, `/dna/intent/api/v1/sda/provisionDevices`, `/dna/intent/api/v2/template-programmer/template/deploy`) and the **GitHub Contents API**. It does the following on your behalf:

| Stage | What Happens |
|---|---|
| **1. Read** | Pulls the raw contents of `settings.json` directly (`Get-GitHub-File-v2`) — no directory scan loop |
| **2. Parse** | A JSONPath query extracts the hierarchy fields, the composite `templateName`, and the `templateTarget` device IP array |
| **3. Resolve (parallel)** | Three branches run simultaneously:<br>• `GET /dna/intent/api/v1/sites?nameHierarchy=…` → `siteId`<br>• `GET /dna/intent/api/v2/template-programmer/project?name={Project Name}` → `compositeTemplateId`<br>• `GET /dna/intent/api/v1/network-device` + per-IP JSONPath loop → `deviceIdArray` |
| **4. Composite Structure** | `GET /dna/intent/api/v2/template-programmer/template?id={compositeTemplateId}` → extract `containingTemplateIds` (member UUIDs in deployment order) |
| **5. Member Loop** | For each member: `GET .../template?id={memberId}` → extract `templateParams` → build `{ paramName: defaultValue }` (Set Variables for ≤1 param, Python transform for >1) → accumulate `memberTemplateDeploymentInfo` |
| **6. Versioned Body** | `GET /dna/intent/api/v1/templates/{compositeTemplateId}/versions` → resolve latest `versionId`; assemble full deployment body with `isComposite=true`, `forcePushTemplate=true`, device placeholders (`**REPLACE_DEVICE_ID**`, `**REPLACE_DEVICE_HOSTNAME**`), and the per-member array |
| **7. Per-Device Loop** | For each device UUID:<br>• Resolve hostname; substitute placeholders<br>• `GET /dna/intent/api/v1/sda/provisionDevices` → choose `POST` (first-time) or `PUT` (re-provision); poll task<br>• `POST /dna/intent/api/v2/template-programmer/template/deploy`; poll task |

Because the workflow detects current provisioning state per device and uses `forcePushTemplate: true` on every deployment, runs are **safe to re-run** — no duplicate provisioning records and configuration drift is corrected on each pass.

### Logical Flow

The diagram below shows every decision point and loop, including the three-branch parallel resolution block (Step 3), the member-template iteration (Steps 4–5), the composite body assembly (Step 6), the per-device provision/deploy loop with task polling (Step 7), and the first-time vs. re-provision branch:

![GitOps Device Provisioning — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/7.0-Cisco-Catalyst-Center-Provision-Composite/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/7.0-Cisco-Catalyst-Center-Provision-Composite/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/7.0-Cisco-Catalyst-Center-Provision-Composite/README.md)

## Source of Truth — `settings.json`

The same `settings.json` that has driven every previous module also drives provisioning. The workflow reads two pieces of information from the `network_profile` block:

- The composite **template name** to deploy (`DayNTemplateNames[].TemplateName`).
- The **list of device IPs** to provision and configure (`DayNTemplateNames[].TemplateTarget`).

```json
{
  "project": [
    {
      "HierarchyParent": "Global/PODS",
      "HierarchyArea":   "POD 0",
      "HierarchyBldg":   "Building P0",
      "HierarchyFloor":  "Floor 1",
      "network_profile": {
        "DayNTemplateNames": [
          {
            "TemplateName": "BGP-EVPN-BUILD.j2",
            "TemplateTarget": [
              "198.19.1.1", "198.19.1.2", "198.19.1.3",
              "198.19.1.4", "198.19.1.5", "198.19.1.6"
            ],
            "DeployTemplate": true
          }
        ]
      }
    }
  ]
}
```

> **Note:** Unlike the network-profile workflow, the site hierarchy fields (`HierarchyParent`, `HierarchyArea`, `HierarchyBldg`, `HierarchyFloor`) are also exposed as **direct workflow input parameters** in addition to being read from `settings.json`. The input parameters drive the `siteId` and device resolution; the JSON fields drive template target and composite name extraction.

For this lab, the file lives at `Projects/BGP_EVPN/Settings/settings.json` in the `kebaldwi/TECOPS-2599` repository, and is the same file referenced by the default workflow input parameters (`GITHUB_USER`, `GITHUB_REPO`, `GITHUB_PATH`, `GITHUB_FILE`).

## What You Will Do in This Module

1. Open the **Cisco Workflows** dashboard and locate the `GitOps-DeviceProvisioning` workflow.
2. Review the input parameters:</br> (`HierarchyParent`, `HierarchyArea`, `HierarchyBldg`, `HierarchyFloor`, `Project Name`, `GITHUB_USER`, `GITHUB_REPO`, `GITHUB_PATH`, `GITHUB_FILE`).
3. Run the workflow and observe each step from the **View Runs** panel — including the parallel resolution, per-member parameter extraction, composite body assembly, and the per-device provisioning + deployment loop with task polling.
4. Verify the resulting site provisioning and configuration deployment in Catalyst Center under **Provision → Network Devices → Inventory** and via the device's **Show Running Configuration**.

> **Prerequisites:** **Completed** every previous module — [**Building Hierarchy**](../catc-catcenter-1-hierarchy/01-intro.md), [**Assigning Settings and Credentials**](../catc-catcenter-2-settings/01-intro.md), [**Discovering Devices**](../catc-catcenter-3-discovery/01-intro.md), [**Importing Templates and Building Composites**](../catc-catcenter-4-templates/01-intro.md), and [**Building and Assigning Network Profiles**](../catc-catcenter-5-networkprofiles/01-intro.md). The site, settings, devices, composite template, and Network Profile must all be in place before this workflow can resolve every required ID and deploy the configuration.

> **Time:** This is the most time-intensive workflow in the suite. Each device is processed sequentially — provision (with task polling) followed by template deploy (with task polling). Allow several minutes per device.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)