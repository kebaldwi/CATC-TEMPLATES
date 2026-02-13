# Building a PreShared Key (PSK) Wireless LAN 

## Lab Section 1 - Building a PreShared Key (PSK) Wireless LAN 

In this subsection we will build a Wireless LAN for PSK authentication. Click on the arrow below to expand and follow to complete the tasks.

For our lab scenario we will assume this is to be used for Cisco 8821 IP Phones.

<details open>
<summary> Building a WLAN with a Pre-Shared Key (PSK) </summary>

#### Step 1 - ***Create SSID***

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Design>Network Settings`.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the `Wireless` tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page click `Add` above the *SSID* section to create a new Wireless LAN

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-begin.png?raw=true "Import JSON")

4. A Wireless SSID workflow will begin with *BASIC Settings* which will guide you through the build process of the WLAN. Complete the following steps:
   1. Enter the **Wireless Network Name (SSID)** as `CAMPUS-PSK-<POD#>`
   2. **Dual Band Operation (2.4 Ghz and 5 Ghz)** *enables the SSID for dual band operation*
   3. **Voice and Data** *configuring best practices for Both Voice and Data*
   4. **Admin Status** *enables the SSID*
   5. **Broadcast SSID** *enables the SSID to be broadcast allowing clients to see it*
   6. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-basic.png?raw=true "Import JSON")

5. The Wireless SSID workflow will continue with *Security Settings*. Complete the following steps:
   1. In the *Level of Security* section select **Personal**
   2. Additionally in the *Level of Security* section select **WPA2**
   3. For *Passphrase Type* select **ASCII**
   4. Enter `C1sco12345C1sco12345` for the *Passphrase*
   5. In the *AAA Configuration section* select **Fast Lane**
   6. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-security.png?raw=true "Import JSON")

6. The Wireless SSID workflow continues with *Advance Settings*. Complete the following steps:
   1. Leave all sections here as default as shown
   2. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-advance.png?raw=true "Import JSON")

#### Step 2 - ***Associate SSID to Profile***

1. The Wireless SSID workflow continues with *Associate SSID to Profile*. As no *Wireless Profile* exists, we must click **Add Profile** to add one to Catalyst Center.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-profile-begin.png?raw=true "Import JSON")

2. The Wireless SSID workflow continues with *Associate SSID to Profile*. Complete the following steps:
   1. Enter the **Profile Name** as `DNAC-WIRELESS`
   2. Select **No** *under Fabric*
   3. Select **Interface**
   4. Select **management** for the *Interface Name*
   5. Select **No** for *do you need Anchor for the SSID*
   6. Select **FlexConnect Local Switching** for the SSID
   7. Enter **20** for *Local to VLAN*
   8. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-profile-campus-psk.png?raw=true "Import JSON")

3. The Wireless SSID workflow continues with *Associate SSID to Profile*. On the left the Profile **DNAC-WIRELESS** will be displayed with a green checkmark. Click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-profile-campus-psk-associated.png?raw=true "Import JSON")

4. The Wireless SSID workflow continues with a *Summary* page. On the left the a summary of all the changes will be displayed. Click **Save** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-profile-campus-psk-summary.png?raw=true "Import JSON")

5. The Wireless SSID workflow completes with a *Results* page displaying that both the SSID and the Profiles were successfully saved and updated. Click **Configure Network Profile** to assign the profile to a site.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-profile-campus-psk-results.png?raw=true "Import JSON")

#### Step 3 - ***Assign Sites to Network Profile***

1. On the *Network Profile* page select **Assign** beside the wireless profile **DNAC-WIRELESS**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-network-profile-assign.png?raw=true "Import JSON")

2. On the *Add Sites to Profile* slide out page select **Floor 1** to assign the site to the wireless network profile. 
3. Click ***Save*** to complete the assignment

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-network-profile-add-sites.png?raw=true "Import JSON")

4. On the *Network Profile* page note **1 Site** appears under *Sites* for the wireless profile **DNAC-WIRELESS**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-network-profile-assigned.png?raw=true "Import JSON")

5. Return to the **Wireless Settings** page and you should see now our new *SSID* **CAMPUS-PSK-<POD#>**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-ssid-psk-results.png?raw=true "Import JSON")

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

At this point you will have successfully configured the **PSK SSID** on the **Wireless Controller** from **Catalyst Center**. During this lab we will configure additional SSID's, Wireless Network Profiles, RF Profiles, FlexConnect VLANs and deployed the configuration. The next step is configuring additional **SSID**.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Proceed to iPSK SSID Sub Module**](./module2b-ipsk.md)

> [**Return to Module 2**](./module2-wlans.md)

> [**Proceed to iPSK SSID Sub Module 2**](./module2b-ipsk.md)

> [**Proceed to EAP SSID Sub Module 2**](./module2c-eap.md)

> [**Proceed to OPEN SSID Sub Module 2**](./module2d-open.md)

> [**Return to Lab Menu**](./README.md)