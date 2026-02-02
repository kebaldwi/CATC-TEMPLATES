# Hierarchy Build Deployment

We will now `build` the Hierarchy using the CSV variables previously discussed.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 100 - Build Hierarchy`
   3. Click the `Run Collection` submenu option

      ![Collection Run](./assets/Postman-Collection-Hierarchy.png?raw=true)

## Run the Collection

To run the collection, do the following:

   1. Ensure all the sub-components of the `Runner` are selected
   2. On the right under data, click *select* 
   3. Browse and select the CSV using explorer
   4. Click Open to select the file to be used

      ![Select File](./assets/Postman-Collection-Hierarchy-Run-CSV.png?raw=true)

   5. Click  the `Run Catalyst Center API LAB 100 - Build Hierarchy` button

      ![Collection Runner](./assets/Postman-Collection-Hierarchy-Runner.png?raw=true)

3. Select `View Results` to view the following summary, which will slowly appear as the collection is processed. Notice APIs are only run when they are required. You may view the pre and post-script logic that causes this behavior. Each iteration is a row of the CSV being processed.

   ![Collection Summary](./assets/Postman-Collection-Hierarchy-Summary.png?raw=true)

## Verifying Student Settings Assignment

To verify that the Hierarchy was built successfully, we will inspect the site in Catalyst Center.

Follow these steps:

1. Open a browser and navigate to [**Catalyst Center**](https://198.18.129.100), where an SSL Error is displayed as depicted. Click the **Proceed to `https://192.18.129.100` (unsafe)** link to continue

   ![SSL Error](./assets/catc-SSLERROR.png?raw=true)

2. Log into Catalyst Center using 

   * username: `admin`
   * password: `C1sco12345`

   ![Login](./assets/catc-Login.png?raw=true)

3. When the Catalyst Center Dashboard is displayed, Click the **&#8801;** icon to display the menu'

   ![Hamburger](./assets/catc-Menu.png?raw=true)

4. Select `Design>Network Hierarchy` from the menu to continue.

   ![Menu](./assets/catc-Menu-Hierarchy.png?raw=true)

5. Expand the Hierarchy on the left to show your specific `Area`

   ![Verify](./assets/catc-Hierarchy-Student-Verify.png?raw=true)

## Summary

At this point, we have built the Hierarchy utilizing environment variables and REST-API's within the collection runner. To continue your learning, look at the various REST-API's used to complete this task. Notice that there was a task to create a **{{Token}}** for authentication, which was used and proceeded with the calls to create the Area, Building, and Floor. Each layer of the hierarchy was a singular call. 

> **Note**: Additionally, if there is time, look at the pre and response scripts.

> [**Next Module**](../catc-catcenter-2-settings/01-intro.md)

> [**Return to LAB Menu**](../README.md)