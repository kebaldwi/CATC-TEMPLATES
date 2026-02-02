# Template Deployment

We will now `deploy` a template within a Project with your Area Name within Catalyst Centers template editor.

Follow these steps:

## Open the Collection Runner

Navigate and open the desired collection runner:

   1. Within Postman, click on the collection shortcut in the sidebar
   2. Hover over the collection `Catalyst Center API LAB 302 - Template Deployment`
   3. Click the `Run Collection` submenu option

      ![Open Collection Runner](./assets/Postman-Collection-DeployTemplate.png?raw=true)

## Run the Collection

To run the collection, follow these steps:

   1. Locate the sub-components of the `Runner`
   2. On the right under data, click *select* 
   3. Browse and select the CSV using explorer
   4. Click Open to select the file to be used
   5. Optionally select the `Save Responses` option

      ![Select File](./assets/Postman-Collection-DeployTemplate-Run-CSV.png?raw=true)

   6. Click  the `Run Catalyst Center API LAB 302 - Template Deployment` button

      ![Run Collection](./assets/Postman-Collection-DeployTemplate-Runner.png?raw=true)

3. The following summary will slowly appear as the collection is processed
   ![Results](./assets/Postman-Collection-DeployTemplate-Summary.png?raw=true)

## Verifying Template Deployment

To verify that the template was deployed successfully, we will inspect the template editor within Catalyst Center.

Follow these steps:

1. Open a browser and navigate to [**Catalyst Center**](https://198.18.129.100), where an SSL Error is displayed as depicted. Click the **Proceed to `https://192.18.129.100` (unsafe)** link to continue

   ![SSL Error](./assets/catc-SSLERROR.png?raw=true)

2. Log into Catalyst Center using 

   * username: `admin`
   * password: `C1sco12345`

   ![Login](./assets/catc-Login.png?raw=true)

3. When the Catalyst Center Dashboard is displayed, Click the **&#8801;** icon to display the menu'

   ![Hamburger](./assets/catc-Menu.png?raw=true)

4. Select `Tools>Template Editor` from the menu to continue.

   ![Template Editor](./assets/catc-Menu-TemplateEditor.png?raw=true)

5. Expand the Project with your Area Name on the left to show your specific Project with the template, then select it and view it on the right.

   ![Template](./assets/catc-TemplateEditor-DeployTemplate-Verify.gif?raw=true)

## Summary

We have been able to deploy a template within a project inside Catalyst Centers template editor. 

This scenario may be augmented and modified to use imported files within Postman to allow for a more dynamic approach. The flow allows us to rapidly stage Projects and Templates, perhaps importing them from GitHub in the CICD pipeline. 

> **Note**: If there is time, look at the pre and post-scripts within Postman and look at the additionally included Deploy Template API and perhaps run it.

> [**Next Module**](../catc-catcenter-5-archive/01-intro.md)

> [**Return to LAB Menu**](../README.md)