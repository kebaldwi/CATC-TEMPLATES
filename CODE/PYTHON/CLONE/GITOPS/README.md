# Python API Examples for TECOPS-2599

This directory contains Python reference implementations that mirror the Catalyst Center operations used by the Ansible projects in this repository.

The goal is both instructional and operational:
- Show the raw REST workflow behind each Ansible step
- Provide deterministic troubleshooting scripts when module behavior is unclear
- Keep numbering aligned with the Ansible progression

## What These Examples Cover

The Python projects now map to Ansible operations `1.0` through `8.0` (with template-oriented sub-steps under `6.x`):

1. `1.0` Build site hierarchy
2. `2.0` Apply network settings
3. `3.0` Configure global credentials
4. `4.0` Run device discovery
5. `5.0` Assign devices to sites
6. `6.1` Authenticate to Catalyst Center
7. `6.2` Create (or reuse) a template project
8. `6.3` Create and commit a member template
9. `6.4` Create and commit a composite template
10. `7.0` Build switching network profile payloads (optional apply mode)
11. `8.0` Deploy the composite template

## Directory Map

| Example | Path | Purpose |
|---|---|---|
| 1.0 | `1.0-Cisco-Catalyst-Center-Site-Hierarchy/site_hierarchy.py` | Create missing area/building/floor paths from settings data |
| 2.0 | `2.0-Cisco-Catalyst-Center-Settings/network_settings.py` | Build and apply per-site network settings payloads |
| 3.0 | `3.0-Cisco-Catalyst-Center-Credentials/credentials.py` | Create missing CLI/SNMP/NETCONF global credentials |
| 4.0 | `4.0-Cisco-Catalyst-Center-Device-Discovery/device_discovery.py` | Submit discovery jobs from `device_list` entries |
| 5.0 | `5.0-Cisco-Catalyst-Center-Assign-To-Site/assign_to_site.py` | Group devices by hierarchy path and assign to site UUIDs |
| 6.1 | `6.1-Cisco-Catalyst-Center-Templates-Authenticate/authenticate.py` | Obtain JWT token (`X-Auth-Token`) |
| 6.2 | `6.2-Cisco-Catalyst-Center-Templates-Create-Project/create_project.py` | Idempotent template-project lookup/create |
| 6.3 | `6.3-Cisco-Catalyst-Center-Templates-Create-Member-Template/create_member_template.py` | Create and commit a member template |
| 6.4 | `6.4-Cisco-Catalyst-Center-Templates-Create-Composite-Template/create_composite_template.py` | Create and commit a composite template |
| 7.0 | `7.0-Cisco-Catalyst-Center-Network-Profile/network_profile.py` | Build switching profile payloads and optionally POST to a custom endpoint |
| 8.0 | `8.0-Cisco-Catalyst-Center-Provision-Deploy-Composite/deploy_composite.py` | Build deploy payload and push composite to managed device |
| Shared | `common/helpers.py` | Common HTTP, auth, config, and task polling helpers |

## Ansible Relationship

These scripts are Python equivalents of workflow behavior in [Support/Resources/Ansible](Support/Resources/Ansible):

| Python Example | Underlying API Behavior | Ansible Behavior Illustrated |
|---|---|---|
| 1.0 Site Hierarchy | Site inventory + create site tasks | Area/building/floor hierarchy construction and parent-before-child ordering |
| 2.0 Settings | Per-site `PUT /network/{siteId}` updates | Composite network settings workflow and async status handling |
| 3.0 Credentials | Global credential queries and create tasks | CLI/SNMP/NETCONF credential lifecycle |
| 4.0 Discovery | Discovery submission per device group | Discovery workflow manager behavior |
| 5.0 Assign to Site | Site UUID lookup + assignment call | Device-to-site mapping and assignment |
| 6.1 Authenticate | `POST /dna/system/api/v1/auth/token` | API session bootstrap |
| 6.2 Create Project | `GET/POST /template-programmer/project` + task polling | Idempotent project management |
| 6.3 Member Template | Create + commit + version UUID resolution | Template lifecycle and version tracking |
| 6.4 Composite Template | Composite assembly via `containingTemplates` | Composite dependency and ordering behavior |
| 7.0 Network Profile | Settings-driven profile payload generation | Switching profile workflow-manager input shaping |
| 8.0 Deploy Composite | `POST /template-programmer/template/deploy` + task parsing | Provision/deploy execution and monitoring |

## Running the Examples

Set minimum environment variables:

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
```

Optional environment variables:

```bash
export CATC_PORT=443
export CATC_VERIFY_TLS=false
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
export CATC_DEVICE_IP=198.19.1.1
export CATC_PROJECT=DEBUG-PROJECT
export CATC_MEMBER=DEBUG-MEMBER.j2
export CATC_COMPOSITE=DEBUG-COMPOSITE.j2

# Step 7.0 optional apply mode
export CATC_APPLY_NETWORK_PROFILE=false
export CATC_NETWORK_PROFILE_ENDPOINT='/dna/intent/api/v1/network-profile/switching'
```

Recommended run order:

```bash
python3 1.0-Cisco-Catalyst-Center-Site-Hierarchy/site_hierarchy.py
python3 2.0-Cisco-Catalyst-Center-Settings/network_settings.py
python3 3.0-Cisco-Catalyst-Center-Credentials/credentials.py
python3 4.0-Cisco-Catalyst-Center-Device-Discovery/device_discovery.py
python3 5.0-Cisco-Catalyst-Center-Assign-To-Site/assign_to_site.py
python3 6.1-Cisco-Catalyst-Center-Templates-Authenticate/authenticate.py
python3 6.2-Cisco-Catalyst-Center-Templates-Create-Project/create_project.py
python3 6.3-Cisco-Catalyst-Center-Templates-Create-Member-Template/create_member_template.py
python3 6.4-Cisco-Catalyst-Center-Templates-Create-Composite-Template/create_composite_template.py
python3 7.0-Cisco-Catalyst-Center-Network-Profile/network_profile.py
python3 8.0-Cisco-Catalyst-Center-Provision-Deploy-Composite/deploy_composite.py
```

## Notes

- All scripts use only Python standard library calls for maximum transparency.
- Keep `CATC_VERIFY_TLS=true` in production.
- Continue using Ansible for normal operations; use these Python scripts for API-level validation and troubleshooting.