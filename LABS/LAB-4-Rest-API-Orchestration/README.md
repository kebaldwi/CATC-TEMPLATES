# REST API Orchestration with Postman

## Overview

This Lab is designed as a standalone lab to help customers with varying challenges in Automating and Orchestrating their network infrastructure. Within the lab, we will use various tools and techniques to Automate various tasks and orchestrate Catalyst Center.

## General Information

Until this point, we have used REST API for some basic setup tasks, but there are so many situations that can be solved or at least eased using REST API in conjunction with Catalyst Center. In this lab, we will use a complete set of REST API collections which will build upon the foundational knowledge acquired in the previous labs. For this lab, we will concentrate on Catalyst Center configuration and how Catalyst Center can be automated to perform various functions which we have already covered. 

This set of Labs is developed around a set of simple use cases to show both the power of Catalyst Center, the REST APIs, and easy methodologies for execution through Postman.

The lab will utilize a set of collections publicly shared on postman workspaces and those collections will also be expanded to keep in line with this lab.

> [!IMPORTANT] 
> Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Partner**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

## Lab Modules

The Story we will use will be the following, after orientation, we will first integrate ISE with Catalyst Center, and then construct our design. The design consists of a hierarchy, settings and credentials. With the hierarchy set, we still discover our pod devices assigned by the instructor and then deploy templates to the pod. After some time we will archive the configurations of the pod, and then collect the updated inventory. Finally, we will send a show CDP neighbor command to the equipment we have been assigned. 

The use cases we will cover are the following which you can access via the links below:

1. [**Postman Orientation**](./catc-catcenter-0-orientation/01-intro.md)
2. [**Building Hierarchy**](./catc-catcenter-1-hierarchy/01-intro.md)
3. [**Assign Settings and Credentials**](./catc-catcenter-2-settings/01-intro.md)
4. [**Device Discovery**](./catc-catcenter-3-discovery/01-intro.md)
5. [**Template Deployment**](./catc-catcenter-4-templates/01-intro.md)
6. [**Configuration Archive**](./catc-catcenter-5-archive/01-intro.md)
7. [**Retrieving Network Inventory**](./catc-catcenter-6-inventory/01-intro.md)
8. [**Running Show Commands**](./catc-catcenter-7-cmd-run/01-intro.md)

## Preparation Notes

The following section of the README contains information for DevNet Test Drive instructors.

### The DCLOUD Environment

For DevNet Test Drive events, use this environment: [**Catalyst Center pods for DevNet Test Drives v4**]()

The DCLOUD session includes the following equipment.

* Virtual Machines:
  * Catalyst Center 2.3.7.10 or better
  * Identity Services Engine (ISE) 3.4 Patch 3 or better (deployed)
  * Script Server - Ubuntu 20.04  or better
  * Windows 10 Jump Host 
  * Windows Server 2019 - Can be configured to provide identity, DHCP, DNS, etc.

* Virtual Networking Devices:
  * Catalyst 8000v Router - 17.06.01a IOS-XE Code
  * Catalyst 9300v Switch - 17.12.01 IOS-XE Code 

The following diagram shows the DCLOUD topology.

![DCLOUD LAB TOPOLOGY](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_A.png?raw=true)

The following diagram shows one of the CML pods topology.

![DCLOUD CML POD TOPOLOGY](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_B.png?raw=true)

### Management IPs:

This is the pod IP addressing schema that will be used to discover devices within the lab.
Your instructor will assign you a pod number:

| Pod: | Router:     | gi 1         | Switch 1:   | gi 0/0      | Switch2:    | gi 0/0      |
|------|-------------|--------------|-------------|-------------|-------------|-------------|
| 0    | c8000v-p0-1 | 198.18.140.1 | c9000v-p0-1 | 198.18.10.2 | c9000v-p0-2 | 198.18.20.2 |
| 1    | c8000v-p1-1 | 198.18.141.1 | c9000v-p1-1 | 198.18.11.2 | c9000v-p1-2 | 198.18.21.2 |
| 2    | c8000v-p2-1 | 198.18.142.1 | c9000v-p2-1 | 198.18.12.2 | c9000v-p2-2 | 198.18.22.2 |
| 3    | c8000v-p3-1 | 198.18.143.1 | c9000v-p3-1 | 198.18.13.2 | c9000v-p3-2 | 198.18.23.2 |
| 4    | c8000v-p4-1 | 198.18.144.1 | c9000v-p4-1 | 198.18.14.2 | c9000v-p4-2 | 198.18.24.2 |
| 5    | c8000v-p5-1 | 198.18.145.1 | c9000v-p5-1 | 198.18.15.2 | c9000v-p5-2 | 198.18.25.2 |
| 6    | c8000v-p6-1 | 198.18.146.1 | c9000v-p6-1 | 198.18.16.2 | c9000v-p6-2 | 198.18.26.2 |
| 7    | c8000v-p7-1 | 198.18.147.1 | c9000v-p7-1 | 198.18.17.2 | c9000v-p7-2 | 198.18.27.2 |
| 8    | c8000v-p8-1 | 198.18.148.1 | c9000v-p8-1 | 198.18.18.2 | c9000v-p8-2 | 198.18.28.2 |
| 9    | c8000v-p9-1 | 198.18.149.1 | c9000v-p9-1 | 198.18.19.2 | c9000v-p9-2 | 198.18.29.2 |

## Credentials:

| Platform:       | IP Address:    | Username | Password   | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| Router          | 198.18.14[X].1 | netadmin | C1sco12345 |
| Switch 1        | 198.18.1[X].2  | netadmin | C1sco12345 |
| Switch 2        | 198.18.2[X].2  | netadmin | C1sco12345 |

### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials from the session booked into the client to connect.

![DCLOUD VPN CONNECTION](../../ASSETS/COMMON/DCLOUD/VPN-to-DCLOUD.png)

### Tools Required

Please utilize the following tools to run the lab effectively and ensure they are installed on your workstation/laptop before attempting the lab.

1. Cisco AnyConnect VPN Client
2. Postman
3. Google Chrome

<details closed>
<summary> Expand section for Tools Required </summary>

#### Cisco AnyConnect VPN Client

This software is required to connect your workstation to Cisco dCloud. For an explanation of AnyConnect and how to use it with dCloud, please visit the following URL: 

- <a href="https://dcloud-cms.cisco.com/help/android_anyconnect" target="_blank">dCloud AnyConnect Documentation</a>

If you do not have the AnyConnect client, please visit. 

- <a href="https://dcloud-rtp-anyconnect.cisco.com" target="_blank">⬇︎AnyConnect Download Site⬇︎</a>

#### Postman

Postman is an API platform for building and using APIs. Postman simplifies each step of the API lifecycle and streamlines collaboration so you can create better APIs—faster.

Once Postman has been downloaded to your desktop, it is advisable to set up an account and sign in so that all your changes can be used within any system with the client or a web browser, much in the same way as a chrome or firefox profile work. This additional capability I have found instrumental when working in multiple environments. 

- <a href="https://www.postman.com/downloads/" target="_blank">⬇︎Postman Download⬇︎</a>

##### Postman Documentation

For an understanding of postman, please visit this site:

- <a href="https://learning.postman.com/docs/getting-started/introduction/" target="_blank">Postman Documentation</a>

#### Google Chrome

Google Chrome is the optimal browser of choice when working in the Catalyst Center UI. 

To download Google Chrome, please visit. 

- <a href="https://www.google.com/chrome/downloads/" target="_blank">⬇︎Chrome Download⬇︎</a>

</details>

## Summary

This lab is intended for educational purposes only. Use outside of a lab environment should be done at the operator's risk. Cisco assumes no liability for incorrect usage.

This lab is intended to help drive the adoption of REST API and will be added to over time with various use cases. The Public Workspace will also mirror the changes and be kept up to date. We hope this set of labs helps explain how the REST API may be used and goes a little further in helping define and document them.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Orientation Lab**](./catc-catcenter-0-orientation/01-intro.md)

> [**Return to LAB Main Menu**](../README.md)
