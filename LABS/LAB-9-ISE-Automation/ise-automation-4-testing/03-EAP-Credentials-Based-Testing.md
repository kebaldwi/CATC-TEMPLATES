# EAP Credentials-Based Methods Testing

## Overview

In the last section, we tested EAP-TLS -- which is an EAP method that uses certificates for authenticating and authorizing the Client PCs.  For most production environments this is the recommended mechanism, as it eliminates the security concerns around stolen user passwords.  That said, for environments that may not have a Public Key Infrastructure setup (or for Customers that don't want to manage that complexity), EAP also supports multiple username/password capable mechanisms for authentication/authorization.  Namely, the ones supported on our Windows-based Client Lab PCs are EAP-TTLS and EAP-PEAP (MSCHAPv2).

## General Information

>[!WARNING]
>You must have completed all of [***Lab 2 - Wireless Automation***](../../LAB-2-Wireless-Automation/) and Lab 9 modules 0 through 3 before attempting this lab module.

>[!NOTE]
>If you have just come from the EAP-TLS module and have not yet set the EAP-TLS AuthN/AuthZ rules to "disabled" <b><i><u>AND</u></i></b> "Forgot" the configured EAP wireless profile/rebooted the Client LAB PC, please do so now.

This lab module consists of the following tasks:

1. [***Enable EAP-TTLS/PEAP Rules in ISE***](#enable-eap-ttlspeap-rules-in-ise)
2. [***Configure and Connect Lab PC to EAP SSID***](#configure-and-connect-lab-pc-to-eap-ssid)
3. [***Validate ISE Radius Live Logs***](#validate-ise-radius-live-logs)
4. [***Session Termination***](#session-termination)


## Enable EAP-TTLS/PEAP Rules in ISE

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

5. For the rule named "EAP-TTLS-or-PEAP-AuthN":

    1. Select the gray circle/X icon
    
    2. Choose ***Enabled***
    
    3. Click ***Save*** in the top right hand corner
    
        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-28.png?raw=true "Import JSON") ************************

6. Scroll down and click on ***Authorization Policy*** to expand it

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-02.png?raw=true "Import JSON")

7. For the rule named "EAP-TTLS-PEAP-AuthZ":

    1. Select the gray circle/X icon

    2. Choose ***Enabled***

    3. Click ***Save*** in the bottom right hand corner

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-29.png?raw=true "Import JSON") ***********************

>[!TIP]
>Because our parent policy uses the "Default Network Access" profile -- which has both EAP-TTLS and EAP-PEAP enabled -- we can actually utilize the same AuthN and AuthZ rule to accomodate BOTH mechanisms.  In production, you may see these mechanisms broken out into two separate policies, but for the purposes of this lab we'll keep things simple and leave them as one.  This means that we only need to modify the configuration of the Wireless Profile on the Client Lab PC to test each mechanism.

## Configure and Connect Lab PC to EAP SSID

The configuration of our Windows-based Client Lab PC for either EAP-TTLS or EAP-PEAP (w/ MSCHAPv2) is going to be <u>very similar</u>, so instead of breaking these out into two completely separate modules, we've separated out the "shared" steps (which are 1 thru 4 and then 7 thru 11) and where steps differ (note the two different sections of steps 5 and 6).

>[!IMPORTANT]
>Should you want to test one mechanism and then the other -- for example, you want to test EAP-PEAP first and then EAP-TTLS -- note that you will need to go through the "Forget" network process outlined in [**Lab Client Orientation**](../ise-automation-3-policy/01-Lab-Client-Orientation.md) to forget the wireless profile configured for EAP-PEAP and go through the entirety of the steps below for EAP-TTLS.

### Steps 1 thru 4 (Shared for both EAP-TTLS and EAP-PEAP)

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

### Steps 5 thru 6 (for EAP-PEAP)

5. On the Security Tab of "CAMPUS-EAP-POD# Wireless Network Properties" Screen:

    1. Select ***Microsoft: Protected EAP(PEAP)***, then

    2. Select ***Settings***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-30.png?raw=true "Import JSON")

6. One of the key features of EAP-PEAP is that it *does not* require server validation on the client side.  You <u>can</u> do server validation, of course, but for the purposes of the lab we will disable this:

    1. Uncheck "Verify the server's identity by validating the certificate"

    2. Note that we're using EAP-MSCHAPv2 as our inner authentication method. (by default, this will use the currently logged-on user's credentials, which is fine in our case)

    3. Click ***OK***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-31.png?raw=true "Import JSON")

### Steps 5 thru 6 (for EAP-TTLS)

5. On the Security Tab of "CAMPUS-EAP-POD# Wireless Network Properties" Screen:

    1. Select ***Microsoft: EAP-TTLS***

    2. Select ***Settings***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-35.png?raw=true "Import JSON")

6. From the TTLS Properties Screen:

    1. Uncheck the "Enable identity privacy" box

    2. In the "Connect to these servers" enter `ise.dcloud.cisco.com`

        >[!TIP]
        >Unlike EAP-PEAP, EAP-TTLS does require server validation.  Whether you define the server here (as you would if pushing this out via something like a GPO), or not - the server validation requirement remains.  If its not defined here, Windows will ask you to validate the ISE certificate the first time you connect to this SSID anyway.

    3. Check the box next to our Certificate Authority "CA"

    4. Change the inner EAP method to MS-CHAPv2

    5. Choose ***OK***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-36.png?raw=true "Import JSON")

### Steps 7 thru 11 (Shared again for both EAP-PEAP and EAP-TTLS)

7. Back on the "CAMPUS-EAP-POD# Wireless Network Properties" screen, click ***Advanced Settings***

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-32.png?raw=true "Import JSON")

8. On the Advanced settings screen

    1. Check the box next to "Specify authentication mode:"

    2. From the drop-down, select ***User authentication***

    3. Select ***OK***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-33.png?raw=true "Import JSON")

9. Back at the "CAMPUS-EAP-POD# Wireless Network Properties" window, select ***OK***

10. Back at the "Successfully added CAMPUS-EAP-POD#" window, select ***Close***

11. Now back on the Desktop:

    1. Click the Network tray icon

    2. Select the "CAMPUS-EAP-POD#" SSID associated with your POD #

    3. Click ***Connect***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-20.png?raw=true "Import JSON")

    4. If asked for your user credentials, login with ***username: `admin` and password: `C1sco12345`***




## Validate ISE Radius Live Logs

1. From the Windows Jump Host, open a web browser and navigate to ISE via https://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From the hamburger menu in the top left:

    1. Select ***Operations*** then

    2. Under "RADIUS" Select ***Live Logs***

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-07.png?raw=true "Import JSON")

3. From this point, we should see a successful client policy pass for the Windows client, this time the Identity field should be the user account used to authenticate (in our case, the "admin" account).  As before, feel free to click on the Details icon next to the Green checkbox to see more!

    ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-34.png?raw=true "Import JSON")

## Session Termination

ISE maintains a "session" for any endpoints for a certain amount of time, even if those endpoints drop off the wireless network.  Since we're going to be testing multiple different ISE Policy mechanisms in relatively rapid sequence using <u>the same</u> host/USB Wireless Adapter, we don't want a previously authenticated session to muddle with our attempts at creating a new session using a different policy.  This means we should disconnect from the SSID on the Client LAB PC <b><u>AND</u></b> clear out the session from ISE.  To do so:

1. On the Client Lab PC

    1. Click on the Network tray icon

    2. Select whichever SSID you're currently testing, and choose ***Disconnect***

        >[!NOTE]
        >The image below shows as connected to the "EAP" SSID, but choose whichever is accurate for whatever test you're currently on.

        ![json](../../../ASSETS/LABS/ISE/ISE-TESTING-26.png?raw=true "Import JSON")

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


> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into.


