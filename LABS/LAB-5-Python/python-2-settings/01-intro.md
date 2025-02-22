# Building Hierarchy with Settings

In this module, we will use a **CI/CD Pipeline** to build and deploy a hierarchy and settings within Cisco Catalyst Center. 

Cisco Catalyst Center uses hierarchy to logically align intent (code and configuration) against infrastructure. This allows the network administrator to align changes and modifications to the network within maintenance windows.

## Hierarchy Background

The Design area is where you create the structure and framework of your network, including the logical topology, network settings, and device type profiles that you can apply to devices throughout your network.

You can create a network hierarchy that represents your network's geographical locations. Your network hierarchy is built up of **sites**. By default, there is one site called Global. This Global site can be expanded upon to contain areas, and optionally, subareas (areas within areas). Within areas we create buildings and floors. You should create areas, buildings, and floors to easily identify where to apply design settings or configurations later. 

The network hierarchy has a predetermined hierarchy:

- **Areas**: Do not have a physical address. You can think of areas as the largest element. Areas can contain buildings and subareas. For example, an area named `United States` can contain a `California` subarea, and the subarea `California` can contain a `San Jose` subarea.

- **Buildings**: Include a physical address and contain floors and floor plans. When you create a building, you must specify a physical address or latitude and longitude coordinates. Buildings cannot contain areas. By creating buildings, you can apply settings to a specific location.

- **Floors**: Exist within buildings and consist of cubicles, walled offices, wiring closets, and so on. You can add floors only to buildings.

## Settings and Credentials Background

The Design area is where you create the structure and framework of your network, including the logical topology, network settings, and device type profiles that you can apply to devices throughout your network.

The settings and credentials which we assign to the hierarchy allow us to be deterministic in where we inherit settings from parent objects and where we override settings in the child objects.

This allows us to deploy changes to the network with localized maintenance windows and or slowly roll out changes through multiple sites without impacting the entire network. 

As with all the Design, Policy & Provisioning elements, they are all tied to the hierarchical nature of Cisco Catalyst Center. 

> **Prerequisites**: **Completed** the previous section **Orientation**

> [**Next Section**](./02-integration.md)
