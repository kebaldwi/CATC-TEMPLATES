# Building Hierarchy

In this module, we will use **Cisco Workflows** to build and deploy a network site hierarchy within Catalyst Center. Rather than clicking through the Catalyst Center UI to define Areas, Buildings, and Floors one by one, we drive the Catalyst Center Intent API from a Cisco Workflow that reads a structured `settings.json` file directly from this GitHub repository.

This is the first module that puts the orientation concepts into practice. The pattern introduced here — *GitHub as the source of truth, Cisco Workflows as the orchestration engine, Catalyst Center as the system of record* — is reused in every subsequent module of the lab.

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Cisco Workflows Overview" style="width:100%; height:auto;">

## Hierarchy Background

The **Design** area in Catalyst Center is where you create the structure and framework of your network, including the logical topology, network settings, and device type profiles that you can apply to devices throughout your network.

You build a network hierarchy that represents your network's geographical locations. The hierarchy is built up of **sites**. By default, there is one site called `Global`. The `Global` site can be expanded to contain areas, and optionally subareas (areas within areas). Within areas we create buildings, and within buildings we create floors. Creating areas, buildings, and floors makes it easy to apply design settings, credentials, templates, and provisioning intent later — all of which inherit down the tree.

The network hierarchy follows a predetermined order:

- **Areas** — Do not have a physical address. Areas are the largest element and can contain buildings and subareas. For example, an area named `United States` can contain a `California` subarea, which can contain a `San Jose` subarea.
- **Buildings** — Include a physical address and contain floors and floor plans. When you create a building, you must specify a physical address or latitude and longitude coordinates. Buildings cannot contain areas.
- **Floors** — Exist within buildings and consist of cubicles, walled offices, wiring closets, and so on. Floors can only be added to buildings.

Catalyst Center uses this hierarchy to logically align intent (code and configuration) against infrastructure, allowing the network administrator to scope changes and modifications to the network within specific maintenance windows or sites.

## Why Cisco Workflows for Hierarchy?

The workflow we will run in this module — `GitOps-BuildHierarchy-v3` — is a generic Catalyst Center workflow that talks to the Catalyst Center **Intent API** (`/dna/intent/api/v1/site` and `/dna/intent/api/v2/site`) and to the **GitHub Contents API**. It does the following on your behalf:

| Stage | What Happens |
|---|---|
| **1. List** | Lists all files in a GitHub directory (`Get-GitHub-Directory-v2`) |
| **2. Match** | Filters down to the target `settings.json` file |
| **3. Read** | Pulls the raw contents of `settings.json` (`Get-GitHub-File-v2`) |
| **4. Parse** |  Converts the JSON array into a table of hierarchy rows (Parent / Area / Building / Floor / Address) |
| **5. Build** | For each row:<br>• checks Catalyst Center<br> Then conditionally IF missing:<br>• creates the **Parent**, **Area**, **Building**, and **Floor**<br>• polling each create operation to completion |
| **6. Verify** | Resultant settings and credentials reflected in the workflow output |

Because the workflow checks each level before creating it, the run is **idempotent** — running it again with the same `settings.json` does not duplicate sites. If you change `settings.json` in GitHub and re-run the workflow, only the new sites are added.

### Logical Flow

The diagram below shows the full decision and loop structure of `GitOps-BuildHierarchy-v3`, including the embedded sub-flow that checks/creates each level (Parent → Area → Building → Floor) and polls execution status:

![GitOps Build Hierarchy — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/1.0-Cisco-Catalyst-Center-Site-Hierarchy/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/1.0-Cisco-Catalyst-Center-Site-Hierarchy/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/1.0-Cisco-Catalyst-Center-Site-Hierarchy/README.md)

## Source of Truth — `settings.json`

The hierarchy that Catalyst Center will end up with is defined entirely by the `settings.json` file in the GitHub repository. Each row in the JSON array describes one full Area → Building → Floor path:

```json
[
  {
    "HierarchyParent": "Global",
    "HierarchyArea": "NA",
    "HierarchyBldg": "HQ San Jose",
    "HierarchyFloor": "Floor 1",
    "HierarchyBldgAddress": "123 Main St"
  }
]
```

For this lab, the file lives at `Projects/BGP_EVPN/Settings/settings.json` in the `kebaldwi/TECOPS-2599` repository, and is the same file referenced by the default workflow input parameters (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`).

## What You Will Do in This Module

1. Confirm Catalyst Center ↔ ISE integration is in place (prerequisite for later modules, verified here).
2. Open the **Cisco Workflows** dashboard and locate the `GitOps-BuildHierarchy-v3` workflow.
3. Review the input parameters (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`, `FORCE Update`).
4. Run the workflow and observe each step from the **View Runs** panel.
5. Verify the hierarchy was created correctly in Catalyst Center under **Design → Network Hierarchy**.

> **Prerequisites:** **Completed** the previous section [**Orientation**](../catc-catcenter-0-orientation/01-intro.md), including the Remote Target setup that allows Cisco Workflows to reach Catalyst Center over the DCLOUD VPN.

> [**Next Section**](./02-integration.md)

> [**Return to LAB Menu**](../README.md)