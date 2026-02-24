# Wireless Automation

> [!WARNING]
> For best results and if you have not ensured that the lab is functioning correctly. Please consider checking the readiness of the lab in this [DCLOUD LAB PREPARATION](../DCLOUD.md) section.

## Overview

This Lab is designed as a set of standalone labs to help customers with varying challenges in Automating and Orchestrating their wireless network infrastructure. Within the lab, we will use various tools and techniques to Automate various tasks and orchestrate Catalyst Center.

## General Information

Until this point, we have focused our efforts on the wired space and utilized templates, and REST-API to solve some basic to advanced use cases. In this lab, we will change our focus to deal with the wireless environment and utilize methods to deal with common tasks from a wireless automation point of view. This lab will build upon the foundational knowledge acquired in the previous labs. For this lab, we will concentrate on Catalyst Center configuration specific to Cisco Wireless and how Catalyst Center can be automated to perform various functions.

This page will serve as the landing page for this lab section due to the amount of content it will cover and the need to expand on it over time. 

> [!TIP]
> For many reasons and specifically with Wireless the **Wireless Settings**, and **Feature Templates** in the UI are the best way I can recommend for managing Wireless controllers at scale, **with** or **without** **Fabric**. </br></br>The reason, is that Per Device Configuration is just as it sounds iterating through settings on multiple controllers, whicch will never be as quick or nimble at scale as the UI. </br></br>We also **do not advocate** for building **templates** for **controllers** due to required radio resets that become painful at scale. This is elegantly solved by Wireless Intent.

## Lab Preparation

Please set up the lab using the following:

1. [**Lab Preparation**](./preparation.md)

## Lab Modules

The lab will be split into modules to concentrate on specific tasks. Each is designed to build your knowledge in specific areas and they will call out any dependancies on previous modules. We will cover are the following which you can access via the links below:

1. [**Wireless Controller Discovery or PnP**](./module1-ctrlpnpdiscovery.md)
2. [**WLAN Creation**](./module2-wlans.md)
   * [**2a PSK SSID Creation**](./module2a-psk.md)
   * [**2b iPSK SSID Creation**](./module2b-ipsk.md)
   * [**2c Enterprise 802.1x (EAP) SSID Creation**](./module2c-eap.md)
   * [**2d OPEN SSID Creation**](./module2d-open.md)
3. [**RF Profiles**](./module3-rfprofiles.md)
4. [**WLC Provisioning**](./module4-wlcprovisioning.md)
5. [**AP Provisioning**](./module5-approvisioning.md)
6. [**AI RF Profiles**](./module6-airfprofiles.md)
7. [**Application QoS**](./module7-applicationqos.md)
8. [**Model Based Config**](./module8-modelbasedconfig.md)
9. [**Wireless Templates**](./module9-wirelesstemplates.md)
10. [**Controller HA**](./module10-controllerha.md)

## Preparation

To complete this module, it's best to connect to the dCloud lab environment using your laptop so that you can get accustomed to and begin using the tools. If you cannot install postman, completing all tasks via the workstation in the DCLOUD environment is possible.

Our screenshots will all be from the jump host but remember you can use your laptop.

If you would like to connect to the DCLOUD environment, please ensure you install the following.

### Lab Requirements

This lab is designed to be run in Cisco dClouds - Enterprise Network Sandbox Lab. It was developed in version 4, including Catalyst Center 2.2.3.5 and equipment running at least 17.x versions of code. 

> [!IMPORTANT]
> Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Parter**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

> [!NOTE]
> While the RTP DC can facilitate the wireless automation, it lacks a wirelessly enabled workstation for testing.

1. [Cisco Enterprise Networks Hardware Sandbox West DC](https://dcloud2-sjc.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)
2. [Cisco Enterprise Networks Hardware Sandbox East DC](https://dcloud2-rtp.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)

This allows you to run these labs and gives not only an environment to try the various code samples, but also to develop and export your own code for use in your production environment. DCLOUD  provides for rapid and safe POC/POV on-demand environment without impacting production environments. DCLOUD also negates the need for shipping equipment, associated lead times, and licensing issues associated with setting up your own private testing environment. Please do adhere to the best practices for the DCLOUD environment when using it.

DCLOUD allows for use with a web-based browser client for VPN-less connectivity, as well as AnyConnect VPN client connectivity for those who prefer it. The labs are hosted in Cisco San Jose Facility (Select US East or US West Region when scheduling in DCLOUD). Choose the Cisco Enterprise Network Sandbox version you prefer. 

> [!IMPORTANT]
> To access this or any other content, including demonstrations, labs, and training in DCLOUD please work with your **Cisco Account team** or **Cisco Partner Account Team** directly. Your Account teams will make sure the session is scheduled and shared for you to use. Once booked follow the guide within Github to complete the tasks adhering to the best practices of the dCLOUD environment.

#### Components

The DCLOUD session includes the following equipment:

Virtual Machines:

    Catalyst Center 2.3.5.5 or better
    Identity Services Engine (ISE) 3.0 Patch 4 or better (deployed)
    Identity Services Engine (ISE) 3.0 (Not deployed)
    Stealthwatch 7.4.0 or better
    FlowCollector 7.4.0 or better
    Cisco Prime Infrastructure 3.10  or better
    Script Server - Ubuntu 20.04  or better
    Wireless LAN Controller - C9800 running IOS-XE Bengaluru 17.5.1 code or better
    Windows 10 Jump Host 
    Windows Server 2019 - Can be configured to provide identity, DHCP, DNS, etc.
    Windows 10 Clients

Hardware Devices:

    ISR 4451 Router - 17.06.01a IOS-XE Code
    Catalyst 9300 Switch - 17.06.01 IOS-XE Code with Embedded Wireless Controller (EWC) and ThousandEyes Enterprise Agent
    9130AX Access Points
    Silex Controllers (3 Wired NIC's and 1 Wireless NIC)

The lab envionment that is available is depicted here:

![json](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology3.png?raw=true "Import JSON")

## Lab Credentials:

| Platform:       | IP Address:    | Username | Password   | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| 9800-1          | 198.19.11.2    | admin    | C1sco12345 |
| 9800-2          | 198.19.11.3    | admin    | C1sco12345 |
| Router          | 198.18.133.145 | netadmin | C1sco12345 |
| Switch 1        | 198.18.128.22  | netadmin | C1sco12345 |
| Switch 2        | 198.18.128.23  | netadmin | C1sco12345 |
| AP-1            | DHCP Assigned  | Cisco    | Cisco      |
| AP-2            | DHCP Assigned  | Cisco    | Cisco      |

### Tools Required

Please utilize the following tools to run the lab effectively and ensure they are installed on your workstation/laptop before attempting the lab.

1. Cisco AnyConnect VPN Client
2. Postman
3. Google Chrome

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

## Summary

This lab is intended for educational purposes only. Use outside of a lab environment should be done at the operator's risk. Cisco assumes no liability for incorrect usage.

This lab is intended to help drive the adoption of Rest-API and will be added to over time with various use cases. The Public Workspace will also mirror the changes and be kept up to date. We hope this set of labs helps explain how the Rest-API may be used and goes a little further in helping define and document them.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Wireless Lab Preparation**](../LAB-2-Wireless-Automation/preparation.md)

> [**Return to LAB Main Menu**](../README.md)
