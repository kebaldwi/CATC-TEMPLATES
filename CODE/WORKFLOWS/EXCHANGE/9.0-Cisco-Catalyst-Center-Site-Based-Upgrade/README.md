# 9.0 — Cisco Catalyst Center: Site Based Upgrade

> **Workflow:** `Catalyst Center Site Based Upgrade.json`
> **Type:** Cisco Catalyst Center Generic Workflow (Intent API)
> **Subworkflows:** `CATC-DynamicSiteSelector`, `CATC-PaginatedDeviceInventory`, `CATC-MultipleShowCommands-v3`, `Get Task ID`, `Wait For Catalyst Center Task`, `String to Array`, `Create Image Uuid Array`
> **API Endpoints:**
> &nbsp;&nbsp;`GET  /dna/intent/api/v1/networkDevices/assignedToSite` — devices assigned to a site (paginated)
> &nbsp;&nbsp;`GET  /dna/intent/api/v1/image/importation/device-family-identifiers` — resolve device family identifier
> &nbsp;&nbsp;`POST /dna/intent/api/v1/images/ccoSync` — sync software images from Cisco.com
> &nbsp;&nbsp;`GET  /dna/intent/api/v1/images?productNameOrdinal={id}` — list images for a device family
> &nbsp;&nbsp;`GET  /dna/intent/api/v1/images?siteId={id}` — list images available for a site
> &nbsp;&nbsp;`POST /dna/intent/api/v1/images/{id}/download` — download an image from Cisco.com
> &nbsp;&nbsp;`POST /dna/intent/api/v1/images/{uuid}/sites/{siteId}/tagGolden` — tag an image as golden for a site/family
> &nbsp;&nbsp;`POST /dna/intent/api/v1/image/distribution` — distribute an image to a device
> &nbsp;&nbsp;`POST /dna/intent/api/v1/image/activation/device` — activate (boot) an image on a device
> **Minimum Catalyst Center version:** 2.3.7.9
> **Authors:** Keith Baldwin — Solutions Engineer - Automation HyperSpecialist (kebaldwi@cisco.com)
> **Copyright © 2024–2026 Cisco Systems, Inc. All rights reserved.**

---

## Table of Contents

1. [Overview](#overview)
   - [What it does](#what-it-does)
   - [What makes this workflow different](#what-makes-this-workflow-different)
   - [Logical Flow](#logical-flow)
2. [Prerequisites](#prerequisites)
3. [Directory Structure](#directory-structure)
4. [Workflow Input Parameters](#workflow-input-parameters)
5. [Internal Working Variables](#internal-working-variables)
6. [How It Works](#how-it-works)
   - [Step 1 — Select Site](#step-1--select-site)
   - [Step 2 — Device Selection](#step-2--device-selection)
   - [Step 3 — Target Devices (Pre-check)](#step-3--target-devices-pre-check)
   - [Step 4 — Get SWIM Images](#step-4--get-swim-images)
   - [Step 5 — Image Sanitization (per site)](#step-5--image-sanitization-per-site)
   - [Step 6 — Image Deployment](#step-6--image-deployment)
   - [Step 7 — Update Show Commands (Post-check)](#step-7--update-show-commands-post-check)
   - [Complete Device Inventory](#complete-device-inventory)
7. [SWIM API Payload Reference](#swim-api-payload-reference)
8. [Subworkflows](#subworkflows)
9. [Running the Workflow](#running-the-workflow)
10. [Expected Output](#expected-output)
11. [Workflow Ordering Dependency](#workflow-ordering-dependency)
12. [Troubleshooting](#troubleshooting)
13. [Additional Notes](#additional-notes)

---

## Overview

This Cisco Catalyst Center workflow performs a **site-based software image upgrade (SWIM)** across the devices within a selected site hierarchy. It guides an operator through site selection, device-type filtering, device family and target device selection, golden image preparation, and a choice of upgrade methodology — with diagnostic show-command capture before and after the upgrade for verification.

The workflow scopes the upgrade to a parent site and all of its child sites, intersects the site-assigned devices with a filtered, reachable, managed inventory of the selected device type, and lets the operator pick a specific device family (e.g., `Cisco Catalyst 9300 Switch`) and the final list of devices to upgrade. It then runs pre-check show commands against the cleansed target list, resolves the SWIM device family identifier, syncs and selects a golden image, ensures the image is downloaded and golden-tagged at each site, and distributes and/or activates the image on the selected devices. A confirmation prompt gates the post-check, after which the post-check show commands populate the shared global SWIM inventory table for before/after comparison.

### What it does

| Action | Mechanism |
|--------|-----------|
| Select parent + child sites | `CATC-DynamicSiteSelector` + Python "Find Children" → `HierarchyNames`, `HierarchyUuid` |
| Choose device type | `task.prompt_request` — Switches and Hubs / Routers / Wireless Controllers |
| Collect site-assigned devices | `For Each` site → `GET /dna/intent/api/v1/networkDevices/assignedToSite` → `HierarchyDeviceList` |
| Retrieve filtered inventory | `CATC-PaginatedDeviceInventory` (Workflow 10.0) + JSONPath filter (`family` + Reachable + Managed) |
| Build initial target table | Intersect inventory with site-assigned UUIDs → `Output-DeviceTable` |
| Choose device family | `task.prompt_request` — unique types from `Output-DeviceTable` (e.g., `Cisco Catalyst 9300 Switch`) |
| Select devices for upgrade | `task.prompt_request` (multiselect) → cleansed `DeviceTargetList` |
| Resolve SWIM family id | `GET /dna/intent/api/v1/image/importation/device-family-identifiers` → `SWIMFamilyIdentifier` |
| Build cleansed target table | Second `For Each` over filtered devices → `Output-DeviceTable` + `DeviceTargetUuidList` |
| Capture pre-check | `CATC-MultipleShowCommands-v3` → `precheck` column |
| Sync + select image | `POST /dna/intent/api/v1/images/ccoSync` + `GET /dna/intent/api/v1/images?productNameOrdinal=…` + prompt |
| Golden-tag per site | `GET images?siteId=…` → conditional `download` + `tagGolden` with task waits |
| Image upgrade method | `task.prompt_request` — Consolidated Upgrade / Distribute then Activate |
| Distribute / Activate | `POST image/distribution` and/or `POST image/activation/device` per device, with confirmations |
| Capture post-check | Confirmation prompt → `CATC-MultipleShowCommands-v3` → `postcheck` column |
| Complete inventory | `Complete Device Inventory` finalizes global `Device SWIM Inventory` table |

### What makes this workflow different

Unlike a manual, device-by-device upgrade through the Catalyst Center UI, this workflow:

1. **Scopes upgrades by site hierarchy** — selecting a parent site automatically includes all child sites (matched by `siteHierarchy` prefix), so an entire campus or building can be upgraded in one run.
2. **Intersects two device views** — it cross-references the site-assigned device list with a filtered, reachable, managed inventory, ensuring only devices that are both in the selected hierarchy **and** the chosen device type **and** online/managed are targeted.
3. **Pre-check runs against the cleansed list** — device family selection and the multi-select "Select Devices for Upgrade" prompt happen **before** the pre-check, so `CATC-MultipleShowCommands-v3` only runs against the devices the operator actually intends to upgrade.
4. **Automates golden image preparation per site** — for each site it checks whether the selected image is imported and golden-tagged, and conditionally downloads from Cisco.com and tags as golden, waiting on each Catalyst Center task to complete.
5. **Offers two upgrade methodologies** — operators choose **Consolidated Upgrade** (distribute-if-needed + activate in one call) or **Distribute then Activate** (separate, individually confirmed distribution and activation phases).
6. **Built-in safety gates** — every destructive phase and the post-check require explicit confirmation prompts (`Proceed to Upgrade Image`, `Proceed to Distribute Image`, `Proceed to Activate Image`, `Proceed to Post Upgrade Checks`); declining halts the workflow cleanly with a descriptive status.
7. **Before/after verification** — pre-check and post-check diagnostic show commands are captured into a shared global SWIM inventory table, enabling state comparison across the upgrade.
8. **Reuses pagination utilities** — device inventory is gathered through Workflow 10.0 (`CATC-PaginatedDeviceInventory`), keeping inventory retrieval scalable and consistent.

### Logical Flow

The diagram below shows the full orchestration from site selection through parallel device collection, device family and target selection, pre-check against the cleansed list, image sync and per-site sanitization, the upgrade-method branch (with confirmation gates and halt paths), the gated post-check, and the final inventory update:

![Logical Flow](DIAGRAMS/logical-flow.png)

> Source: [`DIAGRAMS/logical-flow.mmd`](DIAGRAMS/logical-flow.mmd) — re-render with:
> ```bash
> npx -y @mermaid-js/mermaid-cli -i DIAGRAMS/logical-flow.mmd -o DIAGRAMS/logical-flow.png -w 1100 -b white
> ```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Cisco Catalyst Center | >= 2.3.7.9 |
| Workflow 1.0 — Site Hierarchy | Site hierarchy must exist in Catalyst Center |
| Workflow 10.0 — Paginated Device Inventory | `CATC-PaginatedDeviceInventory` and `CATC-DeviceInventory-v2` must be imported (called as a subworkflow) |
| `CATC-DynamicSiteSelector` subworkflow | Must be imported (provides the site selection UI and hierarchy JSON) |
| `CATC-MultipleShowCommands-v3` subworkflow | Must be imported (pre/post-check diagnostics via Command Runner) |
| `Get Task ID` / `Wait For Catalyst Center Task` | Atomic workflows used to poll SWIM tasks (download/tag golden) |
| `Create Image Uuid Array` / `String to Array` | Atomic helpers used by image deployment and array normalization |
| Devices assigned to sites | Target devices must be discovered, reachable, managed, and assigned to sites in the selected hierarchy |
| Cisco.com connectivity (for image sync/download) | Catalyst Center must be able to reach Cisco.com to sync and download images |
| Sufficient privileges in CatC | User/service account must have permission to download images, tag golden, distribute, and activate |

---

## Directory Structure

```
9.0 Cisco Catalyst Center: Site Based Upgrade/
├── Catalyst Center Site Based Upgrade.json  # Catalyst Center workflow definition (import via CatC UI)
├── DIAGRAMS/
│   ├── logical-flow.mmd                     # Mermaid diagram source — re-render with npx mermaid-cli
│   └── logical-flow.png                     # Rendered flowchart (referenced by this README)
└── README.md                                # This document
```

---

## Workflow Input Parameters

This workflow is **interactive** — most inputs are collected through prompts during execution rather than as launch-time parameters. The key operator decision points are:

| Prompt | Type | Options / Source | Description |
|--------|------|------------------|-------------|
| Select Site | site selector | Catalyst Center hierarchy (via `CATC-DynamicSiteSelector`) | Parent site to upgrade; all child sites are included automatically |
| Select Device Type | single select | Switches and Hubs / Routers / Wireless Controllers | Device family to target |
| Select Device Family | single select | Unique device types from initial target table (e.g., `Cisco Catalyst 9300 Switch`) | SWIM device family for image selection |
| Select Devices for Upgrade | multiselect | Filtered `Local-DeviceTable` | Final set of devices to upgrade — drives both the pre-check and the upgrade |
| Select Image | single select | Images returned for the family | Golden image to deploy |
| Image Upgrade Method | single select | Consolidated Upgrade Method / Distribute then Activate | Upgrade methodology |
| Proceed to Upgrade / Distribute / Activate Image | checkbox | — | Per-phase confirmation gates for the destructive image operations |
| Proceed to Post Upgrade Checks | checkbox | — | Confirmation gate before the post-check show commands are captured |

> **Note:** All prompts expire after 72 hours if unanswered.

---

## Internal Working Variables

These variables are managed automatically by the workflow.

| Variable | Type | Purpose |
|----------|------|---------|
| `HierarchyNames` | array | Parent and child site name hierarchies |
| `HierarchyUuid` | array | Parent and child site UUIDs (iterated for device collection and image tagging) |
| `HierarchyDeviceList` | array | Device IDs assigned to the selected sites |
| `DeviceTypeInventory` | string (JSON) | Filtered, reachable, managed inventory of the selected device type |
| `Output-DeviceTable` | table (output) | Target device table with `precheck`/`postcheck` columns |
| `Local-DeviceTable` | table | Per-family device table used to drive the multi-select prompt |
| `DeviceTargetUuidList` | array | UUIDs of devices selected for upgrade |
| `DeviceTargetList` | array | Hostnames of devices selected for upgrade |
| `DeviceType` | array | Selected device type tokens used by the inventory filter |
| `SWIMDeviceTypes` | array | Unique device types extracted from the initial target table |
| `SWIMFamilyIdentifier` | string | Device family identifier used for image queries |
| `selectedImageName` | string | Name of the chosen golden image |
| `selectedImageUuid` | string | UUID of the chosen golden image |
| `imageNameArray` | array | Image names presented in the Select Image prompt |
| `UpgradeMethod` | array | Upgrade methodology options |
| `showCommands` / `showCommandsArray` | string / array | Diagnostic show commands for pre/post-check |
| `DeviceUpdates` | table (output) | Working table written by `CATC-MultipleShowCommands-v3` |
| `Inventory Page Size` | integer | Pagination size passed to `CATC-PaginatedDeviceInventory` |
| `Device SWIM Inventory` (global) | table | Shared pre/post-check results table across subworkflows |

---

## How It Works

### Step 1 — Select Site

The `CATC-DynamicSiteSelector` subworkflow presents the Catalyst Center site hierarchy and returns the selected site and the full hierarchy JSON. A Python "Find Children" script then:

1. Locates the selected site by `siteNameHierarchy`.
2. Reads its `siteHierarchy` prefix.
3. Collects every site whose `siteHierarchy` starts with that prefix (the parent and all descendants).

The resulting site names and IDs are stored in `HierarchyNames` and `HierarchyUuid`.

---

### Step 2 — Device Selection

Step 2 is a single grouped phase that gathers, filters, and cleanses the device list, and resolves the SWIM family identifier — all **before** the pre-check runs. It is composed of five sub-stages.

**2a — Select Device Type**

A prompt asks the operator to select a single device type: **Switches and Hubs**, **Routers**, or **Wireless Controllers**. The selection is stored in `DeviceType` and drives the inventory filter.

**2b — Filter Devices (Parallel)**

A `logic.parallel` block runs two branches concurrently.

Branch 1 — Site-assigned devices: a `For Each` loop over `HierarchyUuid` calls

```
GET /dna/intent/api/v1/networkDevices/assignedToSite?siteId={siteId}&offset={offset}&limit={limit}
```

and a Python script appends each returned `deviceId` to `HierarchyDeviceList`.

Branch 2 — Filtered inventory: `CATC-PaginatedDeviceInventory` (Workflow 10.0) retrieves the full inventory, which is then filtered with JSONPath:

```
$.response[?(@.family == '<selected_type>'
            && @.reachabilityStatus == 'Reachable'
            && @.managementState == 'Managed')]
```

A Python script normalizes the result to an array and stores it in `DeviceTypeInventory`.

**2c — Build Initial Target Table**

The filtered inventory is converted to a table (`Read Table from JSON`). A `For Each` loop over the filtered devices checks whether each device's `instanceUuid` is present in `HierarchyDeviceList`:

| Branch | Condition | Action |
|--------|-----------|--------|
| Match | `instanceUuid ∈ HierarchyDeviceList` | Add row to `Output-DeviceTable` (initial target table) |
| No match | otherwise | Skip the device |

**2d — Select Device Family and Devices**

Unique device types are extracted from `Output-DeviceTable` into `SWIMDeviceTypes`, and the operator picks a specific **Device Family** (e.g., `Cisco Catalyst 9300 Switch`). A `Local-DeviceTable` is built for that family (JSONPath + `String to Array`), and a multiselect **Select Devices for Upgrade** prompt lets the operator choose the final target devices. The selection cleanses `DeviceTargetList`.

> **Why this order matters:** by collecting both the device family and the upgrade target list here, the pre-check in Step 3 runs **only** against the devices the operator intends to upgrade.

**2e — Resolve SWIM Family and Cleansed Targets**

The workflow resolves the SWIM device family identifier:

```
GET /dna/intent/api/v1/image/importation/device-family-identifiers
JSONPath: $..[?(@.deviceFamily == '<selected_family>')].deviceFamilyIdentifier
```

and stores it in `SWIMFamilyIdentifier`. A second `For Each` loop then rebuilds `Output-DeviceTable` containing only the operator-selected devices and populates `DeviceTargetUuidList` (instance UUIDs of the cleansed targets).

---

### Step 3 — Target Devices (Pre-check)

With the cleansed `Output-DeviceTable` in hand, the workflow:

1. Copies `Output-DeviceTable` into the global **Device SWIM Inventory** table.
2. Calls `CATC-MultipleShowCommands-v3` to run the diagnostic show commands against the target devices, writing the results into the `precheck` column.
3. Updates the working `DeviceUpdates` table and syncs the result back to the global **Device SWIM Inventory** table.

---

### Step 4 — Get SWIM Images

```
POST /dna/intent/api/v1/images/ccoSync                                  # sync from Cisco.com (continue on failure)
GET  /dna/intent/api/v1/images?productNameOrdinal={SWIMFamilyIdentifier}  # list candidate images
```

Image names are extracted (JSONPath + `String to Array`) into `imageNameArray` and presented in a **Select Image** prompt. The selected image's `id` is resolved via JSONPath and stored as `selectedImageName` and `selectedImageUuid`.

---

### Step 5 — Image Sanitization (per site)

A `For Each` loop over `HierarchyUuid` ensures the image is ready at each site:

```
GET /dna/intent/api/v1/images?siteId={siteId}
JSONPath: imported?  isGoldenTagged?
```

| Branch | Condition | Action |
|--------|-----------|--------|
| Imported, not golden | `imported == true && goldenTagged == false` | `POST images/{uuid}/sites/{siteId}/tagGolden` → `Get Task ID` → `Wait For Catalyst Center Task` |
| Not imported | `imported == false` | `POST images/{id}/download` → `Wait For Catalyst Center Task` → `tagGolden` → `Get Task ID` → `Wait For Catalyst Center Task` |

The `Get Task ID` and `Wait For Catalyst Center Task` atomic workflows handle task polling.

---

### Step 6 — Image Deployment

The `Create Image Uuid Array` atomic workflow builds the `imageUuidList` payload from `selectedImageUuid`. An **Image Upgrade Method** prompt then offers two paths:

**Consolidated Upgrade**

1. **Proceed to Upgrade Image** confirmation prompt.
2. If confirmed — `For Each` selected device:
   ```
   POST /dna/intent/api/v1/image/activation/device
   { deviceUpgradeMode: "currentlyExists", deviceUuid, distributeIfNeeded: "true", imageUuidList }
   ```
3. If declined — workflow halts: **"Image Not Activated - Process Halted"**.

**Distribute then Activate**

1. **Proceed to Distribute Image** confirmation prompt.
   - If confirmed — `For Each` selected device: `POST /dna/intent/api/v1/image/distribution` `{ deviceUuid, imageUuid }`.
   - If declined — halt: **"Image Not Distributed - Process Halted"**.
2. **Proceed to Activate Image** confirmation prompt.
   - If confirmed — `For Each` selected device: `POST /dna/intent/api/v1/image/activation/device`.
   - If declined — halt: **"Image Not Activated - Process Halted"**.

---

### Step 7 — Update Show Commands (Post-check)

A **Proceed to Post Upgrade Checks** confirmation prompt gates the post-check phase. When confirmed, `CATC-MultipleShowCommands-v3` runs the same diagnostic commands against the upgraded devices and writes the results into the `postcheck` column. The `DeviceUpdates` table and the global **Device SWIM Inventory** are updated, providing a before/after view of device state.

---

### Complete Device Inventory

A final `Set Multiple Variables` block (`Complete Device Inventory`) finalizes the global **Device SWIM Inventory** table so it is available to downstream workflows and as the workflow output.

---

## SWIM API Payload Reference

### Tag Image as Golden

`POST /dna/intent/api/v1/images/{imageUuid}/sites/{siteId}/tagGolden`

```json
{
  "productNameOrdinal": "<SWIMFamilyIdentifier>",
  "deviceRoles": ["UNKNOWN", "BORDER_ROUTER", "CORE", "DISTRIBUTION", "ACCESS"]
}
```

### Distribute Image

`POST /dna/intent/api/v1/image/distribution`

```json
[
  { "deviceUuid": "<device-uuid>", "imageUuid": "<image-uuid>" }
]
```

### Activate Image

`POST /dna/intent/api/v1/image/activation/device`

```json
[
  {
    "deviceUpgradeMode": "currentlyExists",
    "deviceUuid": "<device-uuid>",
    "distributeIfNeeded": "true",
    "imageUuidList": ["<image-uuid>"]
  }
]
```

**Key field notes:**

| Field | Notes |
|-------|-------|
| `distributeIfNeeded` | `"true"` allows the consolidated method to distribute the image if it is not already present before activating. |
| `deviceUpgradeMode` | `"currentlyExists"` activates the image already staged on the device. |
| `productNameOrdinal` | The SWIM device family identifier resolved in Step 2e. |
| `deviceRoles` | Roles for which the image is tagged golden at the site. |

---

## Subworkflows

| Subworkflow | Purpose |
|-------------|---------|
| `CATC-DynamicSiteSelector` | Presents the site hierarchy and returns the selected site plus the full hierarchy JSON. |
| `CATC-PaginatedDeviceInventory` | Workflow 10.0 — retrieves the full device inventory via pagination, with an optional device-type filter. |
| `CATC-MultipleShowCommands-v3` | Runs multiple show commands via Command Runner for pre-check and post-check diagnostics. |
| `Get Task ID` | Atomic workflow — extracts the Catalyst Center service task ID from an Intent API response. |
| `Wait For Catalyst Center Task` | Atomic workflow — polls task status until completion or failure (configurable interval and retries). |
| `String to Array` | Atomic workflow — normalizes a string into a JSON array (handles list literals, CSV, newline-separated values). |
| `Create Image Uuid Array` | Atomic workflow — builds the `imageUuidList` payload from `selectedImageUuid` for the activation call. |

---

## Running the Workflow

### Import the Workflow

1. In Catalyst Center, navigate to **Platform → Workflow Manager**.
2. Click **Import** and upload `Catalyst Center Site Based Upgrade.json`.
3. Ensure all required subworkflows are imported (see [Prerequisites](#prerequisites)), including Workflow 10.0's `CATC-PaginatedDeviceInventory`.
4. The workflow appears as **Catalyst Center Site Based Upgrade** in the workflow list.

### Execute the Workflow

1. Click **Run** on the imported workflow.
2. Select the **Catalyst Center target** when prompted (mandatory).
3. Answer the interactive prompts in sequence:
   - **Select Site** → parent site (child sites included automatically)
   - **Select Device Type** → Switches and Hubs / Routers / Wireless Controllers
   - **Select Device Family** → e.g., `Cisco Catalyst 9300 Switch`
   - **Select Devices for Upgrade** → multiselect from the cleansed target list
   - **Select Image** → golden image to deploy
   - **Image Upgrade Method** → Consolidated or Distribute then Activate
   - **Confirmation prompts** → confirm each destructive phase
4. Monitor progress in **Workflow Executions** → **Execution Details**.

---

## Expected Output

A successful run produces the following sequence in the workflow execution log:

```
Step 1       Site selected: Global/Campus/Building-1
             Hierarchy resolved: 1 parent + 3 child sites
Step 2a      Device Type selected: Switches and Hubs
Step 2b      (parallel)
             Branch 1: site-assigned devices collected → HierarchyDeviceList (24 devices)
             Branch 2: CATC-PaginatedDeviceInventory → filtered (Reachable+Managed) → 31 devices
Step 2c      Initial Output-DeviceTable built: 18 devices (in hierarchy + type + online)
Step 2d      Device Family selected: Cisco Catalyst 9300 Switch
             Devices selected for upgrade: 12 (cleansed DeviceTargetList)
Step 2e      SWIMFamilyIdentifier resolved
             Cleansed Output-DeviceTable rebuilt → DeviceTargetUuidList (12 entries)
Step 3       Global Device SWIM Inventory updated
             Pre-check show commands captured → precheck column populated
Step 4       images/ccoSync triggered
             Candidate images listed → Select Image: cat9k_iosxe.17.15.05.SPA.bin
             selectedImageUuid resolved
Step 5       Per-site image sanitization:
               Site Building-1/Floor-1: image imported, tagging golden → task complete
               Site Building-1/Floor-2: image not imported → download → golden → task complete
Step 6       Create Image Uuid Array → imageUuidList built
             Upgrade Method: Distribute then Activate
             Distribution confirmed → 12 devices distributed ✓
             Activation confirmed → 12 devices activated ✓
Step 7       Proceed to Post Upgrade Checks confirmed
             Post-check show commands captured → postcheck column populated
             DeviceUpdates + global Device SWIM Inventory updated
Completed    Complete Device Inventory finalized — site based upgrade completed successfully
```

---

## Workflow Ordering Dependency

This workflow orchestrates a complete site-based upgrade and depends on several supporting workflows.

| Workflow | Purpose | Depends on | Required before |
|----------|---------|------------|-----------------|
| 1.0 — Site Hierarchy | Creates Area / Building / Floor hierarchy | — | Yes — provides sites and device assignments |
| 3.0 — Device Discovery | Discovers devices and assigns them to sites | 1.0 | Yes — devices must exist and be assigned |
| 10.0 — Paginated Device Inventory | Full paginated device inventory utility | `CATC-DeviceInventory-v2` | **Yes — called as a subworkflow** |
| **9.0 — This workflow** | Site-based software image upgrade | 1.0, 3.0, 10.0, supporting subworkflows | — |

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| `No target devices found` | Selected hierarchy has no devices of the chosen type that are reachable and managed | Verify devices are discovered, reachable, managed, and assigned to the selected sites; confirm the device type matches. |
| `Site has no child sites` | Selected site is a leaf or the hierarchy prefix match returned only the parent | This is expected for leaf sites; the upgrade scopes to the selected site only. |
| `Image not listed for family` | `images/ccoSync` failed or the family identifier is wrong | Verify Cisco.com connectivity; confirm the selected Device Family resolves a valid `SWIMFamilyIdentifier`. |
| `Image download times out` | Slow Cisco.com download or insufficient wait retries | The download wait allows ~10 minutes (5 s × 120). Re-run; verify Cisco.com bandwidth and Catalyst Center disk space. |
| `Tag golden task fails` | Image not fully imported, or insufficient privileges | Ensure the image import completed before tagging; verify the account can tag golden images. |
| `Distribution or activation fails for a device` | Device unreachable, low storage, or unsupported image | Check device reachability and flash space; confirm the image is compatible with the device platform. |
| `Workflow halts after a confirmation prompt` | Operator declined a confirm gate | This is expected (safety gate). Re-run and confirm the phase to proceed. |
| `Pre/post-check columns empty` | `CATC-MultipleShowCommands-v3` failed or Command Runner unavailable | Verify the subworkflow is imported and Command Runner is functional; check device reachability. |

---

## Additional Notes

- **Hierarchy scoping:** Selecting a parent site includes all descendant sites (matched by `siteHierarchy` prefix). To upgrade a single floor only, select that floor directly.
- **Intersection logic:** A device is targeted only if it is simultaneously (1) assigned to a site in the hierarchy, (2) of the selected device type, (3) `Reachable`, and (4) `Managed`.
- **Selection drives the pre-check:** Device family and the multi-select upgrade list are collected in Step 2 **before** the pre-check, so `CATC-MultipleShowCommands-v3` runs only against the cleansed `DeviceTargetUuidList`.
- **Two upgrade methods:** Use **Consolidated** for a single distribute-if-needed + activate operation; use **Distribute then Activate** to stage images first and activate during a later maintenance window, with independent confirmation gates.
- **Safety gates:** Every destructive phase — plus the post-check (`Proceed to Post Upgrade Checks`) — requires explicit confirmation; declining halts the workflow with a clear status rather than proceeding.
- **Before/after verification:** Pre-check and post-check show commands are stored in the shared global **Device SWIM Inventory** table for state comparison across the upgrade.
- **Image preparation is idempotent:** Already-imported and already-golden images are left as-is; only missing images are downloaded and tagged.
- **Reuses Workflow 10.0:** Device inventory retrieval is delegated to `CATC-PaginatedDeviceInventory`, so keep Workflow 10.0 imported for this workflow to function.
