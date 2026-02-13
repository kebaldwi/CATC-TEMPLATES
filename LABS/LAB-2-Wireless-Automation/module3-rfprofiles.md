# Creating a Wireless Radio Frequency RF Profile

In this subsection we will build a Wireless Radio Frequency (RF) Profile. This helpful tool, allows the administrator to tune the RF spectrum for the type of environment, and channels which are needed to support clients within their carpeted and non carpeted spaces. 

There are two types of RF Proile which can be created in **Catalyst Center**. As of **2.3.5.6** AI RF Profiling was introduced to help customers to better tune their wireless environments making use of suggestions made by **Catalyst Center** through interations with the Cisco Cloud infrastructure. 

**AI RF Profiles** can be built at the building level today, and allow for a building of one or more Catalyst 9800 Wireless Controllers to work across multiple floors to synchronize the wireless RF, as we did with Mobility Groups over the years. **AI RF Profiles** may be built through a conversion of an existing **Basic RF Profile**, or from scratch. They are assigned to controllers in the AI RF Profile settings page.

**Basic RF Profiles** as they are now called are the existing set of capabilities that can be used to tune the RF for a specific floor. Much like **AI RF Profiles** though these cannot be used in conjunction with the cloud and do not offer AI suggestions. There are many things that can be accomplished from an RF Profile, to tweek the environment, from channels used, to data rates, to power settings deployed. Access points when deployed will utilize these RF Profiles to deploy the SSID's and the intention is to have the best wireless experience for the clients served in a specific area.

## Create Basic RF Profile

During the next few steps we will create a **Basic RF Profile**.

<details open>
<summary> Click the arrow for details</summary>

### Step 1 - ***Create Basic RF Profile***

1. To create an Basic RF Profile, first open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select **`Design > Network Settings`**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the **`Wireless`** tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page hover over `Add` beside the **Wireless Radio Frequency Profile** section to create a new Basic RF Profile

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-begin.png?raw=true "Import JSON")

4. The Create RF Profile page displays. Complete the following steps:
   1. Enter the **Profile Name** as `BASIC-RFP` then scroll down to continue
   2. Ensure that **2.4 Ghz** is selected

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-24ghz-1.png?raw=true "Import JSON")

   3. Set the **Supported Data Rates** to start at **`12`** and the **Mandatory Data Rates** to **`18`** and **`36`** as shown
   4. Set the **Data RSSI threshold** to **`72`** and the **Voice RSSI threshold** to **`72`** as shown
   
      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-24ghz-2.png?raw=true "Import JSON")

5. Scroll back to the top and continue creating the Basic RF Profile by completing the following steps:

   1. Select the **5 Ghz** Section.
   2. For **Channel Width** from **Best** by selecting the drop down.
   3. Then select **40 Mhz** from the channel sizes available.

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-5ghz-1.png?raw=true "Import JSON")

   4. Enable **Zero Wait DFS** to ensure the wireless does not impede **RADAR**.
   5. Click the **Select All** for the DCA Channels and then **Deselect** Channels **`169-173`** as they are impeded by **LTE**.

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-5ghz-2.png?raw=true "Import JSON")

   6. Set the **Supported Data Rates** to start at **`12`** and the **Mandatory Data Rates** to **`18`** and **`36`** as shown
   7. Set the **Data RSSI threshold** to **`72`** and the **Voice RSSI threshold** to **`72`** as shown
   8. Click **Save** continue

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-5ghz-3.png?raw=true "Import JSON")

6. The `Wireless` tab will reappear with the new **BASIC RF Profile** as displayed.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-results.png?raw=true "Import JSON")

</details>

## Summary

At this point you will have successfully configured **RF Profiles** on the **Wireless Controller** from **Catalyst Center**. During this lab we configured have configured SSID's, Wireless Network Profiles, RF Profiles, FlexConnect VLANs. The next step is **WLC** provisioning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to WLC Provisioning Module**](../LAB-2-Wireless-Automation/module4-wlcprovisioning.md)

> [**Return to Lab Menu**](./README.md)