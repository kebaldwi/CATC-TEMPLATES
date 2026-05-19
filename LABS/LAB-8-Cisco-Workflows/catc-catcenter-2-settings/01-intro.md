# Assigning Settings and Credentials

In this module, we will use **Cisco Workflows** to apply **network settings** and **device credentials** to the site hierarchy that was created in the previous module. As with hierarchy, the source of truth is a `settings.json` file in this GitHub repository — the workflow reads it and drives the Catalyst Center Intent API to make reality match.

The same GitOps pattern from the hierarchy module reappears here: *GitHub as the source of truth, Cisco Workflows as the orchestration engine, Catalyst Center as the system of record.*

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Cisco Workflows Overview" style="width:100%; height:auto;">

## Settings and Credentials Background

The **Design** area of Catalyst Center is where you create the structure and framework of your network — including the network settings and device credentials that you apply to devices throughout your network.

Network settings and credentials are bound to the **site hierarchy** so they can be inherited from a parent site (e.g., `Global`) and selectively overridden in child sites (Area / Building / Floor). This is what allows operations teams to:

- Apply changes within scoped maintenance windows.
- Roll out changes progressively across regions, buildings, or floors without impacting the entire network.
- Keep a clear, deterministic view of where each setting actually comes from.

The settings and credentials this workflow applies cover the full set of design-level intent that Catalyst Center pushes down at provisioning time:

- **Network settings** — DNS, DHCP, NTP, SNMP, Syslog, Netflow, Timezone, Message-of-the-Day banner, and Client/Endpoint AAA (RADIUS/TACACS or ISE).
- **Device credentials** — CLI (SSH/Telnet) credentials, SNMP v2c read/write community strings, and NETCONF port credentials, plus the assignment of those credentials to the target site.

## Why Cisco Workflows for Settings & Credentials?

The workflow we will run in this module — `GitOps-BuildSettings-v3` — is a generic Catalyst Center workflow that calls the Catalyst Center **Intent API** (`/dna/intent/api/v1/network/{siteId}`, `/dna/intent/api/v1/global-credential`, `/dna/intent/api/v2/site/{siteId}/credential`) and the **GitHub Contents API**. It does the following on your behalf:

| Stage | What Happens |
|---|---|
| **1. List** | Lists all files in a GitHub directory (`Get-GitHub-Directory-v2`) |
| **2. Match** | Filters down to the target `settings.json` file |
| **3. Read** | Pulls the raw contents of `settings.json` (`Get-GitHub-File-v2`) |
| **4. Parse** | Converts the JSON array into hierarchy rows (Parent / Area / Building / Floor)</br> and extracts up to 35 settings/credential fields per row |
| **5. Apply** | For each row, `CATC-AssignSettings-v2`:<br>• Applies network settings — `POST /dna/intent/api/v1/network/{siteId}`<br>• Checks credentials — `GET /dna/intent/api/v1/global-credential`<br>• Creates credentials — `POST /dna/intent/api/v1/global-credential`<br>• Assigns credentials — `POST /dna/intent/api/v2/site/{siteId}/credential` |
| **6. Verify** | Resultant settings and credentials reflected in the workflow output |

Because the workflow checks for existing credentials before creating them, the run is **idempotent** — running it again with the same `settings.json` does not duplicate global credentials. To overwrite existing settings or credentials, set `FORCE Update = true`.

### Logical Flow

The diagram below shows the full decision and loop structure of `GitOps-BuildSettings-v3`, including the sub-flow that extracts 35 fields per row and the API invocation sequence executed by `CATC-AssignSettings-v2`:

![GitOps Build Settings — Logical Flow](../../../ASSETS/LABS/WORKFLOWS/diagrams/2.0-Cisco-Catalyst-Center-Settings-and-Credentials/DIAGRAMS/logical-flow.png)

> Full workflow reference: [Support/Resources/Cisco Workflows/2.0-Cisco-Catalyst-Center-Settings-and-Credentials/README.md](https://github.com/kebaldwi/TECOPS-2599/blob/main/Support/Resources/Cisco%20Workflows/2.0-Cisco-Catalyst-Center-Settings-and-Credentials/README.md)

## Source of Truth — `settings.json`

The same `settings.json` that defines the hierarchy also carries the network settings and device credentials per hierarchy row. Each top-level entry binds settings to a specific Area / Building / Floor:

```json
[
  {
    "HierarchyParent": "Global",
    "HierarchyArea": "NA",
    "HierarchyBldg": "HQ San Jose",
    "HierarchyFloor": "Floor 1",
    "network_settings": {
      "dns_server":   { "primary_ip_address": "8.8.8.8", "domain_name": "cisco.com" },
      "dhcp_server":  ["192.168.1.1"],
      "ntp_server":   ["pool.ntp.org"],
      "timezone":     "America/Los_Angeles",
      "client_and_endpoint_aaa": {
        "server_type": "ISE",
        "primary_server_address": "10.0.0.8",
        "protocol": "RADIUS",
        "shared_secret": "Cisco123!",
        "pan_address": "10.0.0.8"
      }
    },
    "device_credentials": {
      "cli_credential":     { "description": "HQ-SSH-Creds", "username": "netadmin", "password": "Cisco123!", "enable_password": "Cisco123!" },
      "snmp_v2c_read":      { "description": "HQ-SNMP-Read",  "read_community":  "public" },
      "snmp_v2c_write":     { "description": "HQ-SNMP-Write", "write_community": "private" },
      "netconf_credential": { "description": "HQ-NETCONF",    "netconf_port": 830 }
    }
  }
]
```

For this lab, the file lives at `Projects/BGP_EVPN/Settings/settings.json` in the `kebaldwi/TECOPS-2599` repository, and is the same file referenced by the default workflow input parameters (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`).

## What You Will Do in This Module

1. Open the **Cisco Workflows** dashboard and locate the `GitOps-BuildSettings-v3` workflow.
2. Review the input parameters:</br> (`GITHUB-OWNER`, `GITHUB-REPO`, `GITHUB-PATH`, `GITHUB-FILE`, `FORCE Update`, `TemplateHubProjectName`).
3. Run the workflow and observe each step from the **View Runs** panel.
4. Verify that **Network Settings**, **Device Credentials**, and **Telemetry** were applied correctly in Catalyst Center under **Design → Network Settings**.

> **Prerequisites:** **Completed** the previous module [**Building Hierarchy**](../catc-catcenter-1-hierarchy/01-intro.md). The site hierarchy referenced by each row in `settings.json` must already exist in Catalyst Center.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)