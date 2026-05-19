# Introduction to Catalyst Center Orchestration with Cisco Workflows

## Overview

This Lab is designed as a standalone lab to help customers with varying challenges in Automating and Orchestrating their network infrastructure. Within the lab, we will use various tools and techniques to Automate various tasks and orchestrate Catalyst Center.

## Catalyst Center

![Cisco Catalyst Overview](../../../ASSETS/LABS/COMMON/cisco_catc.png)

Catalyst Center is an intelligent Automation and Assurance platform for the campus. Catalyst Center enables, simplified Day-0 through Day-N management of switching, routing, and wireless infrastructure. It also improves operations with AI/ML-enhanced analytics to streamline troubleshooting and provide actionable insights into the health of the network and the quality of experience for users and applications. Here are some of the capabilities of Catalyst Center in their respective domains:

* NetOps: Network Plug and Play for Zero Touch Deployment, Software Image Management, Compliance, Configuration Templates and Network Profiles, Model-Driven Configuration, and RMA Support.
* AIOps: AI/ML-enhanced monitoring and troubleshooting support. Predictive Insights, Network Baselines, Network Reasoner, Device/Client/Application 360, Intelligent Capture.
* SecOps: AI Endpoint Analytics, Group-Based Policy and Analytics, Software-Defined Access
* DevOps: ITSM Integrations, APIs, SDK & Ansible Module

## Network management is far too complex

Complexities of network environments that involve multiple devices, configurations, and policies. These environments often include legacy systems, various hardware types, and differing compliance requirements, making management incredibly challenging. 

The Networking Landscape complexity is increased with islands of management planes, discontiguous implementation flows, especially where multiple controllers are involved.

Double administration at times for monitoring which leads to wasted time, and inability to track change across it all.

![Managing Complex Environments](../../../ASSETS/LABS/WORKFLOWS/readme/COMPLEX.png?raw=true "Complex Environment")

## Complexity creates challenges for network and security teams

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/COMPLEXITY.png" alt="Workflow Properties" style="width:100%; height:auto;">

Complexity leads to inaccuracy which leads to failures. Error prone processes and troubleshooting cause a loss in time due to Management Plane sprawl which is compounded by the growth and demand of the networks today.

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/CHANGE.png" alt="Workflow Properties" style="width:100%; height:auto;">

* *What if it didn’t have to be that way.*
* *What if management planes could talk to one another, without fate sharing,
without complex integrations.*
* *What if this could somehow even be driven by events or even AI.*

## Cisco Workflows - *'What is it?'*

Meraki has added a well-established Cisco tool to the dashboard; Workflows. But let’s be very clear, it’s not just for Meraki. Customers can use this powerful automation and orchestration engine on pretty much anything. In addition to Meraki, it can be used for automating Cisco controllers like Catalyst Center, SD-WAN, ISE, ThousandEyes, ACI, Nexus Dashboard, Intersight, Webex, IOT, and anything Cisco or 3rd party that utilizes REST-API. If it has a REST API or an SSH adapter, Workflows can automate it.

<img src="../../../ASSETS/LABS/WORKFLOWS/readme/WORKFLOWS.png" alt="Workflow Properties" style="width:100%; height:auto;">

If you can use Microsoft Visio, you can use Workflows.

## Use Case Lab Approach

These Labs are organized as use cases, and each use case has an associated API Collection.

1. Building a Hierarchy
2. Defining Settings and Credentials
3. Device Discovery
4. Importing Templates
5. Building Network Profiles
6. Provisioning Devices

## Prerequisites

To effectively run the Labs, install the following tools on your computer:

> **NOTE**:  Cisco AnyConnect VPN Client: Required to connect your workstation to Cisco DCLOUD. You can download it from the [AnyConnect Download Site](https://dcloud-rtp-anyconnect.cisco.com). For more information, refer to the [DCLOUD AnyConnect Documentation](https://dcloud-cms.cisco.com/help/android_anyconnect).

> **NOTE**: Google Chrome: Recommended for working in the Catalyst Center UI in these Labs. Download it from the [Chrome website](https://www.google.com/chrome/downloads/).

### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials given by the **instructor** into the client to connect.

![DCLOUD VPN CONNECTION](../../../ASSETS/LABS/COMMON/VPN-to-DCLOUD.png?raw=true)

> [**Next Section**](./02-preparation.md)

> [**Return to LAB Menu**](../README.md)