# Wireless LAN Design

Within this lab module, we will concentrate our efforts on the design aspects of creating Wireless LANs (WLANs) via **Catalyst Center**. Previously we have discovered the Wireless LAN Controller by **Catalyst Center**, and assigned it to a site within the hierarchy. At this point we will configure the various settings for the Wireless Design.

Within this lab we will concentrate on the following which are typical in most Enterprise Networks today:

1. Wireless LAN Creation
2. Wireless Profiles
3. RF Profiles
4. FlexConnect 
5. Controller Provisioning

## Logical Topology

To review the lab envionment that is available is depicted here:

For routing in the environment an OSPF IGP process has been created to propogate internal route information. Within the access switches which are connected at Layer 3 to the router, we have estansiated a layer 2 port channel between them and initiated various vlans for Access Point connectivity and for the clients, whose gateway is built on an HSRP instance shared between the two switches.

The 9130AX Access Points are connected to both access switches and the ports are automatically configured via the AUTOCONF feature.

![json](../../ASSETS/LABS/WIRELESS/DCLOUD_Topology_Wireless-v2.png?raw=true "Import JSON")

The clients will be connected connected to the network via FlexConnect due to the nature of the DCLOUD labs design. Where applicable we will call out the differences between FlexConnect and Local Mode Design.

The Wireless Clients will associate and connect to the SSID's within the lab and will then be dropped into one of the following VLAN via the trunk from the FlexConnect Access Point.

1. Vlan 20 - datavlan - 192.168.20.0/24
2. Vlan 30 - voicevlan - 192.168.30.0/24
3. Vlan 40 - guestvlan - 192.168.40.0/24

For simplicity we may utilize the Vlan 30 as a second Data network when proving out CoA or AAA Overide features.

## Lab Section 1 - Wireless LAN's

To get started with Wireless Controller configuration and automation we first need to build the settings, Wireless LAN environments and associated profiles for deployment. Each Wireless LAN can be built by Catalyst Center and all settings may be deployed either through the UI, from Model-Based Config (covered separately), and by Templates (covered separately)for extranious configuration which might be required.

This section will be devoted to building Wireless LAN's. Subsequent sections will cover the profiles and provisioning:

These will be divided into sub-modules.

1. [Building a PreShared Key (PSK) Wireless LAN](./module2a-psk.md)
2. [Building a Identity PreShared Key (iPSK) Wireless LAN](./module2b-ipsk.md)
3. [Building a Enterprise 802.1x (EAP) Wireless LAN](./module2c-eap.md)
4. [Building a Guest Wireless LAN](./module2d-open.md)

## Summary

At this point you will have successfully configured the **SSID's** on the **Wireless Controller** from **Catalyst Center**. During this lab we configured SSID's, Wireless Network Profiles. The next step is creating an **RF Profiles** followed by provisioning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to RF Profile Provisioning Module**](../LAB-2-Wireless-Automation/module3-rfprofiles.md)

> [**Return to Lab Menu**](./README.md)