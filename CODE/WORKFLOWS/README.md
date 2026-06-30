# Catalyst Center — Workflows

> As-Built Documentation
> Authors: Keith Baldwin — Solutions Engineer - Automation HyperSpecialist (kebaldwi@cisco.com)
> Copyright © 2024–2026 Cisco Systems, Inc. All rights reserved.

This folder holds the Catalyst Center workflow JSON exports used throughout this repository. Workflows are grouped by maturity and intended consumption model into two subfolders:

| Subfolder | Purpose | Status |
|-----------|---------|--------|
| [EXCHANGE/](EXCHANGE/) | Production-ready, polished `-v3` end-to-end suite that is **published in Cisco Workflows** (the in-product Workflow Exchange catalog inside Catalyst Center). | Recommended for new deployments |
| [CATC/](CATC/) | Workflow library of original `CATC-*` building blocks and the first-generation `GitOps-*` v1 build chain. Many EXCHANGE workflows are evolved from, or reuse, the workflows in this folder. | Reference and reuse as subworkflows |

---

## Table of Contents

1. [EXCHANGE — Production Suite (Published in Cisco Workflows)](#exchange--production-suite-published-in-cisco-workflows)
2. [CATC — Workflow Library and Building Blocks](#catc--workflow-library-and-building-blocks)
3. [Relationship Between the Two Folders](#relationship-between-the-two-folders)
4. [Which Folder Should I Use?](#which-folder-should-i-use)

---

## EXCHANGE — Production Suite (Published in Cisco Workflows)

Folder: [EXCHANGE/](EXCHANGE/) — see the suite documentation in [EXCHANGE/README.md](EXCHANGE/README.md).

The EXCHANGE folder contains the **twelve-workflow `-v3` production suite** that delivers an end-to-end GitOps build-and-deploy chain for Catalyst Center, plus operations and reusable utility workflows. Every workflow in this folder is **published in Cisco Workflows** — the in-product Workflow Exchange catalog accessed from Catalyst Center under *Platform → Automation → Exchange* — so customers can install them directly from the catalog inside Catalyst Center without manually importing JSON.

Use cases solved by the EXCHANGE suite:

| # | Workflow | Use Case Solved |
|---|----------|-----------------|
| 1.0 | [Site Hierarchy](EXCHANGE/1.0-Cisco-Catalyst-Center-Site-Hierarchy/) | Build and maintain the Area / Building / Floor site hierarchy from a single source of truth in GitHub. |
| 2.0 | [Settings and Credentials](EXCHANGE/2.0-Cisco-Catalyst-Center-Settings-and-Credentials/) | Apply network settings (DNS, DHCP, NTP, SNMP, syslog, banner, AAA, Netflow) and assign CLI / SNMP credentials to sites. |
| 3.0 | [Device Discovery and Assign](EXCHANGE/3.0-Cisco-Catalyst-Center-Device-Discovery-and-Assign/) | Run Catalyst Center discovery jobs and assign discovered devices to their target sites. |
| 4.0 | [Templates GitHub Integration](EXCHANGE/4.0-Cisco-Catalyst-Center-Templates-Github-integration/) | Synchronise DayN member templates from a GitHub repository into a Template Hub project. |
| 5.0 | [Templates Composite](EXCHANGE/5.0-Cisco-Catalyst-Center-Templates-Composite/) | Build composite templates from YAML definitions in GitHub and commit them in Template Hub. |
| 6.0 | [Network Profile](EXCHANGE/6.0-Cisco-Catalyst-Center-Network-Profile/) | Bind a switching network profile to a site with Day0 and DayN template IDs. |
| 7.0 | [Provision Composite](EXCHANGE/7.0-Cisco-Catalyst-Center-Provision-Composite/) | Provision (or re-provision) managed devices and deploy the composite template at a site. |
| 8.0 | [Command Runner](EXCHANGE/8.0-Cisco-Catalyst-Center-Command-Runner/) | Run up to five read-only show commands on a managed device via the CLI Poller API for ad-hoc verification. |
| 9.0 | [Site Based Upgrade](EXCHANGE/9.0-Cisco-Catalyst-Center-Site-Based-Upgrade/) | Orchestrate site-scoped SWIM upgrades — golden image preparation, distribution, activation, and pre/post-check diagnostics. |
| 10.0 | [Paginated Device Inventory](EXCHANGE/10.0-Cisco-Catayst-Center-Paginated-Device-Inventory/) | Reusable utility — paginate the full device inventory and return a merged, optionally filtered device list. |
| 11.0 | [Paginated Site Hierarchy](EXCHANGE/11.0-Cisco-Catalyst-Center-Paginated-Site-Hierarchy/) | Reusable utility — paginate the complete site hierarchy and return merged JSON plus name and UUID lists. |
| 12.0 | [Bulk Command Runner](EXCHANGE/12.0-Cisco-Catalyst-Center-Bulk-Command-Runner/) | Reusable utility — iterate a shared device table, batch show commands in groups of five, and record pre/post-change diagnostics. |

Net outcome: a deterministic, version-controlled, end-to-end build of a Catalyst Center site — from empty hierarchy to provisioned devices with deployed composite templates — plus operational tooling for diagnostics and site-scoped upgrades.

---

## CATC — Workflow Library and Building Blocks

Folder: [CATC/](CATC/) — see the library documentation in [CATC/README.md](CATC/README.md).

The CATC folder is the **workflow library**. It contains the original `CATC-*` building-block workflows and the first-generation `GitOps-*` build chain that preceded the EXCHANGE `-v3` suite. These workflows are retained in the repository for reference, for reuse as subworkflows, and to support customers still running the earlier chain.

The contents fall into four functional groups:

| Group | Workflows | Use Case Solved |
|-------|-----------|-----------------|
| **CATC building blocks** | `CATC-BuildHierarchy-v2`, `CATC-AssignSettings-v2`, `CATC-CreateTemplate-v2`, `CATC-GitHubIntegration-v2`, `CATC-DeviceDiscovery`, `CATC-PortConfiguration` | Small, reusable workflows that each wrap one or a few Catalyst Center Intent API calls — composable into larger pipelines. |
| **Read-only utilities** | `CATC-GetHierarchy`, `CATC-DeviceInventory`, `CATC-CommandRunner` | Inspection helpers used as subworkflows by the rest of the suite (hierarchy snapshot, device inventory snapshot, ad-hoc show commands). |
| **Brown-field onboarding** | `CATC-BrownFieldOnboarding-v2`, `CATC-BrownFieldOnboarding-v3` | IBNS-based end-to-end onboarding of existing switches (discovery → normalisation → provisioning). |
| **GitOps v1 build chain** | `GitOps-BuildHierarchy`, `GitOps-BuildSettings`, `GitOps-DeviceDiscovery`, `GitOps-ImportTemplates`, `GitOps-BuildCompositeTemplate`, `GitOps-BuildNetworkProfile`, `GitOps-DeviceProvisioning` | First-generation GitHub-driven build chain — each workflow wraps the matching CATC building block and reads its intent from a GitHub repository. |

The CATC library is **not** packaged in the Workflow Exchange catalog. It is consumed directly from this repository — either by importing the JSON manually into Catalyst Center, or by referencing the individual workflows as subworkflows from other automations.

---

## Relationship Between the Two Folders

```
EXCHANGE/  ──►  Polished -v3 production chain    ──►  Published in Cisco Workflows
   ▲
   │ evolved from / reuses
   │
CATC/      ──►  CATC-* building blocks + GitOps v1 chain    ──►  Reference / subworkflow reuse
```

- Each `-v3` workflow in EXCHANGE is the productised successor of a workflow (or set of workflows) in CATC.
- Several EXCHANGE workflows still call into CATC workflows as subworkflows (for example, the EXCHANGE Command Runner is the same `CATC-CommandRunner.json` from the library).
- The CATC folder is the historical and structural foundation. The EXCHANGE folder is the supported, catalog-published surface.

---

## Which Folder Should I Use?

- **For a new production deployment** — use [EXCHANGE/](EXCHANGE/). Install directly from the Workflow Exchange catalog inside Catalyst Center, or import the JSON files from this folder. Follow the ordered installation in [EXCHANGE/README.md](EXCHANGE/README.md).
- **For learning, building your own workflows, or reusing subworkflows** — start in [CATC/](CATC/). The building-block workflows are smaller and easier to read, and they are the source patterns that the EXCHANGE suite is built on.
- **For customers still on the v1 GitOps chain** — keep using the `GitOps-*` workflows in [CATC/](CATC/) until you can plan a cut-over to the EXCHANGE `-v3` suite.