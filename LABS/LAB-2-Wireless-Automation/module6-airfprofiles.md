# Creating a Wireless AI Radio Frequency (RF) Profile

In this subsection we will build a Wireless AI Radio Frequency (RF) Profile. This helpful tool, allows the administrator to tune the RF spectrum for the type of environment, and channels which are needed to support clients within their carpeted and non carpeted spaces. 

There are two types of RF Proile which can be created in **Catalyst Center**. As of **2.3.5.6** AI RF Profiling was introduced to help customers to better tune their wireless environments making use of suggestions made by **Catalyst Center** through interations with the Cisco Cloud infrastructure. 

**AI RF Profiles** can be built at the building level today, and allow for a building of one or more Catalyst 9800 Wireless Controllers to work across multiple floors to synchronize the wireless RF, as we did with Mobility Groups over the years. **AI RF Profiles** may be built through a conversion of an existing **Basic RF Profile**, or from scratch. They are assigned to controllers in the AI RF Profile settings page.

**Basic RF Profiles** as they are now called are the existing set of capabilities that can be used to tune the RF for a specific floor. Much like **AI RF Profiles** though these cannot be used in conjunction with the cloud and do not offer AI suggestions. There are many things that can be accomplished from an RF Profile, to tweek the environment, from channels used, to data rates, to power settings deployed. Access points when deployed will utilize these RF Profiles to deploy the SSID's and the intention is to have the best wireless experience for the clients served in a specific area.

## Create AI RF Profile

During the next few steps we will create an **AI RF Profile** by cloning a **Basic RF Profile**. The purpose of which is to facilitate the easy duplication of settings and enable the AI RRM capabilities for **Catalyst Center** to make suggestions about **optimizing** wireless settings. 

<details open>
<summary> Click the arrow for details</summary>

### Step 1 - ***Create AI RF Profile***

During this section we will duplicate the previously created **Basic RF Profile**. If you have not done so please complete the previous section.

1. To create our **AI RF Profile**, first open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select **`Design > Network Settings`**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the **`Wireless`** tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page select the **checkbox**  beside the **Basic RF Profile** named **BASIC-RF**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-rfprofile-results.png?raw=true "Import JSON")

4. To Create **AI RF Profile** from the Actions menu select **Upgrade to AI**. This will **duplicate** the wireless settings and open up an **AI profile** to be edited.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile.png?raw=true "Import JSON")

5. Select **Yes** to the **Upgrade to AI** popup

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-1.png?raw=true "Import JSON")

6. An editable version of the new **AI RF Profile** will appear. Complete the following steps: 

   1. Rename the profile to **`AI-RFP`**
   2. Set the **Busy Hours** to **low** as shown
   3. Click **Save** continue

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-2.png?raw=true "Import JSON")

</details>

## Assign the AI RF Profile

To assign the **AI Profile** to the **Building**. **AI Profiles** if you remember are to be **assigned** at the **Building level**, and cannot be assigned at a floor level. This is because they are defined to allow **Catalyst Center** to **coordinate** the **wireless settings** for an entire building of which **multiple controllers** may be used on differing floors. 

> [!NOTE]
> This section will need to be completed **after** the initial provisioning of the **Wireless LAN Controller**.

<details open>
<summary> Click the arrow for details</summary>

### Step 1 - ***AI Analytics***

1. To assign **AI RF Profile** we need to first enable the **AI Analytics** within the **Catalyst Center** system settings. Navigate to **`System > Settings`**. 

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigate-system.png?raw=true "Import JSON")

2. Select **Cisco AI Analytics** to enable the capability.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigate-system-ai.png?raw=true "Import JSON")

3. The **Cisco AI Analytics** page displays. Enable the following:

   1. Enable AI Network Analytics
   2. AI-Enhanced RRM
   3. Enable Endpoint Smart Grouping
   4. Enable AI Spoofing Detection
   
      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-system-ai-analytics-1.png?raw=true "Import JSON")

   5. Enable log export
   6. On the dropdown provided choose **US East (N. Virginia)** for the storage of data.

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-system-ai-analytics-2.png?raw=true "Import JSON")

   7. Click the **Enable** button to continue.

      ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-system-ai-analytics-3.png?raw=true "Import JSON")  

4. Click the **checkbox** to accept the **EULA** and then click **Submit**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-system-ai-analytics-4.png?raw=true "Import JSON")  

5. Click **OK** on the Success Popup displayed.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-system-ai-analytics-5.png?raw=true "Import JSON")  

### Step 2 - ***Assign AI RF Profile***

During this section we will assign the previously created **AI RF Profile**. If you have not done so please complete the previous sections.

1. To assign our **AI RF Profile**, first open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select **`Design > Network Settings`**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-network-settings.png?raw=true "Import JSON")

2. On the Network page click the **`Wireless`** tab to navigate to the wireless page.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-wireless-settings.png?raw=true "Import JSON")

3. On the **Wireless** page select the **AI RF Profile**  beside the **Basic RF Profile** 

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-1.png?raw=true "Import JSON")

4. In the **AI RF Profile** section locate the profile **AI-RFP** and on the right click the **`...`** symbol and then from the menu **Assign Locations** 

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-2.png?raw=true "Import JSON")

5. On the **Assign Locations to AI RF-Profile** popout page use the hierarchy to navigate and select the **Building** as shown. Then click **Assign**

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-3.png?raw=true "Import JSON")

6. Click **Confirm** to continue  

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-4.png?raw=true "Import JSON")

7. Click **Continue** to continue 

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-5.png?raw=true "Import JSON")

8. On the **AI RF Profile** section click the **1**  beside the **AI-RFP Profile** to see where its assigned.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-wireless-airfprofile-assign-6.png?raw=true "Import JSON")

</details>

## Summary

At this point you will have successfully configured **AI RF Profiles** on the **Wireless Controller** from **Catalyst Center**. During this lab we configured have configured SSID's, Wireless Network Profiles, RF Profiles, FlexConnect VLANs. The next step is applying **QoS**.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Application QoS Module**](../LAB-2-Wireless-Automation/module7-applicationqos.md)

> [**Return to Lab Menu**](./README.md)