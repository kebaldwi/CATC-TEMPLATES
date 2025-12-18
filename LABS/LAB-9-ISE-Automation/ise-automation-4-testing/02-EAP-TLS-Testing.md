# EAP-TLS Testing

## Overview

In this module we will be testing the wireless connectivity using the EAP-TLS mechanism setup as part of [***Lab 2 - Module 2c (EAP)](../../LAB-2-Wireless-Automation/module2c-eap.md) and the ISE Policies we setup in the previous Lab 9 Section.

## General Information

>[!WARNING]
>You must have completed all of [***Lab 2 - Wireless Automation***](../../LAB-2-Wireless-Automation/) and Lab 9 modules 0 through 3 before attempting this lab module.

This lab module consists of the following tasks:

1. [***Enable EAP-TLS Rules in ISE***](#enable-eap-tls-rules-in-ise)
2. [***Configure and Connect Lab PC to EAP SSID***](#configure-and-connect-lab-pc-to-eap-ssid)
3. [***Validate ISE Radius Live Logs***](#validate-ise-radius-live-logs)
4. [***Session Termination***](#session-termination)


## Enable EAP-TLS Rules in ISE

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

5. For the rule named "EAP-TLS-AuthN":

    1. Select the gray circle/X icon
    
    2. Choose ***Enabled***
    
    3. Click ***Save*** in the top right hand corner
    
        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-10.png?raw=true "Import JSON")

6. Scroll down and click on ***Authorization Policy*** to expand it

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-02.png?raw=true "Import JSON")

7. For the rule named "EAP-TLS-AuthZ":

    1. Select the gray circle/X icon

    2. Choose ***Enabled***

    3. Click ***Save*** in the bottom right hand corner

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-11.png?raw=true "Import JSON")

## Configure and Connect Lab PC to EAP SSID

Unlike our iPSK SSID - which the end hosts essentially just see as a regular PSK-protected WPA2 SSID; and, as such, require no additionally configuration aside from entering their key -- 802.1x-based SSIDs (ie: the CAMPUS-EAP-POD# SSID) will require some additional configuration on the Client PC side.

1. On your Client Lab PC, open:

    1. ***Control Panel***, then

    2. ***Network and Internet***

    3. ***Network and Sharing Center***

    4. Choose ***Setup a new connection or network***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-12.png?raw=true "Import JSON")

2. Choose ***Manually connect to a wireless network*** and click Next

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-13.png?raw=true "Import JSON")

3. On the next screen:

    1. Enter the EAP SSID assocated to your POD (Ex: CAMPUS-EAP-POD#)

    2. Select ***WPA2 Enterprise***

    3. Uncheck "Start this connection automatically"

    4. Click ***Next***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-14.png?raw=true "Import JSON")

4. On the Success Screen, choose ***Change Connection Settings***
    
    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-15.png?raw=true "Import JSON")

5. On the next screen:

    1. Select the ***Security*** tab, then

    2. Change the dropdown to ***Microsoft: Smart Card or other certificate***

    3. Click ***Advanced Settings***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-16.png?raw=true "Import JSON")

6. In the 802.1x settings tab:

    1. Check the box for "Specify authentication mode":

    2. Use the dropdown to select ***Computer authentication***

    3. Click ***OK*** to return to the previous screen

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-17.png?raw=true "Import JSON")

7. Back at the Wireless Network Properties Screen, click ***Settings***

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-18.png?raw=true "Import JSON")

8. For the next screen:

    1. Check the box next to "Connect to these servers" and enter `ise.dcloud.cisco.com`

    2. Select the ***CA*** box

    3. Click ***Advanced***

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-19.png?raw=true "Import JSON")

9. On the Configure Certificate Selection screen:

    1. Check the box next to "Certificate Issuer"

    2. Check the box next to ***CA***

    3. Click ***OK***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-21.png?raw=true "Import JSON")

10. Back on the "Smart Card or other Certificate Properties" screen, select ***OK***

11. Back at the CAMPUS-EAP-POD1 Wireless Network Properties Screen, click ***OK***

12. Back at the "Successfully added CAMPUS-EAP-POD#" screen, click ***Close***

13. Now back on the Desktop:

    1. Click the Network tray icon

    2. Select the "CAMPUS-EAP-POD#" SSID associated with your POD #

    3. Click ***Connect***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-20.png?raw=true "Import JSON")


## Validate ISE Radius Live Logs

1. From the Windows Jump Host, open a web browser and navigate to ISE via https://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From the hamburger menu in the top left:

    1. Select ***Operations*** then

    2. Under "RADIUS" Select ***Live Logs***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-07.png?raw=true "Import JSON")

3. From this point, we should see a successful client policy pass for the Windows client, this time the Identity field should be the Subject Common Name (CN) presented by the end host's domain certificate.  As before, feel free to click on the Details icon next to the Green checkbox to see more!

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-22.png?raw=true "Import JSON")

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
> It is advised that you go back into the DCLOUD-LAB-POLICY and "Disable" both the Authentication and Authorization policies that you enabled before, prior to testing the next mechanism.  Please reference the screenshots from the "Enable" section above if you need a reminder of where those are at!  Additionally, it is recommended that you "Forget" the Wireless Network configuration from the Client Lab PC before proceeding to the next module.

:mega::mega::mega:


>[!IMPORTANT]
>**Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into.

[**Next Section**](../ise-automation-4-testing/03-EAP-Credentials-Based-Testing.md)

[**Return to ISE Automation Lab Overview**](../README.md)