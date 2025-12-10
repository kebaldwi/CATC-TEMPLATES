# DNAC-TEMPLATE LABS [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

## Overview

This section of the repository is built out in LAB form to guide you through the typical steps required to enable the various automation tasks delivered by Catalyst Center. This lab will give examples of templates used in Catalyst Center that can be modified for your use and tested on equipment within the LAB environment. Additional information within the lab provides a well-rounded explanation of Automation methods with Templates. Lastly, the lab allows for customers to use Catalyst Center workflows to practice deploying Onboarding, DayN Templates, and Application Policy automation on both Wired and Wireless Platforms.

The goal of this lab is for it to be a practical guide to aid engineers to rapidly begin using Catalyst Center automation and help them work towards a template strategy. Additionally, this lab will give customers a permanent place to try out the templates and include configurations for various use cases. This environment will enable engineers to reduce the time and effort needed to instantiate the network.

As a result, customers will gain experience setting up Plug and Play onboarding and templates. Additionally, they will use advanced velocity templating and troubleshooting tools, which may help during faultfinding to determine what is failing in a deployment.

## Labs

Please use this menu to navigate the various sections of this Github repository. Within the multiple folders are examples, explanation readme files for reference.

**IMPORTANT:** Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Parter**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

### New Catalyst Center Lab Content

This newer and more modular lab approach is designed to deal with and includes concepts from the legacy labs in a newer more modular format.

1. [Lab 1 Wired Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation) - Covers green and brown field use cases **(allow 4.0 hrs)**
2. [Lab 2 Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation) - Covers traditional wireless automation  **(allow 4.0 hrs)**
2. [Lab 3 Advanced Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-3-Advanced-Automation) - Covers how to build templates and logic  **(allow 4.0 hrs)**
4. [Lab 4 Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - Covers [Postman](https://www.postman.com) automation and orchestration of Catalyst Center **(allow 2.0 hrs)**
5. Lab 5 Python Orchestration - In Development - Covers Python automation and orchestration of Catalyst Center **(allow 3.0 hrs)**
6. Lab 6 Ansible Orchestration - In Development - Covers Ansible automation and orchestration Catalyst Center **(allow 3.0 hrs)**
7. [Lab 7 CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) - Covers [Python](https://www.python.org) with [JENKINS](https://www.jenkins.io) orchestration via REST-API **(allow 4.0 hrs)**
8. [Lab 8 Cisco Workflows](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-8-Cisco-Workflows/) - Covers orchestration via REST-API **(allow TBD hrs)**
9. [Lab 9 ISE Automation](  https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-9-ISE-Automation) - Covers how to automate ISE **(allow 4.0 hrs)**

### Legacy Lab Content

In this legacy lab section you will continue to find all the existing labs which deal with specifics in separate easy to do labs. This set of labs is being depricated due to new content above.

<details closed>
<summary> Expand section for Legacy Lab Content if required </summary></br>

* [PnP Preparation](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module1-pnpprep.md) - The lab covers setup for Plug and Play **(allow 1.5 hrs)**
* [Onboarding Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module2-pnp.md) - The lab covers in depth topics in deploying Day 0 templates **(allow 1.5 hrs)**
* [Day N Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - The lab covers Day N template constructs and use cases **(allow 0.5 hrs)**
* [Composite Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - This lab covers building a composite template on Catalyst Center **(allow 0.5 hrs)**
* [Application Policys](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automationy/module4-applicationqos.md) - This lab covers Application Policy & SDAVC in Catalyst Center **(allow 1.0 hrs)**
* [Telemetry](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module5-telemetry.md) - This lab explains how to deploy Streaming Telemetry for Catalyst Center Assurance **(allow 0.5 hrs)**
* [Advanced Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module6-advanced.md) - This lab will explore Advanced Automation examples **(allow 1.5 hrs)**
* [Dynamic Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-3-Advanced-Automation/) - This lab will explore additional Advanced Automation examples **(allow 2.0 hrs)**
* [Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - This lab uses [Postman](https://www.postman.com) Collections to automate Catalyst Center **(allow 2.0 hrs)**
* [Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation/) - This lab covers Traditional Wireless Automation  **(allow 6.0 hrs)**
* [Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-K-Orchestration/) - This lab covers [Postman](https://www.postman.com) and [Ansible](https://www.ansible.com) orchestration **(allow 4.0 hrs)**
* [CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) This lab covers [Python](https://www.python.org), [Ansible](https://www.ansible.com) and [JENKINS](https://www.jenkins.io) to orchestrate via REST-API **(allow 4.0 hrs)**

</details>

## DCLOUD as a LAB

### Overview

This section will explain which lab to utilize within the **DCLOUD** environment to run these labs. It will also discuss a customer POC environment and the steps necessary to successfully run these sections within a customer environment for localized testing.

### DCLOUD Labs

This lab environment has been tested on the following DCLOUD session

#### Overview

As a quick start with Catalyst Center Automation, you may utilize the above labs in conjuction with DCLOUD's sandbox:

1. [Cisco Enterprise Networks Hardware Sandbox West DC](https://DCLOUD2-sjc.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)
2. [Cisco Enterprise Networks Hardware Sandbox East DC](https://DCLOUD2-rtp.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)

This allows you to run these labs and gives not only an environment to try the various code samples, but also to develop and export your own code for use in your production environment. DCLOUD  provides for rapid and safe POC/POV on-demand environment without impacting production environments. DCLOUD also negates the need for shipping equipment, associated lead times, and licensing issues associated with setting up your own private testing environment. Please do adhere to the best practices for the DCLOUD environment when using it.

DCLOUD allows for use with a web-based browser client for VPN-less connectivity, as well as AnyConnect VPN client connectivity for those who prefer it. The labs are hosted in Cisco San Jose Facility (Select US East or US West Region when scheduling in DCLOUD). Choose the Cisco Enterprise Network Sandbox version you prefer. 

>**Note:** To access this or any other content, including demonstrations, labs, and training in DCLOUD please work with your Cisco Account team or Cisco Partner Account Team directly. Your Account teams will make sure the session is scheduled and shared for you to use. Once booked follow the guide within Github to complete the tasks adhering to the best practices of the DCLOUD environment.

#### Components

The DCLOUD session includes the following equipment:

Virtual Machines:

    Catalyst Center 2.2.3.4 or better
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

![json](../ASSETS/COMMON/DCLOUD/DCLOUD_Topology3.png?raw=true "Import JSON")

#### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials from the session booked into the client to connect.

![json](../ASSETS/COMMON/DCLOUD/VPN-to-DCLOUD.png?raw=true "Import JSON")

#### DCLOUD LAB Preparation

In order to prepare the lab for use with this section of the repository please ensure that you prepare the lab according to the information detailed in the [DCLOUD LAB PREPARATION](./DCLOUD.md) section.

> [!TIP]
> If this is the first time you have used these labs it is worth going through the LAB preparation documentation to ensure that the lab is functioning correctly. Please consider checking the readiness of the lab in this [DCLOUD LAB PREPARATION](./DCLOUD.md) section.

## Disclaimer

Various labs are designed for use in the **DCLOUD** environment but can but are for use elsewhere. What is important to realize is the impact of each type of test. For instance, in the ***PnP Preparation*** lab, we go through discovery methods such as ***option 43*** and ***DNS Discovery***. If we were to use the DHCP option 43 and place that in the server options on the DHCP server, it would affect multiple scopes. **Care** is required, therefore, to ensure you do not get unexpected results. Similarly with ***DNS Discovery***, if the sub domain used was available to all devices, more than one device would discover Catalyst Center. Changes like this may be suitable for production in the future but detrimental during testing.

The environment allows for use with a web-based browser client for VPN-less connectivity, access as well as AnyConnect VPN client connectivity for those who prefer it. The labs are hosted out of our San Jose and RTP Facilities and so you would choose sessions from either US East or US West. Choose the Cisco Enterprise Network Sandbox v3 or v4. To access this or any other content, including demonstrations, labs, and training in Cloud please work with your Cisco Account team or Cisco Partner Account Team directly. Your Account teams will make sure the session is scheduled and shared for you to use. Once booked follow the guide within Github to complete the tasks adhering to the best practices of the DCLOUD environment.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](../README.md)