# Building and Assigning Network Profiles

In this module, we will use **Cisco Workflows** to **create** a switching **network profile** in Catalyst Center, attach the published Day0/DayN templates to it, and **assign** it to the correct site in the hierarchy. As with the previous modules, the source of truth is the same `settings.json` file in this GitHub repository — the workflow reads the `network_profile` block and drives the Catalyst Center Intent API to make reality match.

The same GitOps pattern reappears here: *GitHub as the source of truth, Cisco Workflows as the orchestration engine, Catalyst Center as the system of record.*

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Cisco Workflows Overview" style="width:100%; height:auto;">

## Network Profile Background

A **Network Profile** in Catalyst Center binds **Day0** (PnP onboarding) and **DayN** (operational configuration) templates to a **site**. Without a profile assigned to a site, devices provisioned at that site cannot automatically receive their configuration templates — provisioning would have nothing to apply.

Profiles are typed by the device family they target. This workflow creates **switching** profiles only (other types — `wireless`, `routing` — require different API payloads and are not handled here). Each switching profile contains:

- An optional **Day0 template reference** — the PnP/onboarding template applied during initial device boot. Often left empty for fabric deployments where PnP uses a separate seed process.
- One or more **DayN template references** — the operational templates (typically a single composite template such as `BGP-EVPN-BUILD.j2`) applied during device provisioning.

Profile-to-site assignment is what makes the templates available for Day-N provisioning in the next module. Once assigned, devices that are provisioned at a site automatically receive the templates bound through the profile.

In this lab we will create a switching profile named `BGP-EVPN-Switching`, attach the composite template `BGP-EVPN-BUILD.j2` published in the previous module as its DayN template, and assign the profile to the target site (Area / Building / Floor) defined in `settings.json`.

## Why Cisco Workflows for Network Profiles?

The workflow we will run in this module — `GitOps-BuildNetworkProfile` — is a generic Catalyst Center workflow that calls the Catalyst Center **Intent API** (`/dna/intent/api/v1/template-programmer/template`, `/dna/intent/api/v2/site`, `/dna/intent/api/v1/network-profile`, `/dna/intent/api/v1/network-profile/{id}/site`) and the **GitHub Contents API**. It does the following on your behalf:

| Stage | What Happens |
|---|---|
| **1. Read** | Pulls the raw contents of `settings.json` directly (`Get-GitHub-File-v2`) — no directory scan loop |
| **2. Parse** | A JSONPath query extracts 9 fields: hierarchy path (Parent/Area/Bldg/Floor), `ProfileName`, `DayNTemplates` and `Day0Templates` arrays, and their counts |
| **3. Prepare (parallel)** | Three parallel branches:<br>• Join Day0 template names to a comma-separated string (empty when null)<br>• Join DayN template names to a comma-separated string<br>• Compose the `siteNameHierarchy`, call `GET /dna/intent/api/v2/site`, extract `siteId` |
| **4. Resolve (parallel)** | Two parallel branches call `CATC-GetTemplates-v2` to resolve each Day0 and DayN template **name** to its current Template Hub **UUID** (single or multi-template handling) |
| **5. Create & Assign** | `CATC-CreateSiteProfile-v3`:<br>• `GET /dna/intent/api/v1/network-profile` (existence check by name + type)<br>• `POST /dna/intent/api/v1/network-profile` (create switching profile with template references)<br>• `GET /dna/intent/api/v1/network-profile/{id}/site` (verify current site assignment)<br>• `POST /dna/intent/api/v1/network-profile/{id}/site` (assign profile to target site) |
| **6. Settle** | Top-level `Sleep 30 s` allows Catalyst Center to propagate the profile assignment before downstream provisioning workflows begin |

Because the workflow checks for an existing profile before creating one and verifies site assignment before issuing the assign call, runs are **safe to re-run** — repeated runs against the same `settings.json` will not duplicate the profile or its site binding.

### Logical Flow

The diagram below shows the full decision and parallel-branch structure of `GitOps-BuildNetworkProfile`, including the two parallel blocks (Steps 3 and 4) and the four-step sequence inside `CATC-CreateSiteProfile-v3`:

![GitOps Build Network Profile — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/6.0-Cisco-Catalyst-Center-Network-Profile/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/6.0-Cisco-Catalyst-Center-Network-Profile/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/6.0-Cisco-Catalyst-Center-Network-Profile/README.md)

## Source of Truth — `settings.json`

The same `settings.json` that defines the hierarchy, network settings, device discovery, and template targeting also carries the `network_profile` definition. Each entry under `project[]` binds one switching profile to a specific Area / Building / Floor:

```json
{
  "project": [
    {
      "HierarchyParent": "Global/PODS",
      "HierarchyArea":   "POD 0",
      "HierarchyBldg":   "Building P0",
      "HierarchyFloor":  "Floor 1",
      "network_profile": {
        "profile_name": "BGP-EVPN-Switching",
        "DayNTemplateNames": [
          {
            "TemplateName": "BGP-EVPN-BUILD.j2",
            "TemplateTag": "DEMO",
            "Project": "Building P0",
            "TemplateTarget": [
              "198.19.1.1", "198.19.1.2", "198.19.1.3",
              "198.19.1.4", "198.19.1.5", "198.19.1.6"
            ],
            "DeployTemplate": true
          }
        ],
        "Day0TemplateNames": [
          {
            "TemplateName": null,
            "TemplateTag": null,
            "Project": null,
            "TemplateTarget": [],
            "DeployTemplate": null
          }
        ]
      }
    }
  ]
}
```

The `DayNTemplateNames[].TemplateName` value (`BGP-EVPN-BUILD.j2`) is the composite template published by the previous module. The workflow resolves this name to its Template Hub UUID at runtime via `CATC-GetTemplates-v2`, so the profile payload is portable across Catalyst Center instances. `Day0TemplateNames[].TemplateName` is left `null` for this lab — fabric deployments use a separate PnP seed process rather than a Day0 template bound to the profile.

For this lab, the file lives at `Projects/BGP_EVPN/Settings/settings.json` in the `kebaldwi/TECOPS-2599` repository, and is the same file referenced by the default workflow input parameters (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`).

## What You Will Do in This Module

1. Open the **Cisco Workflows** dashboard and locate the `GitOps-BuildNetworkProfile` workflow.
2. Review the input parameters:</br> (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`, `TemplateHubProjectName`).
3. Run the workflow and observe each step from the **View Runs** panel — including the parallel template-name preparation, `siteId` resolution, parallel template-UUID resolution, profile creation, and site assignment.
4. Verify the resulting profile and its site binding in Catalyst Center under **Design → Network Profiles**.

> **Prerequisites:** **Completed** the previous modules [**Building Hierarchy**](../catc-catcenter-1-hierarchy/01-intro.md), [**Assigning Settings and Credentials**](../catc-catcenter-2-settings/01-intro.md), and [**Importing Templates and Building Composites**](../catc-catcenter-4-templates/01-intro.md). The site hierarchy must exist, network settings must be applied, and every template named in `network_profile` must already be imported and committed in the Template Hub before this workflow can resolve the IDs and create the profile.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)