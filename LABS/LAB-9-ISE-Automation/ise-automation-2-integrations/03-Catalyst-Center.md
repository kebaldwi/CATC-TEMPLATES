# ISE Integration with Catalyst Center

## Overview

Cisco Catalyst Center integrates with Cisco Identity Services Engine (ISE) to enable secure, policy-based network segmentation and access control within enterprise networks. Catalyst Center acts as a centralized controller and analytics platform that discovers network devices and shares this information securely with ISE. Through this integration, policies created in Catalyst Center, such as scalable group tags (SGTs) for access control and segmentation, are enforced by ISE, which activates the underlying infrastructure to implement zero-trust security. The integration uses pxGrid for secure data sharing and REST APIs for communication, allowing Catalyst Center to provision devices with AAA/RADIUS configurations and maintain synchronized policy enforcement across wired and wireless infrastructure. This collaboration enhances network visibility, automates device onboarding, and supports consistent policy application to reduce risk and improve compliance.

## General Information

Much like some of the previous modules in this ISE Automation Lab, we are going to give you the option to do this integration via API - but also show you how it is done via the GUI.  Note that you only need to complete <b><i><u>one</u></i></b> option before proceeding to the Policy module.

>[!WARNING]
>You must have completed the following modules prior to continuing:

1. [**PKI Infrastructure**](../ise-automation-1-certificates/01-PKI-Infrastructure.md) from Lab 9 - Section 1 "Certificates"
2. [**Catalyst Center Certificate**](../ise-automation-1-certificates/02-Catatlyst-Center.md) from Lab 9 - Section 1 "Certificates"
3. [**ISE Certificates**](../ise-automation-1-certificates/03-ISE-Certificates.md) from Lab 9 - Section 1 "Certificates" (either via GUI or API)


>[!NOTE]
>:mega: If you have already completed the integration between Catalyst Center and ISE as part of the [Module 1 - PnP Prep](../../LAB-1-Wired-Automation/module1-pnpprep.md) from Lab 1, you may skip this module.<br><br>
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host. <br><br>

This module consists of the following sub modules:

1. [**Catalyst Center Integration - GUI**](./03a-Catalyst-Center-GUI.md)
2. [**Catalyst Center Integration - API**](./03b-Catalyst-Center-API.md)

