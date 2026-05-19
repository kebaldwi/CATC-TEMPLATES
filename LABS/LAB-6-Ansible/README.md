# Catalyst Center Orchestration with Ansible

## Overview

This Lab is designed as a standalone lab to help customers with varying challenges in Automating and Orchestrating their network infrastructure. Within the lab, we will use the **Cisco Catalyst Center Ansible collections** (`cisco.catalystcenter` and `cisco.dnac`) to drive the Catalyst Center Intent API end-to-end — from an empty system through a fully provisioned fabric — entirely from version-controlled JSON in this GitHub repository.

## Network management is far too complex

Complexities of network environments that involve multiple devices, configurations, and policies. These environments often include legacy systems, various hardware types, and differing compliance requirements, making management incredibly challenging.

The Networking Landscape complexity is increased with islands of management planes, discontiguous implementation flows, especially where multiple controllers are involved. Double administration at times for monitoring leads to wasted time and an inability to track change across it all.

![Managing Complex Environments](../../ASSETS/LABS/ANSIBLE/readme/COMPLEX.png?raw=true "Complex Environment")

## Complexity creates challenges for network and security teams

<img src="../../ASSETS/LABS/ANSIBLE/readme/COMPLEXITY.png" alt="Complexity Drivers" style="width:100%; height:auto;">

Complexity leads to inaccuracy which leads to failures. Error-prone processes and troubleshooting cause a loss in time due to Management Plane sprawl, compounded by the growth and demand of the networks today.

* *What if it didn't have to be that way.*
* *What if a single declarative source of truth could drive the controller.*
* *What if every change could be peer-reviewed in Git, replayed at will, and run unattended.*

## Ansible for Catalyst Center — *'What is it?'*

Cisco publishes two Ansible collections that wrap the Catalyst Center Intent API:

* **`cisco.catalystcenter`** — newer collection aligned with the modern site-hierarchy model (areas, buildings, floors as typed resources).
* **`cisco.dnac`** — long-standing collection providing high-level **Workflow Manager** modules (discovery, credentials, templates, network profiles) that wrap multi-step API sequences into single idempotent tasks.

Together with `ansible.builtin.uri` for the handful of operations not yet covered by a module, these collections are sufficient to automate the entire Day-0 → Day-N lifecycle of a Catalyst Center managed network. Every playbook in this lab is **data-driven** — it reads the shared [`settings.json`](../../Projects/BGP_EVPN/Settings/settings.json) intent file and makes Catalyst Center match.

> Reference: [Support/Resources/Ansible](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/README.md) — full as-built documentation for every playbook used in this lab.

## General Information

This lab uses a complete set of Ansible playbooks that drive Catalyst Center through its REST APIs. The same `settings.json` consumed by the Cisco Workflows track is consumed here — only the orchestration engine changes. The playbooks are sequenced so that each one's outputs satisfy the next one's prerequisites.

> [!IMPORTANT]
> Please note that lab content in this repository is aligned with specific DCLOUD demonstrations that have to be scheduled by either a **Cisco Employee** or a **Cisco Partner**. If you are having trouble accessing the DCLOUD content, please get in touch with your **Local Cisco Account Team**.

## Lab Modules

The story is the following: after orientation, we construct our design (hierarchy + settings + credentials), discover our pod devices, import templates from GitHub, build a network profile, and finally provision the devices.

The use cases we will cover are the following — links open the first section of each module:

1. [**Orientation**](./catc-catcenter-0-orientation/01-intro.md)
2. [**Building Hierarchy**](./catc-catcenter-1-hierarchy/01-intro.md)
3. [**Settings and Credentials**](./catc-catcenter-2-settings/01-intro.md)
4. [**Device Discovery and Site Assignment**](./catc-catcenter-3-discovery/01-intro.md)
5. [**Templates from GitHub**](./catc-catcenter-4-templates/01-intro.md)
6. [**Network Profile**](./catc-catcenter-5-networkprofiles/01-intro.md)
7. [**Provisioning Devices**](./catc-catcenter-6-provisioning/01-intro.md)

> A companion playbook — [10.0 Backup My Configs](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/10.0-Backup-My-Configs/README.md) — archives running configurations from all IOS-XE and NX-OS devices via SSH. It is not part of the seven lab modules but is recommended as a periodic operational task.

## Preparation Notes

The following section of the README contains information for the lab.

### The DCLOUD Environment

Use this environment: [**Catalyst Center + ISE Lab for Automation & Orchestration**](https://dcloud2.cisco.com/demo/catalyst-center-ise-lab-for-automation-orchestration)

The DCLOUD session includes the following equipment.

* Virtual Machines:
  * Catalyst Center 2.3.7.10 or better
  * Identity Services Engine (ISE) 3.4 Patch 3 or better (deployed)
  * Script Server — Ubuntu 22.04 or 24.04 (this is where Ansible runs)
  * Windows 10 Jump Host
  * Windows Server 2019 — identity, DHCP, DNS
  * vSphere 8.0 / ESXi Host

* Virtual Networking Devices:
  * Catalyst 8000v Router — 17.16.01a IOS-XE Code
  * Catalyst 9000v Switch — 17.15.03 IOS-XE Code
  * Cisco Nexus 9000v Switch — 10.5.3 Code

The following diagram shows the DCLOUD topology.

![DCLOUD LAB TOPOLOGY](../../ASSETS/LABS/COMMON/DCLOUD_Topology_A.png?raw=true)

### Access and Credentials:

| Platform:       | IP Address:    | Username      | Password    |
|-----------------|----------------|---------------|-------------|
| Catalyst Center | 198.18.129.100 | admin         | C1sco12345  |
| ISE             | 198.18.133.27  | admin         | C1sco12345  |
| Windows AD      | 198.18.133.1   | admin         | C1sco12345  |
| Script Server   | 198.18.133.28  | root          | C1sco12345  |
| vSphere Server  | 198.18.134.80  | Administrator | C1sco12345! |
| CML Server      | 198.18.128.11  | Guest         | C1sco12345  |

> All Ansible playbooks in this lab are run from the **Script Server** (`198.18.133.28`). The `install-ansible.sh` bootstrap script bundled with the playbooks installs Python 3.9, the `cisco.catalystcenter` and `cisco.dnac` collections, and creates an isolated venv at `~/tecops-venv`.

#### Large Branch Topology

The following diagram shows one of the CML pods topology.

![DCLOUD CML LARGE CAMPUS TOPOLOGY](../../ASSETS/LABS/COMMON/DCLOUD_Topology_B.png?raw=true)

| Platform:  | OOB Mgmt:      | Loopback 0: | Username  | Password   |
|------------|----------------|-------------|-----------|------------|
| Spine-01   | 198.18.128.101 | 198.19.1.1  | net-admin | C1sco12345 |
| Spine-02   | 198.18.128.102 | 198.19.1.2  | net-admin | C1sco12345 |
| Border-01  | 198.18.128.103 | 198.19.1.3  | netadmin  | C1sco12345 |
| Border-02  | 198.18.128.104 | 198.19.1.4  | netadmin  | C1sco12345 |
| Leaf-01    | 198.18.128.105 | 198.19.1.5  | netadmin  | C1sco12345 |
| Leaf-02    | 198.18.128.106 | 198.19.1.6  | netadmin  | C1sco12345 |

#### Small Branch Topology

The following diagram shows one of the CML pods topology.

![DCLOUD CML SMALL BRANCH TOPOLOGY](../../ASSETS/LABS/COMMON/DCLOUD_Topology_C.png?raw=true)

| Platform: | IP Address:  | Username | Password   |
|-----------|--------------|----------|------------|
| Router    | 198.18.140.1 | netadmin | C1sco12345 |
| Switch 1  | 198.18.10.2  | netadmin | C1sco12345 |
| Switch 2  | 198.18.20.2  | netadmin | C1sco12345 |

### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials from the session booked into the client to connect.

![DCLOUD VPN CONNECTION](../../ASSETS/LABS/COMMON/VPN-to-DCLOUD.png?raw=true)

### Tools Required

Please ensure the following tools are installed on your workstation/laptop before attempting the lab.

1. Cisco AnyConnect VPN Client
2. Google Chrome
3. An SSH client (built-in `ssh` on macOS/Linux; PuTTY or Windows Terminal on Windows)

<details closed>
<summary> Expand section for Tools Required </summary>

#### Cisco AnyConnect VPN Client

Required to connect your workstation to Cisco dCloud. For an explanation of AnyConnect and how to use it with dCloud, please visit:

- <a href="https://dcloud-cms.cisco.com/help/android_anyconnect" target="_blank">dCloud AnyConnect Documentation</a>

If you do not have the AnyConnect client, please visit:

- <a href="https://dcloud-rtp-anyconnect.cisco.com" target="_blank">⬇︎AnyConnect Download Site⬇︎</a>

#### Google Chrome

Google Chrome is the optimal browser when working in the Catalyst Center UI.

- <a href="https://www.google.com/chrome/downloads/" target="_blank">⬇︎Chrome Download⬇︎</a>

#### Ansible

Ansible itself does **not** need to be installed on your laptop. The orientation module installs it on the DCLOUD Script Server via the bundled [`install-ansible.sh`](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/install-ansible.sh) script. If you want to inspect the playbook source locally, any text editor (VS Code recommended) works.

</details>

## Summary

This lab is intended for educational purposes only. Use outside of a lab environment should be done at the operator's risk. Cisco assumes no liability for incorrect usage.

This lab is intended to help drive the adoption of Infrastructure-as-Code patterns against Catalyst Center, and will be added to over time with additional use cases.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on the feedback form [give feedback](https://github.com/kebaldwi/TECOPS-2599/discussions/new?category=feedback-and-ideas).</br></br>
> **Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please open an [issue](https://github.com/kebaldwi/TECOPS-2599/issues/new) including the file path along with the issue you ran into.

> [**Continue to Orientation Lab**](./catc-catcenter-0-orientation/01-intro.md)

> [**Return to LAB Main Menu**](../README.md)
