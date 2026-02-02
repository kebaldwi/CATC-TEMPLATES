# Retrieve Device Inventory

In this module, we will use *Postman* to retrieve the device inventory of the hierarchy within Catalyst Center. 

Catalyst Center uses hierarchy to align infrastructure needs logically against intent. This allows the network administrator to align change requests and outage windows to allow for changes and modifications to the network.

##  Catalyst Center Inventory Background

Catalyst Center keeps a detailed inventory of the devices discovered or onboarded from the network. The inventory is used to reference devices in the Catalyst Center UI but also offers a place to see detailed information about the Product ID, Hostname, Software Image, and much more.

The inventory could be used in reports to determine compliance or to reference the devices within the system for either deploying templates or issuing show commands with the command runner used earlier.

For example we may pull the device inventory to determine what we may need to upgrade for code, or to pull the Unique Identifier for a device that we may want to push a specific configuration to via template. There are many needs for this type of request.

> **Prerequisites**: **Completed** the previous section **Device Discovery**

## Postman and External Data Sources

Within Postman, we will utilize the collection `Template Deployment` to build projects within the `Template Editor` and add `Regular Templates` to them in order to `configure` devices. 

This Collection may be run whenever you wish to `configure` or `modify` the **configuration** of a `device` within Catalyst Center. 

Accompanying the Collection is a **required** Comma Separated Value (CSV) file, which is essentially an `answer file` for the values used to build the design which we have previously edited. 

You will have already modified the 3rd line of the **CSV** with the correct POD information with the following: 

So it looks like this but for your **POD** specific information.

![VS Code CSV edits for Hierarchy](./assets/csv-edit-hierarchy.png)

![VS Code CSV edits for Devices](./assets/csv-edit-devices.png)

> [**RETURN**](../catc-catcenter-0-orientation/04-externaldata.md)**:** If you have not done so please refer back to the previous section to edit the **CSV** accordingly [**link**](../catc-catcenter-0-orientation/04-externaldata.md)

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)