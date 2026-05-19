# Importing Templates and Building Composites

In this module, we will use **Cisco Workflows** to **import** Jinja2 templates from this GitHub repository directly into the **Catalyst Center Template Hub**, and then **assemble** those templates into a **composite template** that can be deployed to devices through Network Profiles. As with hierarchy, settings, and discovery, the source of truth is GitHub — the workflows read the `.j2` template files and `.yml` composite definitions and drive the Catalyst Center Intent API to make reality match.

The same GitOps pattern reappears here: *GitHub as the source of truth, Cisco Workflows as the orchestration engine, Catalyst Center as the system of record.*

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Cisco Workflows Overview" style="width:100%; height:auto;">

## Template Hub Background

Catalyst Center includes a **Template Hub** (which replaced the legacy Template Editor in earlier versions). The Template Hub allows for the import and export of custom templates written in **Jinja2** (`.j2`) or **Velocity** (`.vm`) scripting languages. Templates are encapsulated in JSON inside Catalyst Center and grouped logically into **Projects**.

Two kinds of templates exist:

1. **Regular templates** — a single Jinja2 or Velocity file containing device configuration logic (variables, includes, conditionals, and CLI lines).
2. **Composite templates** — an ordered grouping of regular templates that are deployed together as one logical configuration unit. Composite templates are what Network Profiles ultimately reference when assigning intent to a site.

Templates and parameters allow for the **configuration** of devices when associated with a site hierarchy through a **Network Profile**. Before either can be done, every template must first exist in the Template Hub and be **published** (committed) — both `Regular` templates and any `Composite` template that references them.

In this lab we will:

1. Import every `.j2` template under `Projects/BGP_EVPN/DayNTemplates` into the Template Hub project `BGP_EVPN`, in dependency-safe order, and **commit** each one.
2. Use the `BGP-EVPN-BUILD.yml` composite definition to **assemble** those templates into a single composite template, then **commit** the composite.

> **Note:** A Deployment API exists in the underlying workflows for completeness, but actual provisioning to devices is performed in later modules (Network Profile, Provisioning) and not invoked here.

## Why Cisco Workflows for Templates?

Two workflows back this module:

- **`GitOps-ImportTemplates`** — imports every `.j2`/`.vm` file from a GitHub directory into a Template Hub project, in dependency-safe order, and commits each template.
- **`GitOps-BuildCompositeTemplate`** — reads `.yml` composite definition files from the same GitHub directory and assembles them into a published composite template that bundles ordered member templates.

Both call the Catalyst Center **Intent API** (`/dna/intent/api/v1/template-programmer/project`, `/dna/intent/api/v1/template-programmer/project/{id}/template`, `/dna/intent/api/v1/template-programmer/template`, `/dna/intent/api/v1/template-programmer/template/version`) and the **GitHub Contents API**.

### `GitOps-ImportTemplates` — High-level Stages

| Stage | What Happens |
|---|---|
| **1. List** | Lists all files in the GitHub directory (`Get-GitHub-Directory-v2`) |
| **2. Project Name** | Python script derives `CATC-ProjectName` from `GITHUB-PATH`; condition selects the supplied `TemplateHubProjectName` if non-empty |
| **3. Dependency Map** | `CATC-DependencyMapping-v1` parses every `.j2`/`.vm` file for `{% include %}` / `#parse` references and reorders the file list so dependencies import first |
| **4. Filter & Read** | For each file, only `.j2` / `.vm` / `.json` extensions proceed; `Get-GitHub-File-v2` retrieves raw content with `Accept: application/vnd.github.raw+json` |
| **5. Substitute & Import** | Python replaces `{{ TEMPLATE_PROJECT_NAME }}` with the resolved project name; `CATC-CreateTemplate-v3` finds/creates the project, checks for the existing template, and `POST`s the template (skipped when present and `FORCE Update = false`) |
| **6. Commit All** | After a 30 s settle, `CATC-GetProjectTemplatesIDs` collects every template ID in the project and `CATC-CommitTemplate-v2` publishes each one (`POST /dna/intent/api/v1/template-programmer/template/version`) |

### `GitOps-BuildCompositeTemplate` — High-level Stages

| Stage | What Happens |
|---|---|
| **1. List** | Lists all files in the GitHub directory (`Get-GitHub-Directory-v2`) |
| **2. Project Name** | Same Python-derived `CATC-ProjectName` + `TemplateHubProjectName` selection logic as above |
| **3. Filter `.yml`** | The `For Each` loop only processes files ending in `.yml`; `.j2`/`.vm`/other files are silently skipped |
| **4. Read & Name** | `Get-GitHub-File-v2` retrieves the raw YAML; Python derives `TemplateName` by replacing `.yml` with `.j2` |
| **5. Resolve & Create** | `CATC-CreateCompositeTemplate-v3` finds/creates the project, checks for the existing composite, parses the YAML `sequence`, resolves each member template name to its UUID via `GET /dna/intent/api/v1/template-programmer/template`, and `POST`s the composite with ordered `containingTemplates` |
| **6. Commit Composite** | After a 30 s settle, `CATC-CommitTemplate-v2` publishes only the composite template just created |

Because both workflows check for existing items before creating them, runs are **idempotent**. Setting `FORCE Update = true` overwrites existing templates / composites with their current GitHub contents (creating a new published version each time).

### Logical Flow

The full decision and loop structure for each workflow — including dependency mapping, per-file processing, member-ID resolution, and the commit loops — is shown below:

#### `GitOps-ImportTemplates` Logical Flow

![GitOps Import Templates — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/4.0-Cisco-Catalyst-Center-Templates-Github-integration/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/4.0-Cisco-Catalyst-Center-Templates-Github-integration/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/4.0-Cisco-Catalyst-Center-Templates-Github-integration/README.md)

#### `GitOps-BuildCompositeTemplate` Logical Flow

![GitOps Build Composite Template — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/5.0-Cisco-Catalyst-Center-Templates-Composite/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/5.0-Cisco-Catalyst-Center-Templates-Composite/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/5.0-Cisco-Catalyst-Center-Templates-Composite/README.md)

## Source of Truth — `.j2` Templates and `.yml` Composite Definition

The template source files live in the same GitHub path consumed by both workflows:

```
Projects/
└── BGP_EVPN/
    └── DayNTemplates/
        ├── BGP-EVPN-BUILD.yml          # YAML composite definition
        ├── BGP-EVPN-BUILD.j2           # Primary Jinja2 build template
        ├── DEFN-CLIENT-PORTS.j2        # Shared definition (dependency)
        ├── DEFN-VRF.j2                 # Shared VRF definition
        ├── FABRIC-EVPN.j2              # Fabric EVPN configuration
        ├── FABRIC-NVE.j2               # Fabric NVE configuration
        └── (additional .j2 / .yml files)
```

A regular template may carry the placeholder `{{ TEMPLATE_PROJECT_NAME }}`, which is substituted with the resolved project name at import time. Templates may also reference each other with Jinja2 includes; `CATC-DependencyMapping-v1` reads these references and reorders the import sequence so dependencies are always imported first.

The composite definition is a small YAML file that names the composite, the project it belongs to, and the ordered sequence of member templates it bundles:

```yaml
# BGP-EVPN-BUILD.yml
composite:
  name: BGP-EVPN-BUILD
  project: BGP_EVPN
  description: "BGP EVPN Build composite for Catalyst 9000 fabric"
  sequence:
    - template: DEFN-CLIENT-PORTS.j2
    - template: DEFN-VRF.j2
    - template: FABRIC-EVPN.j2
    - template: FABRIC-NVE.j2
    - template: BGP-EVPN-BUILD.j2
```

For this lab, all of the above lives at `Projects/BGP_EVPN/DayNTemplates` in the `kebaldwi/TECOPS-2599` repository, and is the same path referenced by the default workflow input parameters (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`).

## What You Will Do in This Module

1. Open the **Cisco Workflows** dashboard and locate `GitOps-ImportTemplates`.
2. Review the input parameters:</br> (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `TemplateHubProjectName`, `FORCE Update`).
3. Run `GitOps-ImportTemplates` and observe each step from the **View Runs** panel — including dependency reordering, per-template import, and the commit loop.
4. Run `GitOps-BuildCompositeTemplate` against the same GitHub path to assemble the composite template from its YAML definition and commit it.
5. Verify the resulting project, regular templates, and composite template in Catalyst Center under **Tools → Template Hub**.

> **Prerequisites:** **Completed** the previous module [**Building Hierarchy**](../catc-catcenter-1-hierarchy/01-intro.md). The site hierarchy is required for downstream Network Profile assignment; settings and discovery (modules 2 and 3) are not strictly required for the import itself but are needed before composite templates can be deployed in later modules.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)