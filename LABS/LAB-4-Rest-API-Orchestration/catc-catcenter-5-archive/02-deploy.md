# Archiving Device Configurations

We will now use the REST-API's within the collection `Configuration Archive` to pull the configuration archives for all devices within the inventory. 

This collection will first get a list of devices, then download the configuration archive for each one. You will need to save the responses to download them.

There is a difference in the way we will approach this use case because of the way the API was written. The API was developed to download or archive a specific configuration. To Archive multiple configurations you would create a loop. As Postman has nowhere to send the data as a zip file we will do only one of these. Normally you would loop through and archive them into a file store.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner through the following:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 304 - Configuration Archive`
   3. Click the `Run Collection` submenu option

      ![Open Collection Runner](./assets/Postman-Collection-ConfigArchive.png?raw=true)

## Run the Collection

To run the collection, do the following:

To run the collection, do the following:

   1. Locate the sub components of the `Runner`
   2. On the right under data, click *select* 
   3. Browse and select the CSV using explorer
   4. Click Open to select the file to be used
   5. Optionally select the `Save Responses` option

      ![Select File](./assets/Postman-Collection-ConfigArchive-Run-CSV.png?raw=true)

   6. Click  the `Run Catalyst Center API LAB 201 - Device Discovery` button

      ![Run Collection](./assets/Postman-Collection-ConfigArchive-Runner.png?raw=true)


## Retrieve the Archive

1. The following summary will slowly appear as the collection is processed

   1. Copy the Password `TestT3$t` to open the zip file later.
 
      ![Results](./assets/Postman-Collection-ConfigArchive-Summary.png?raw=true)
 
   2. Click the console at the bottom of Postman and search for the last API call made.

      ![View Console](./assets/Postman-Collection-ConfigArchive-Console.png?raw=true)

   3. Expand the results of the API call and open the `Response Body`
   4. Notice the file response does have the Configurations in it. This API Collection collected all of them and, if exported to a Python system, could save them to a local file folder.

      ![Raw Data](./assets/Postman-Collection-ConfigArchive-Console-Results.png?raw=true)

2. Click on the collection `Catalyst Center API LAB 304 - Configuration Archive` to expand it in the left pane, then do the following:

   1. Click on the Rest-API `Get Results` sub-component to open it on the right
   2. Click on the little arrow on the right of `Send` to expose a submenu
   3. Click `Send and Download` to send this Rest-API and automatically download what is retrieved

      ![Get Request](./assets/Postman-Collection-ConfigArchive-ResultsAPI.png?raw=true)

3. As the Rest-API `Get Results`completes an explorer window will prompt to save the results to the desktop click ok to save the file

   ![Download](./assets/Postman-Collection-ConfigArchive-ResultsAPI-Send.png?raw=true)

4. Locate the zip file on the desktop, and extract it using whatever extraction tool is available to your system. WinRar is what can be used and is displayed here.

   ![Extract](./assets/Postman-Collection-ConfigArchive-Extract.png?raw=true)

5. During Extraction, you will be prompted for the password we stored from step 6, but again it is `TestT3$t` in the event you can't locate it. Enter the password as prompted and complete the extraction.

   ![Opening](./assets/Postman-Collection-ConfigArchive-Pwd.png?raw=true)

6. Locate the Extracted folder and open one of the text-based files within to reveal the configuration selected.

   ![Files](./assets/Postman-Collection-ConfigArchive-Verify.png?raw=true)

## Summary

Congratulations, in this lablet, we used *Postman* to download an archive of the `running` and `startup` configurations of devices from Catalyst Center. 

Catalyst Center allows for the `archiving` of both the `running` and `startup` Configurations for devices within the inventory of Catalyst Center. 

In the earlier Catalyst Center GUI's, there was no capability to archive the configurations apart from this REST-API-based approach. Additional capabilities have been added to the most recent version of Catalyst Center, but there remain good use cases for this capability.

> **Note**: Additionally, if there is time, look at the pre and post-scripts within Postman.

> [**Next Module**](../catc-catcenter-6-inventory/01-intro.md)

> [**Return to LAB Menu**](../README.md)