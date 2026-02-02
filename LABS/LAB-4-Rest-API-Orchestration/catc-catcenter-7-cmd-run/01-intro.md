# Running Show Commands

In this module, we will use *Postman* to run some `show` commands on network devices within the infrastructure that Catalyst Center manages. This allows a method of getting troubleshooting information in the event we need to populate 3rd party management systems. We can use this set of commands to pull parts of the configuration or even make queries via CDP or LLDP to determin neighbor information.

This type of request allows us flexibility in pragmatically determining specific information whcih we may use in programming logic to determine next steps in an automation flow.

## Command Runner Background

The Command Runner tool allows you to run cli commands from the Inventory window on platforms. 

The platform commands that you can run are those such as `ping`, `traceroute`, and `snmpget` to troubleshoot device reachability issues. Additionally, `show` commands may also help or aid in troubleshooting.

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