# Lab Client Orientation

## Overview

Before we get into configuring the Network Access Policies on ISE to match up with the wireless SSIDs that were configured in [**Lab 2 - Wireless Automation**](../../LAB-2-Wireless-Automation/module2-wlans.md), it is important to become familiar with the end host(s) you will be using to test and troubleshoot the various configurations, and validate that they are ready for testing.  Additionally, we need to grab some information from the wireless adapter used in this lab in order to use it within our iPSK policy.

## General Information

>[!WARNING]
>You must have completed the [**PKI Infrastructure**](../ise-automation-1-certificates/01-PKI-Infrastructure.md) before completing this lab module.

This lab module consists of the following tasks:

1. [**Launching a Lab Client and Validating Certificates**](#launching-a-lab-client-and-validating-certificates)
2. [**Connecting to and Utilizing the SX Virtual Link**](#connecting-to-and-utilizing-the-sx-virtual-link)
3. [**Capturing the MAC Address of the USB Wireless Adapter**](#capturing-the-mac-address-of-the-usb-wireless-adapter)
4. [**Add the MAC Address to the Environment Variable in Postman**](#add-the-mac-address-to-the-environment-variable-in-postman)

## Launching a Lab Client and Validating Certificates

Please recall the lab topology diagram we've been working with:

![json](../../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_Wireless-v2.png?raw=true "Import JSON")

At the bottom of this diagram, you will notice four (4) Client PCs.  Each of these PCs is connected to the "management" wired network (the green box - containing ISE, Catalyst Center, AD Server, etc.).  At the time of this writing, these devices are simple Windows 10 PCs that have been added to the dcloud.cisco.com domain.  Since one of our wireless test cases includes EAP-TLS, which requires the use of certificates, we need to validate that the devices have obtained a computer certificate and a Trusted Root CA Certificate for this domain.

Complete the following tasks:

1. From the dCloud Session View, select any of the 4 client PCs and under ***Remote Access*** launch the ***Web RDP***

2. Once the client PC logs in, 

    1. Click on the Start Menu and 
    
    2. Type `certlm.msc`

    3. Click on "Run as administrator"

        ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-01.png?raw=true "Import JSON")

3. Expand ***Personal > Certificates*** and validate that a certificate corresponding to the Client PC you opened (ex: win10-client1 should have a certificate containing win10-client1)

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-02.png?raw=true "Import JSON")

4. Now expand ***Trusted Root Certification Authorities > Certificates*** and validate that a "CA" certificate exists in this store:

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-03.png?raw=true "Import JSON")

>[!IMPORTANT]
>Should either the Personal certificate or the Trusted CA Certificate from steps 3 or 4 above <b><i><u>NOT</u></i></b> exist, please launch Command Prompt from the affected Client PC and run the command `gpupdate /force` -- or contact your lab proctor for assistance.

## Connecting to and Utilizing the SX Virtual Link

Within each lab pod, in addition to the four Client PCs, there are two USB controllers that are shared among them.  Connected to these controllers are one (1) USB Wireless adapters and three (3) USB Ethernet adapters.  Connectivity between these adapters and the end hosts is facilitated by an application called "SX Virtual Link", which is installed on each of the 4 Client PCs.  To connect one of these adapters to a PC:

1. From the dCloud Session View, select any of the 4 client PCs and under ***Remote Access*** launch the ***Web RDP***

2. Once the client PC logs in, launch the "SX Virtual Link" software:

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-04.png?raw=true "Import JSON")

3. Double click on the icon to launch.  Once open, you can see the two USB Controllers, each with 2 adapters in "Available" state.

<div style="padding-left:40px;"><table><tr><td valign="top" width="100%">

1. Click on the Linksys WUSB6300

> [!NOTE]
> The name of your USB Wireless Adapter may vary depending on what POD you get.  If you have trouble figuring out which one is the Wireless adapter, get with your lab proctor for assistance.

2. There are two large circular buttons at the bottom.  The left button is to **Connect** the selected device, and the right button is to **Disconnect**.  Select the **Connect** button

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-05.png?raw=true "Import JSON")

</td></tr></table></div>

4. Open the "Control Panel" and navigate to **Network and Internet > Network and Sharing Center** and select ***Change adapter settings***

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-06.png?raw=true "Import JSON")

5. Here, we can see that the Linksys WUSB6300 device has connected and is showing as an available network adapter:

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-07.png?raw=true "Import JSON")

>[!NOTE]
>Leave this Linksys USB Adapter connected to whatever Client PC you're working on for now, as we will use it in the next step.

>[!IMPORTANT]
>As mentioned above, these USB adapters are <u>shared</u> across all 4 Client PCs via the SX Virtual Link software.  In reality, they are physical USB devices that are simply exposed to the SX Virtual Link software to simulate the ability to plug/unplug the devices from the PCs -- without having to physically be present in the lab to do so.  This means that if you "plug in" (ie: click the Connect button in the SX Virtual Link software) an adapter to one Client PC, such as the wireless Linksys USB in the example above, it will be <u><i><b>unavailable</b></i></u> for use on the other PCs unless it is first disconnected from PC it is connected to via the SX Virtual Link software.  Thankfully, the SX Virtual Link software makes it easy to see this as it will denote a device "in use" within the GUI.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-08.png?raw=true "Import JSON")

## Capturing the MAC Address of the USB Wireless Adapter

The next thing we need to do for this module is to capture the MAC address associated with your pod's specific wireless USB adapter for use in the iPSK configuration on Cisco ISE.  Assuming you've left it connected from the last section:

1. From the PC the USB Wireless Adapter is connected to, open a Command Prompt window and enter the command `ipconfig /all`

2. Here, we are looking for the "Physical Address" (ie: MAC Address) of the Wireless LAN adapter associated with the USB Wireless Adapter we plugged in.  Write this MAC address down somewhere, as we'll need it for the next step.

    ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-09.png?raw=true "Import JSON")


## Add the MAC Address to the Environment Variable in Postman

Now that we have the MAC address of the USB Wireless Adapter for your specific POD, we need to add this value to its respective environment variable in Postman for use in our API calls.

1. Open your Postman app, and on the left:

    1. Select ***Environments*** 

    2. Select ***lab-9-ise-automation-environment***

    3. Locate the variable called ***LAB-PC-MAC-ADD*** and in the "Value" field  

    4. Enter the MAC Address from the previous step in a two-byte, colon-separated format:  (ex: AA:BB:CC:DD:EE:FF)

        ![json](../../../ASSETS/LABS/ISE/ISE-LABPC-ORIENTATION-10.png?raw=true "Import JSON")



## "Forgetting" a Wireless Network After Testing

In your testing, you may want to play around with several different wireless configurations on the same client (specifically when it comes to the different EAP methods).  Unfortunately, the version of Windows running in the lab environment does not have a great way to quickly modify an existing Wireless Profile - they must be deleted (or "Forgotten") and then reconfigured.  To that end, here are the instructions on how to "Forget" a wireless network in Windows.

1. From your Client Lab PC:

    1. Click on the Network tray icon

    2. Choose ***Network and Internet Settings***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-24.png?raw=true "Import JSON")

2. In the window that opens:

    1. On the left, choose ***Wi-Fi***

    2. Select ***Manage Known Networks***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-23.png?raw=true "Import JSON")

3. Click on the wireless network configuration you want to Forget (if this is your first time reading this, you likely wont have anything here yet), and click "Forget"

4. Finally, while not necessarily required, its highly recommended that you reboot the Client Lab PC.  The Lab PCs can sometimes be finicky.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 


[**Custom Endpoint Attribute Creation**](./02-Custom-Endpoint-Attribute.md)

[**Return to ISE Automation Lab Overview**](../README.md)
