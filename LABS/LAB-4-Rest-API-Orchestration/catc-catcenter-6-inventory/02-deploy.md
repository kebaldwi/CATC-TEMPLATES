# Retrieving the Device Inventory

We will now retrieve the entire device inventory from  Catalyst Center.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 401 - Device Inventory`
   3. Click the `Run Collection` submenu option

      ![Open Collection Runner](./assets/Postman-Collection-DeviceInventory.png?raw=true)

## Run the Collection

To run the collection, do the following:

   1. Locate the sub components of the `Runner`
   2. Select the `Save Responses` option as we will need the output
   3. Click  the `Catalyst Center API LAB 401 - Device Inventory` button

      ![Run Collection](./assets/Postman-Collection-DeviceInventory-Runner.png?raw=true)

## View the Results

The following results will slowly appear as the collection is processed.

   1. Click `View Results` on the Left
   2. Watch the Results slowly appear. The API has been set up to give device info in the test area.

      ![Results](./assets/Postman-Collection-DeviceInventory-Summary.png?raw=true)

5. To view the results, do the following:

   1. Click the `Console` option at the bottom of postman
   2. Expand the Get request that begins `GET https://198.18.129.100/api/v1/network-device` 
   3. Within the `Response Body` click the `Drop Down` arrow and view the Response

      ![View Response](./assets/Postman-Collection-DeviceInventory-Console.png?raw=true)

While this displayed all the devices in lab, let's try this one again, and and select the **CSV**.

## Open the Collection Runner and use the CSV for the Pod

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 401 - Device Inventory`
   3. Click the `Run Collection` submenu option

      ![Open Collection Runner](./assets/Postman-Collection-DeviceInventory.png?raw=true)

## Run the Collection

To run the collection, do the following:

   1. Locate the sub-components of the `Runner`
   2. Select the `Save Responses` option as we will need the output
   3. Click  the `Catalyst Center API LAB 401 - Device Inventory` button

      ![Run Collection](./assets/Postman-Collection-DeviceInventory-Pod-Runner-Select.png?raw=true)

      ![Run Collection](./assets/Postman-Collection-DeviceInventory-Pod-Runner.png?raw=true)

## View the Results

The following results will slowly appear as the collection is processed.

   1. Click `View Results` on the Left
   2. Watch the Results slowly appear. The API has been set up to give device info in the test area.

      ![Results](./assets/Postman-Collection-DeviceInventory-Pod-Summary.png?raw=true)

## Summary

We have run a collection against Catalyst Center to retrieve the device inventory and can export that to a file within our host. In this section we prove you can create code to do the same process but display different results based on data given. Think how this might be driven from an AI perspective. Now you could ask for a Device List based on part of your hierarchy, and not just the entire list.

This information might be used for many uses, including making decisions on template deployment, SWIM upgrades, etc. The limits of what can be done from here on are only those of your imagination.

> **Note**: Additionally, if there is time, look at the pre and post-scripts within Postman.

> [**Next Module**](../catc-catcenter-7-cmd-run/01-intro.md)

> [**Return to LAB Menu**](../README.md)