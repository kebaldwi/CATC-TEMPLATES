# Assigning Settings and Credentials

In this module, we will use *Postman* to **deploy** `settings` and `credentials` to a hierarchy within Catalyst Center. 

Catalyst Center uses hierarchy to logically align intent (code and configuration) against infrastructure. This feature enables the network administrator to align change requests and outage windows to allow for changes and modifications to the network.

## Settings and Credentials Background

The Design area is where you create the structure and framework of your network, including the logical topology, network settings, and device type profiles that you can apply to devices throughout your network.

The settings and credentials which we assign to the hierarchy allow us to be deterministic in where we inherit settings from parent objects and where we override settings in the child objects.

This allows us to deploy changes to the network with localized maintenance windows and or slowly roll out changes through multiple sites without impacting the entire network. 

As with all the Design, Policy & Provisioning elements, they are all tied to the hierarchical nature of Catalyst Center. 

> **Prerequisites**: **Completed** the previous section **Build Hierarchy**

## Postman and External Data Sources

Within Postman, we will utilize the collection `Assign Settings Creds` to assign settings and credentials to the Hierarchy of Catalyst Center in order to associate `settings` and `credentials` to devices. 

This Collection may be run whenever you wish to assign or modify the `settings` and `credentials` of the Hierarchy to either **add** or **modify** settings and or credentials. 

Accompanying the Collection is a **required** Comma Separated Value (CSV) file, which is essentially an `answer file` for the values used to build the design which we have previously edited. 

You will have already modified the 3rd line of the **CSV** with the correct POD information with the following: 

So it looks like this but for your **POD** specific information.

![VS Code CSV edits for Hierarchy](./assets/csv-edit-hierarchy.png)

![VS Code CSV edits for Devices](./assets/csv-edit-devices.png)

> [**RETURN**](../catc-catcenter-0-orientation/04-externaldata.md)**:** If you have not done so please refer back to the previous section to edit the **CSV** accordingly [**link**](../catc-catcenter-0-orientation/04-externaldata.md)

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)