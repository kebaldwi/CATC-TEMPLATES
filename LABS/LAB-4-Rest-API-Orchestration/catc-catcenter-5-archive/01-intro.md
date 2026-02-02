# Archiving Configurations

In this module, we will use *Postman* to download an archive of the running and startup configurations of a device in the hierarchy within Catalyst Center. 

Catalyst Center uses hierarchy to logically align intent (code and configuration) against infrastructure. This allows the network administrator to align changes and modifications to the network within maintenance windows.

## Configuration Archive Background

Catalyst Center allows for the Archiving of both the `Running` and `Startup` Configurations for devices within the `inventory` of Catalyst Center. In the earlier Catalyst Center GUI's, there was no capability to export or archive the configurations apart from this REST-API-based approach. Additional capabilities have been added to the most recent version of Catalyst Center, but there remain good use cases for this capability.

One such use case is configuration `compliance`. Suppose we wanted to create a python-based `compliance` tool that utilized the Device Inventory and the configuration files. In that case, we could keep track of devices' **code** and **configurations** to ensure that the code was of a specific version and perhaps certain lines of code were included in the configuration. 

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