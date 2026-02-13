# Telemetry

## Overview

This module was created to review telemetry settings which are deployed to network devices when they are added to a site, either during the PnP process, as part of a **Discovery**, or by **assignment during provisioning**. During this section we will review the Telemetry settings within Catalyst Center. The Telemetry settings are used by Catalyst Center to configure network devices for the required settings required to enable the streaming telemetry to get the best results when viewing Assurance within Catalyst Center.

## General Information

Within this lab we will direct Netflow to Catalyst Center. It is important to understand that some networking devices have minimal allowed Netflow Exporters which can be configured. Should it be the case that you need addiitional flows to other servers or management devices, then please incorporate a UDP Flow Director in your design. This will allow the same flow to be replicated by the director to other management systems which require the feed.

During the course of the lab, you will have noticed that Telemetry settings were configured in the Design, and perhaps noticed that devices discovered and assigned to a site have had those telemetry settings pushed to them. You also may have noticed that there is a **Netconf warning** that may have appeared when you click the link it will filter in on the **c9300-1** which was claimed and onboarded and provisioned using the PnP process.

## Lab Section 1 - Reviewing Telemetry in the Design

In this lab we will enable the Telemetry Settings and Provision the new settings to a device on Catalyst Center.

<details open>
<summary> Click for Details and Sub Tasks</summary>

1. Navigate to the **Network Settings** within Catalyst Center through the menu *Design>Network Settings>*.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Navigate-Settings.png?raw=true "Import JSON")

2. Navigate to the **Telemetry** tab within the **Network Settings** page within Catalyst Center through the submenu.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Telemetry-Navigation-2.png?raw=true "Import JSON")

3. View the **Telemetry** settings within Catalyst Center. Until this point we have not provisioned Netflow onto the switch.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Telemetry-Settings.png?raw=true "Import JSON")

4. Select the checkbox next to **Use Catalyst Center as a Netflow Collector Server**. Then click **Save**.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Telemetry-Settings-NetFlow.png?raw=true "Import JSON")

5. Click **Okay** in the popup which appears.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Telemetry-Settings-Save.png?raw=true "Import JSON")

</details>

## Lab Section 2 - Provisioning Telemetry Configuration

If a device was onboarded via discovery and not added to a site then provisioning the telemetry settings might be carried out in this manner.

<details open>
<summary> Click for Details and Sub Tasks</summary></br>

1. Navigate to the **Inventory** within Catalyst Center through the menu **`Provision > Network Devices > Inventory`**.

   ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateInventory.png?raw=true "Import JSON")

2. From the inventory we can see a **Warning** about **`devices that have not been discovered with NETCONF`**. If we click the link the inventory will filter as shown on the troubled device. If at this point you see more devices they will disappear after the synchronization finishes. **Please allow time for that** 

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-1.png?raw=true "Import JSON")

3. As the issue is incorrect **NETCONF** credential settings we will fix that first. Select the switch **checkbox**, then click **Actions > Inventory > Edit Device** from the submenu.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-2.png?raw=true "Import JSON")

4. On the **Edit Device** page under **Credentials** scroll down and open up the **NETCONF** section and ensure port **830** is set. Then click **Update**

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-3.png?raw=true "Import JSON")

5. Now the credentials have been fixed lets redeploy Telemetry. Reselect the switch **checkbox**, then click **Actions > Telemetry > Update Telemetry Settings** from the submenu.

    ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-4.png?raw=true "Import JSON")

6. Click the **Force Configuration Push** checkbox, and click **Next**.

    ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-5.png?raw=true "Import JSON")

7. Click **Apply** to continue.

    ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-6.png?raw=true "Import JSON")

8. Verify the **Warning** for **NETCONF** is gone.

    ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-7.png?raw=true "Import JSON")

</details>

## Lab Section 3 - Reviewing Telemetry Configuration

In this section we will review the configuration that has been pushed to the device.

<details open>
<summary> Click for Details and Sub Tasks</summary>

1. Select the **Inventory** focus.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-1.png?raw=true "Import JSON")

2. Select the switch checkbox, then click **Actions > Inventory > Resync Device** from the submenu.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Resync.png?raw=true "Import JSON")

3. After a few moments of **syncing** the device will show in a managed state.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Telemetry-1.png?raw=true "Import JSON")

4. Click the actual name **ACCESS-c9300-1-ASW.dcloud.cisco.com** and from the page that appears select **configuration** from the sidebar menu.

   ![json](../../ASSETS/LABS/WIRED/DNAC-Provision-Config.png?raw=true "Import JSON")

Notice the Netflow configuation that has been pushed and additionally review the fully configured switch to see all the various telemetry settings whcih have been deployed from Syslog to SNMP.

</details>

At this point you have successfully built and deployed Telemety to a switch from Catalyst Center.

## Automating Telemetry

While it is possible to click through these processes manually, which can be time-consuming, we can handle this differently. We may automate them further via REST API.

## Summary

The next step will be to build Advanced Automation Templates in the network infrastructure. 

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Advanced Automation Lab**](./module6-advanced.md)

> [**Return to LAB Menu**](./README.md)
