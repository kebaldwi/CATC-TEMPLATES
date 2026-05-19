# Building Hierarchy

In this module, we use the **`cisco.catalystcenter`** Ansible collection to build a network site hierarchy in Catalyst Center. Rather than clicking through the Design pages to create Areas, Buildings, and Floors one by one, we run a single Ansible playbook (`site_hierarchy.yml`) that reads the same `settings.json` file used by every other module and converges the Catalyst Center hierarchy to match.

This is the first module that turns the orientation work into something visible in the controller. The pattern introduced here — *GitHub `settings.json` as source of truth, Ansible as orchestration engine, Catalyst Center as system of record* — is reused in every later module.

> Reference: full as-built playbook documentation at [Support/Resources/Ansible/1.0-Cisco-Catalyst-Center-Site-Hierarchy/README.md](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/1.0-Cisco-Catalyst-Center-Site-Hierarchy/README.md).

## Hierarchy Background

The **Design** area in Catalyst Center is where you create the structure and framework of your network, including the logical topology, network settings, and device-type profiles. You build a network hierarchy that represents your geographical locations.

The hierarchy is built up of **sites**. By default there is one site called `Global`. The `Global` site can be expanded to contain Areas, and optionally subareas (areas within areas). Within Areas we create Buildings, and within Buildings we create Floors. Creating Areas, Buildings, and Floors makes it easy to apply design settings, credentials, templates, and provisioning intent later — all of which inherit down the tree.

The network hierarchy follows a predetermined order:

- **Areas** — Do not have a physical address. Areas are the largest element and can contain buildings and subareas. For example, an area `United States` can contain a `California` subarea, which can contain a `San Jose` subarea.
- **Buildings** — Include a physical address and contain floors and floor plans. When you create a building you must specify a physical address or latitude/longitude coordinates. Buildings cannot contain areas.
- **Floors** — Exist within buildings and consist of cubicles, walled offices, wiring closets, and so on. Floors can only be added to buildings.

Catalyst Center uses this hierarchy to logically align intent against infrastructure, allowing the network administrator to scope changes within specific maintenance windows or sites.

## Why Ansible for Hierarchy?

The `site_hierarchy.yml` playbook drives Catalyst Center using three typed modules from the `cisco.catalystcenter` collection — one per resource type:

| Resource | Module | API Endpoint(s) |
|----------|--------|-----------------|
| Existing site discovery | `cisco.catalystcenter.sites_info` | `GET /dna/intent/api/v1/sites` |
| Areas (create / update / delete) | `cisco.catalystcenter.areas` | `POST /v1/areas`, `PUT /v1/areas/{id}`, `DELETE /v1/areas/{id}` |
| Buildings (create / update / delete) | `cisco.catalystcenter.buildings` | `POST /v2/buildings`, `PUT /v2/buildings/{id}`, `DELETE /v2/buildings/{id}` |
| Floors (create / update / delete) | `cisco.catalystcenter.floors` | `POST /v2/floors`, `PUT /v2/floors/{id}`, `DELETE /v2/floors/{id}` |

The playbook does the following on your behalf:

| Stage | What Happens |
|---|---|
| 1. Read | Loads `settings.json` from disk |
| 2. Synthesize | Derives every Parent / Area / Building / Floor path from the entries' hierarchy fields |
| 3. Sort | De-duplicates the path list and sorts shallow-to-deep so parents are processed before children |
| 4. Map | Calls `sites_info` to fetch every existing site UUID into a `site_id_map` |
| 5. Build | Per row: if the path exists, run a typed module with `state: merged` and the resolved `id:`; otherwise run with `state: merged` and no `id:` to create the resource |
| 6. Resolve | After each create, call `sites_info` again with the new path to capture its UUID — children of this site can then resolve their `parentId` |

Because every level is checked against `site_id_map` before any write, the playbook is fully **idempotent**. Re-running it with the same `settings.json` produces no changes. Editing `settings.json` and re-running adds or updates only the deltas. Setting `state: deleted` reverses the order (deepest first) to respect parent-child constraints.

### Logical Flow

The full decision and loop structure of the playbook (including the embedded include_tasks pattern that runs per path) is shown below:

![Site Hierarchy — Logical Flow](../../../ASSETS/LABS/ANSIBLE/diagrams/1.0-Cisco-Catalyst-Center-Site-Hierarchy/DIAGRAMS/logical-flow.png)

## Source of Truth — `settings.json`

The hierarchy that Catalyst Center will end up with is defined entirely by `settings.json`. Each row in the JSON array describes one Area → Building → Floor path:

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

For this lab the file lives at `Projects/BGP_EVPN/Settings/settings.json` in the cloned repository, and is the same file referenced by every other playbook in the suite via the `settings_json_path` variable in `inventory.yml`.

## What You Will Do in This Module

1. Confirm the Catalyst Center ↔ ISE integration is in place (prerequisite for later modules, verified here).
2. Encrypt the playbook's `vault.yml` with your master password.
3. Run `site_hierarchy.yml` and read the `PLAY RECAP`.
4. Verify the hierarchy was created correctly in Catalyst Center under **Design → Network Hierarchy**.

> **Prerequisites:** the [Orientation module](../catc-catcenter-0-orientation/01-intro.md) is complete — repository cloned on the Script Server, `~/tecops-venv` active, `~/.vault_pass` created with `0600` permissions.

> [**Next Section**](./02-integration.md)

> [**Return to LAB Menu**](../README.md)
