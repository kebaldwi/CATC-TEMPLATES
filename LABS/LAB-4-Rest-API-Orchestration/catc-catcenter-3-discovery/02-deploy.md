# Device Discovery Deployment

We will now `discover` multiple devices listed within the CSV and assign them to the sites as per the hierarchy within the CSV.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 201 - Device Discovery`
   3. Click the `Run Collection` submenu option

      ![Open Collection Runner](./assets/Postman-Collection-Discovery.png?raw=true)

## Run the Collection

To run the collection, do the following:

   1. Locate the sub components of the `Runner`
   2. On the right under data, click *select* 
   3. Browse and select the CSV using explorer
   4. Click Open to select the file to be used
   5. Optionally select the `Save Responses` option

      ![Select File](./assets/Postman-Collection-Discovery-Run-CSV.png?raw=true)

   6. Click  the `Run Catalyst Center API LAB 201 - Device Discovery` button

      ![Run Collection](./assets/Postman-Collection-Discovery-Runner.png?raw=true)

3. The following summary will slowly appear as the collection is processed

   ![Results](./assets/Postman-Collection-Discovery-Summary.png?raw=true)

## Verifying Device Discovery

We will inspect the Discovery Tool within Catalyst Center and the inventory to verify that the devices were discovered successfully.

Follow these steps:

1. Open a browser and navigate to [**Catalyst Center**](https://198.18.129.100), where an SSL Error is displayed as depicted. Click the **Proceed to `https://192.18.129.100` (unsafe)** link to continue

   ![SSL Error](./assets/catc-SSLERROR.png?raw=true)

2. Log into Catalyst Center using 

   * username: `admin`
   * password: `C1sco12345`

   ![Login](./assets/catc-Login.png?raw=true)

3. When the Catalyst Center Dashboard is displayed, Click the **&#8801;** icon to display the menu'

   ![Hamburger](./assets/catc-Menu.png?raw=true)

4. Select `Tools>Discovery` from the menu to continue.

   ![Discovery Menu](./assets/catc-Menu-Discovery.png?raw=true)

5. On the left, you can click on the view all discoveries, then select it and view it on the right. 

   ![Discovery Dashboard](./assets/catc-Discovery-Dashboard.png?raw=true)

6. Within that screen, you can select the various discoveries and look at their details.

   ![Discovery Job](./assets/catc-Discovery-Job.png?raw=true)

7. Alternatively, you can go `Provision > Network Devices > Inventory` and view the devices in the Global Level.

   ![Inventory](./assets/catc-Inventory.png?raw=true)

You will notice the devices have been discovered and assigned to the appropriate level of the Hierarchy as per the CSV.

## Summary

We have discovered devices within the network and imported them into Catalyst Center. This scenario may be augmented and modified to create a brownfield learn, which would allow the provisioning of a template to nullify AAA settings and then assign the device to a site for provisioning.

This may assist in brownfield learning so as to ensure the device may be properly provisioned with the UI based settings for intent.

> **Note**: If there is time, look at the results of the Discovery and Inventory within Catalyst Center and the various pre and post-scripts within Postman.

> [**Next Module**](../catc-catcenter-4-templates/01-intro.md)

> [**Return to LAB Menu**](../README.md)