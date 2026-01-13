# Introduction to ISE Automation

This set of Cisco Learning Labs is developed to introduce you to some of the automation and Rest API functionality of Identity Services Engine (ISE), as well as augment your learning around Catalyst Center wired and wireless automation:  giving you the ability to quickly configure ISE in a way that allows you to test the functionality of what Catalyst Center deploys from earlier labs.

These Labs are designed for the Cisco DCLOUD - Catalyst Center pods for DevNet Test Drives Lab. It was developed for a Lab, which includes Catalyst Center 2.3.5.6 and equipment running at least 17.x versions of code.

## Identity Services Engine (ISE)

![json](../../../ASSETS/LABS/ISE/ISE-Overview.png?raw=true "Import JSON")

Cisco Identity Services Engine (ISE) is an identity-based network access control and policy enforcement system. It functions as a common policy engine that enables endpoint access control and network device administration for enterprises.

You can leverage Cisco ISE to ensure compliance, enhance infrastructure security, and streamline service operations.

A Cisco ISE administrator can gather real-time contextual data for a network, including users and user groups (who?), device type (what?), access time (when?), access location (where?), access type (wired, wireless, or VPN) (how?), and network threats and vulnerabilities.

As a Cisco ISE administrator, you can use this information to make network governance decisions. You can also tie identity data to various network elements to create policies that govern network access and usage.

## Lab Sections/Modules

These labs are organized in such a way that they will need to be completed ***in order*** to achieve an ISE deployment that can be used to test other use cases from earlier labs.

1. PKI and Certificates Setup. (Note that if you have already completed Labs 1 or 2 as part of this lab time slot, many of these tasks may be redundant)
2. ISE Integrations
3. Policy Elements and Sets
4. Testing with Lab PCs

## Prerequisites

To effectively run the Labs, install the following tools on your computer:

>[!NOTE]  
>Cisco AnyConnect VPN Client: Required to connect your workstation to Cisco DCLOUD. You can download it from the [AnyConnect Download Site](https://dcloud-rtp-anyconnect.cisco.com). For more information, refer to the [DCLOUD AnyConnect Documentation](https://dcloud-cms.cisco.com/help/android_anyconnect).<br><br>
>Postman: An API platform for building and using APIs. Download it from [the Postman website](https://www.postman.com/downloads/).<br><br>
>Google Chrome: Recommended for working in the Catalyst Center UI in these Labs. Download it from the [Chrome website](https://www.google.com/chrome/downloads/).<br><br>

### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials given by the **instructor** into the client to connect.

![DCLOUD VPN CONNECTION](../../../ASSETS/COMMON/DCLOUD/VPN-to-DCLOUD.png)

> [**Next Section**](./02-Collections.md)

> [**Return to LAB Menu**](../README.md)