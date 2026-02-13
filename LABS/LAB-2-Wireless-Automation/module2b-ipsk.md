# Building a Identity PreShared Key (iPSK) Wireless LAN

## Lab Section 1 - Building a Identity PreShared Key (iPSK) Wireless LAN

In this subsection we will build a Wireless LAN for Identity iPSK authentication. This lab does have a requirement for ISE configuration. For information on how to prepare ISE for use with this lab please click [ISE Configuration](./iseconfiguration.md).

For our lab scenario we will assume this is to be used for IOT devices.

Click on the arrow below to expand and follow to complete the tasks.

<details open>
<summary> Building a WLAN with a Identity Pre-Shared Key (iPSK)</summary>

#### Step 1 - ***Create SSID***

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Design>Network Settings`.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the `Wireless` tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page click `Add` above the *SSID* section to create a new Wireless LAN

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-begin.png?raw=true "Import JSON")

4. A Wireless SSID workflow will begin with *BASIC Settings* which will guide you through the build process of the WLAN. Complete the following steps:
   1. Enter the **Wireless Network Name (SSID)** as `CAMPUS-iPSK-<POD#>`
   2. **Dual Band Operation (2.4 Ghz and 5 Ghz)** *enables the SSID for dual band operation*
   3. **Voice and Data** *configuring best practices for Both Voice and Data*
   4. **Admin Status** *enables the SSID*
   5. **Broadcast SSID** *enables the SSID to be broadcast allowing clients to see it*
   6. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-basic.png?raw=true "Import JSON")

5. The Wireless SSID workflow will continue with *Security Settings*. Complete the following steps:
   1. In the *Level of Security* section select **Personal**
   2. Additionally in the *Level of Security* section select **WPA2**
   3. Under *Passphrase Type*
      1. select **ASCII**
      2. Enter `C1sco12345C1sco12345` for the *Passphrase*
   4. Under the *AAA Configuration section* select **Fast Lane**
   5. Under the *AAA Configuration section* select **Identity PSK**
   6. Under the *AAA Configuration section* click **Configure AAA**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-security.png?raw=true "Import JSON")
   
   7. Click the dropdown arrow on the left to select a value and then select the VIP `198.18.133.27` of the **ISE Cluster**. Click **Configure** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-aaa-config.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-aaa-configured.png?raw=true "Import JSON")

   5. In the *AAA Configuration section* select **Mac Filtering** and **Fast Lane**
   6. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-security-complete.png?raw=true "Import JSON")

6. The Wireless SSID workflow continues with *Advance Settings*. Complete the following steps:
   1. Select **Radius Client Profiling** and Leave all other sections here as default 
   2. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-advance.png?raw=true "Import JSON")

#### Step 2 - ***Associate SSID to Profile***

1. The Wireless SSID workflow continues with *Associate SSID to Profile*. Select the Wireless Profile on the left as shown `DNAC-WIRELESS`

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-profile-begin.png?raw=true "Import JSON")

   > [!NOTE] 
   > If no *Wireless Profile* exists, we must click **Add Profile** to add one to Catalyst Center.

2. The Wireless SSID workflow continues with *Associate SSID to Profile*. Complete the following steps:
   1. Enter the **Profile Name** as `DNAC-WIRELESS` if blank
   2. Select **No** *under Fabric*
   3. Select **Interface** and **management** for the *Interface Name*
   4. Select **No** for *do you need Anchor for the SSID*
   5. Select **FlexConnect Local Switching** and enter **20** for *Local to VLAN* setting
   6. Click **Associate Profile**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-profile-campus-ipsk-1.png?raw=true "Import JSON")

3. The Wireless SSID workflow continues with *Associate SSID to Profile*. On the left the Profile **DNAC-WIRELESS** will be displayed with a green checkmark. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-profile-campus-ipsk-2.png?raw=true "Import JSON")

4. The Wireless SSID workflow continues with a *Summary* page. On the left the a summary of all the changes will be displayed. Click **Save** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-profile-campus-ipsk-summary.png?raw=true "Import JSON")

5. The Wireless SSID workflow completes with a *Results* page displaying that both the SSID and the Profiles were successfully saved and updated. Click **Wireless Home** to finish the process.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-profile-campus-ipsk-results.png?raw=true "Import JSON")

   > [!NOTE] 
   > If this is a new **Wireless Profile** then select **Configure Network Profile** and complete the optional steps for assigning sites as detailed in Step 3 of creating a PSK WLAN above.

6. Return to the **Wireless Settings** page and you should see now our new *SSID* **CAMPUS-iPSK-<POD#>**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-ipsk-results.png?raw=true "Import JSON")

</details>

## Lab Section 2 - Creating a FlexConnect Local Vlans

In this subsection we will add additional vlans for local switching for our FlexConnect deployment. *Note: If we were utilizing* ***Local Mode*** *for the Access Points we would add additional Wireless Interfaces or vlan groups respectively to the Controller.* 

In this lab, we need to utilize FlexConnect, and so to allow for CoA of clients to other Vlans we need to add those to the configuration of our Access Points. 

<details open>
<summary> Click the arrow for details</summary>

### Step 1 - ***Add FlexConnect VLANs***

1. To create an RF Profile, first open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Design>Network Settings`.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the `Wireless` tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page scroll down to the *FlexConnect VLAN* section and enter the following:
   1. Enter *Native VLAN ID* as `10`
   2. Under *AAA Override VLAN* Section click the **⨁**
   3. In the first *AAA Overide VLAN* set the *VLAN ID* to start at **30**
   4. Set the *VLAN Name* to **voicevlan** as shown
   5. In the second *AAA Overide VLAN* set the *VLAN ID* to start at **40**
   6. Set the *VLAN Name* to **guestvlan** as shown
   7. Click **Save** continue

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-flexconnect-vlan.png?raw=true "Import JSON")

</details>

## Summary

At this point you will have successfully configured the **iPSK SSID** on the **Wireless Controller** from **Catalyst Center**. During this lab we will configure additional SSID's, Wireless Network Profiles, RF Profiles, FlexConnect VLANs and deployed the configuration. The next step is configuring additional **SSID**.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Proceed to EAP SSID Sub Module**](./module2c-eap.md)

> [**Return to Module 2**](./module2-wlans.md)

> [**Return to PSK SSID Sub Module 2**](./module2a-psk.md)

> [**Proceed to EAP SSID Sub Module 2**](./module2c-eap.md)

> [**Proceed to OPEN SSID Sub Module 2**](./module2d-open.md)

> [**Return to Lab Menu**](./README.md)