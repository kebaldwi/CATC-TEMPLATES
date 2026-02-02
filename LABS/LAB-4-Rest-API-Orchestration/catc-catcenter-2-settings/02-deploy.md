# Settings and Credentials Deployment

At this point, we have reviewed the settings within the environment and ensured we will be targeting the correct hierarchy. We are ready to continue pushing the settings and credentials to our newly created hierarchy.

We will now `assign` the settings, credentials, and telemetry settings using the CSV variables provided in the previous step.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 101 - Assign Settings Creds`
   3. Click the `Run Collection` submenu option

      ![Open Run Collection](./assets/Postman-Collection-Settings.png?raw=true)

## Run the Collection

To run the collection, do the following:

   1. Ensure all the sub-components of the `Runner` are selected
   2. On the right under data, click *select* 
   3. Browse and select the CSV using explorer
   4. Click Open to select the file to be used

      ![Select File](./assets/Postman-Collection-Settings-Run-CSV.png?raw=true)

   5. Click  the `Run Catalyst Center API LAB 101 - Assign Settings Creds` button

      ![Run the Collection](./assets/Postman-Collection-Settings-Runner.png?raw=true)

3. The following summary will slowly appear as the collection is processed

   ![Results](./assets/Postman-Collection-Settings-Summary.png?raw=true)

## Verifying Settings and Credentials

To verify that the settings were assigned successfully, we will inspect the site within Catalyst Center.

Follow these steps:

1. Open a browser and navigate to [**Catalyst Center**](https://198.18.129.100), where an SSL Error is displayed as depicted. Click the **Proceed to `https://192.18.129.100` (unsafe)** link to continue

   ![SSL Error](./assets/catc-SSLERROR.png?raw=true)

2. Log into Catalyst Center using 

   * username: `admin`
   * password: `C1sco12345`

   ![Login](./assets/catc-Login.png?raw=true)

3. When the Catalyst Center Dashboard is displayed, Click the **&#8801;** icon to display the menu'

   ![Hamburger](./assets/catc-Menu.png?raw=true)

4. Select `Design>Network Settings` from the menu to continue.
   
   ![Network Settings](./assets/catc-Menu-Settings.png?raw=true)

5. Expand the Hierarchy on the left to show all specific `Area` select it and scroll through the settings.

   ![Verify Settings](./assets/catc-Settings-Verify1.gif?raw=true)

5. Expand the Hierarchy on the left to show all specific `Area` select it and scroll through the credentials.

   ![Verify Credentials](./assets/catc-Settings-Verify2.png?raw=true)

5. Expand the Hierarchy on the left to show all specific `Area` select it and scroll through the telemetry settings.

   ![Verify Telemetry](./assets/catc-Settings-Verify3.gif?raw=true)

## Summary

At this point, we have assigned settings, credentials, and telemetry settings to the Hierarchy utilizing environment variables and REST-API's within the collection runner. 

> **Note**: If there is time, look at the results of the Credentials and Telemetry tabs with Catalyst Center and the various pre and post-scripts within Postman.

> [**Next Module**](../catc-catcenter-3-discovery/01-intro.md)

> [**Return to LAB Menu**](../README.md)