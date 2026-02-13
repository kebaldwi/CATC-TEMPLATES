# Wireless Controller Provisioning

In this subsection we will provision the Wireless Controller with the settings for network services, credentials, telemetry and the additional wireless settings of WLAN's, RF Profiles, FlexConnect Vlans. Whenever a new WLAN or a configuration change is made, it will need to be provisioned to the controller using this process.

This can be augmented with Model-Based Configurations as well as Templates which we will discuss in future modules.

<details open>
<summary> Click the arrow for details</summary>

### Step 1 - ***Provisioning Workflow for the Wireless Controller***

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Provision>Network Devices>Inventory`.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory.png?raw=true "Import JSON")

2. On the Inventory page click the `Inventory` tab and complete the following:
   1. Select the *C9800-WLC.dcloud.cisco.com* device as shown
   2. Select from the *Actions* submenu
   3. Select *Provision*
   4. Select *Provision Device*

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-begin.png?raw=true "Import JSON")

3. The **Inventory > Provision Devices** 5 stage workflow will begin. Make no changes on screen 1 and click **Next** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage1.png?raw=true "Import JSON")

4. On screen 2 of the **Inventory > Provision Devices** workflow select *Managing 1 Primary location(s)* which is where we tell **Catalyst Center** where the Access Points will be that this Wireless Controller will manage.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage2.png?raw=true "Import JSON")

5. On the slideout window select **Floor 1** which is where our Access Points will be that this Wireless Controller will manage. Click **Save** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage2-manage.png?raw=true "Import JSON")

6. It is recommended to enable the *AP Reboot Percentage* which aides in upgrades by selecting how many Access Points are upgraded at any one time. For purposes of the lab we will **Enable** this feature and select **25%** from the dropdown menu. Click **Next** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage2-reboot.png?raw=true "Import JSON")

7. On screen 3 of the **Inventory > Provision Devices** workflow we would see the Model-Based Configurations which would be deployed, but none are assigned at this time. This will be covered in later sections. Click **Next** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage3.png?raw=true "Import JSON")

8. On screen 4 of the **Inventory > Provision Devices** workflow we would see the Templates which would be deployed, but none are assigned at this time. This will be covered in later sections. Click **Next** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage4.png?raw=true "Import JSON")

9. On screen 5 of the **Inventory > Provision Devices** workflow we see a *Summary* of what will be configured. Please take time to review this section. Click **Deploy** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage5.png?raw=true "Import JSON")

10. A warning message about **Fastlane Configuration** is displayed to warn about wireless disruptions. Click **OK** to continue.

    ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage5-deploy.png?raw=true "Import JSON")

11. A *Provision Device* Sidemenu appears, giving 3 options abut when to deploy. Choose the **3rd option** allows for you to review the configuration prior to deployment.. Click **Apply** to continue.

    ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-menu-provision-inventory-stage5-generate.png?raw=true "Import JSON")

### Step 2 - ***Deploying the Configuration for the Wireless Controller***

1. From **Catalyst Centers** hamburger menu icon, open the menu and select `Activities`.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-navigation-activities.png?raw=true "Import JSON")

2. On the *Activites* page select the **Work Items** tab. You will notice the work item *Provision Device - Configuration Preview* on the page. It will probably say in progress. Wait for it to say *success* before proceding.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-activities-psk-preview.png?raw=true "Import JSON")

3. When the work item *Provision Device - Configuration Preview* status displays *success* click the link to display the configuration.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-activities-psk-click.png?raw=true "Import JSON")

4. The Wireless Controller configuration will be displayed. Click **Deploy** to continue deploying the configuration.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-activities-psk-display.png?raw=true "Import JSON")

5. To continue to deploy the Wireless Controller configuration select **Now** and then click **Apply**.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-activities-psk-now.png?raw=true "Import JSON")

. A popup to ask if you want to delete the work item will appear, click **No** to keep a record of events.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-activities-psk-nodelete.png?raw=true "Import JSON")

### Step 3 - ***Checking for successful configuration of the Wireless Controller***

1. Navigate back to the *Inventory*, and change the *Inventory Focus* to **Provision** to watch the progress of the provisioning.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-inventory-psk-focus-provision.png?raw=true "Import JSON")

2. When the *Provisioning Status* of the *C9800-WLC* shows as success, click **see details** to look at the logs.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-inventory-psk-seedetails.png?raw=true "Import JSON")

3. Click to display the logs and examine the output as much as possible.

   ![json](../../ASSETS/LABS/WIRELESS/module2-wlans/dnac-inventory-psk-success.png?raw=true "Import JSON")

</details>

## Summary

At this point you will have successfully provisioned the **Wireless Controller** from **Catalyst Center**. During this lab we configured SSID's, Wireless Network Profiles, RF Profiles, FlexConnect VLANs and deployed the configuration. The next step is **Access Point** provisioning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to AP Provisioning Module**](../LAB-2-Wireless-Automation/module5-approvisioning.md)

> [**Return to Lab Menu**](./README.md)