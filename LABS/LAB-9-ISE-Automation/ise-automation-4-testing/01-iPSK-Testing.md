# iPSK Testing

## Overview

In this module we will be testing the wireless connectivity using the iPSK mechanism setup as part of [***Lab 2 - Module 2b (iPSK)](../../LAB-2-Wireless-Automation/module2b-ipsk.md) and the ISE Policies we setup in the previous Lab 9 Section.

## General Information

>[!WARNING]
>You must have completed all of [***Lab 2 - Wireless Automation***](../../LAB-2-Wireless-Automation/) and all of the Lab 9 modules up to this point before attempting this lab module.

This lab module consists of the following tasks:

1. [***Enable iPSK Rules in ISE***](#enable-ipsk-rules-in-ise)
2. [***Connect Lab PC to iPSK SSID***](#connect-lab-pc-to-ipsk-ssid)
3. [***Validate ISE Radius Live Logs***](#validate-ise-radius-live-logs)
4. [***Session Termination***](#session-termination)

## Enable iPSK Rules in ISE

Complete the following tasks:

1. From your workstation/jumpbox, open Chrome browser and navigate ISE via http://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From the hamburger menu in the top left:

    1. Select ***Policy***, then

    2. ***Policy Sets***

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-12.png?raw=true "Import JSON")

3. On this screen we should see:

    1. Our "DCLOUD-LAB-POLICY", with Conditions of `DEVICE-Device Type EQUALS All Device Types` and under "Allowed Protocols" `Default Network Access`

    2. Click the blue arrow to expand the policy

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-13.png?raw=true "Import JSON")

4. Click on ***Authentication Policy*** to expand it

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-14.png?raw=true "Import JSON")

5. For the rule named "iPSK-AuthN"

    1. Select the gray circle/X icon

    2. Choose ***Enabled***

    3. Click ***Save*** in the top right hand corner

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-01.png?raw=true "Import JSON")

6. Scroll down and click on ***Authorization Policy*** to expand it

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-02.png?raw=true "Import JSON")

7. For the rule named "iPSK-AuthZ":

    1. Select the gray circle/X icon

    2. Choose ***Enabled***

    3. Click ***Save*** in the bottom right hand corner

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-03.png?raw=true "Import JSON")

## Connect Lab PC to iPSK SSID

>[!IMPORTANT]
>Please use the same Lab PC that you used to setup the MAC Address of the USB Wireless Adapter in [***Section 3 - Policy:  Module 1: Lab Client Orientation***](../ise-automation-3-policy/01-Lab-Client-Orientation.md) and [***Module 3:  Policy Configurations***](../ise-automation-3-policy/03-Policy-Configurations-API.md).  Otherwise you will have to configure a new Internal Endpoint with whatever MAC address it is using in order for those iPSK configurations to work.

1. From the Client PC:

    1. Click the Network tray icon

    2. Select the "CAMPUS-iPSK-POD#" SSID associated to your POD #

    3. Choose ***Connect***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-04.png?raw=true "Import JSON")

    4. Enter the iPSK key of "Cisco6789" (no quotes) that we setup as part of the Policy APIs in the last section and click ***Next***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-05.png?raw=true "Import JSON")

    5. If you get this screen, choose ***Yes***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-06.png?raw=true "Import JSON")

## Validate ISE Radius Live Logs

1. From the Windows Jump Host, open a web browser and navigate to ISE via https://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From the hamburger menu in the top left:

    1. Select ***Operations*** then

    2. Under "RADIUS" Select ***Live Logs***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-07.png?raw=true "Import JSON")

3. From this page, we should see a successful client policy pass for the MAC address of your Client Lab PC.  Click on the Details icon next to the Authentication Report (Next to the Green Check):

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-08.png?raw=true "Import JSON")

4. This long page provides all of the details of the connection request as received by ISE.  Scroll to locate the "Other Attributes" section, then locate the ***iPSK*** value.  Here you can see the iPSK that the Client PC submitted:

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-09.png?raw=true "Import JSON")

We now have a successful iPSK test!


## Session Termination

ISE maintains a "session" for any endpoints for a certain amount of time, even if those endpoints drop off the wireless network.  Since we're going to be testing multiple different ISE Policy mechanisms in relatively rapid sequence using <u>the same</u> host/USB Wireless Adapter, we don't want a previously authenticated session to muddle with our attempts at creating a new session using a different policy.  This means we should disconnect from the SSID on the Client LAB PC <b><u>AND</u></b> clear out the session from ISE.  To do so:

1. On the Client Lab PC

    1. Click on the Network tray icon

    2. Select whichever SSID you're currently testing, and choose ***Disconnect***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-26.png?raw=true "Import JSON")

>[!NOTE]
>The image above shows as connected to the "EAP" SSID, but choose whichever is accurate for whatever test you're currently on.

Then, from your Windows Jumphost:

1. From the ISE GUI hamburger menu in the top left:

    1. Select ***Context Visibility*** and then

    2. ***Endpoints***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-25.png?raw=true "Import JSON")

2. Locate your device based on MAC Address (there's likely only one in the list anyway)

    1. Place a check in the box next to the MAC address of your wireless client

    2. Select ***Change Authorization*** dropdown

    3. Select ***CoA Session Terminate***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-27.png?raw=true "Import JSON")

:mega::mega::mega:
>[!NOTE]
> It is advised that you go back into the DCLOUD-LAB-POLICY and "Disable" both the Authentication and Authorization policies that you enabled before, prior to testing the next mechanism.  Please reference the screenshots from the "Enable" section above if you need a reminder of where those are at!

:mega::mega::mega:

>[!IMPORTANT]
>**Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into.

> [**Continue to EAP-TLS Testing**](../ise-automation-4-testing/02-EAP-TLS-Testing.md)

> [**Return to ISE Automation Lab Overview**](../README.md)