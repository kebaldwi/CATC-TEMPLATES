# PnP Preparation

## Overview

This module is the first one in a series of modules within the Wired Automation Lab. You may use the steps in the [Cisco Enterprise Networks Hardware Sandbox](https://dcloud2-sjc.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen) environment, or equally, you might utilize them as part of a Proof of Concept setup at a customer's lab. These procedures may also help form part of a deployment or implementation. Use them to ensure that all the necessary steps are complete before onboarding any devices within Catalyst Center.

## General Information

As you may recall, in the informational sections of this repository, we described various methods of discovery for a device and the preliminary things required for proper zero-touch provisioning. This lab will ensure a successful connection to Catalyst Center by helping to deploy the initial concepts.

We will be utilizing the lab in this manner:

![json](./images/DCLOUD_Topology_PnPLab2.png?raw=true "Import JSON")

## Lab Credentials:

| Platform:       | IP Address:    | Username | Password   | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| Router          | 198.18.133.145 | netadmin | C1sco12345 |
| Switch 1        | 198.18.128.22  | netadmin | C1sco12345 |
| Switch 2        | 198.18.128.23  | netadmin | C1sco12345 |

## Catalyst Center and ISE Integration

In this lab our focus changes slightly as we start to automate for host onboarding. A large component of host onboarding is the authentication of hosts and assignment within the network. In this section and in preparation for the steps which follow we will integrate Catalyst Center with Identity Services Engine. This integration allows pxGrid communication between the two and allows for automation of configuration within ISE for Network Access Devices, SGT, SGACL, and Policys.

### Step 1 - Prepare ISE for Catalyst Center Integration

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Identity Services Engine (ISE) and select the hamburger menu icon to open the system menu.

   ![json](./images/module1-preparation/ise-dashboard.png?raw=true "Import JSON")

2. From the system menu under Administration select PxGrid Settings

   ![json](./images/module1-preparation/ise-menu.png?raw=true "Import JSON")

3. On the PxGrid Settings page select both of the available options and click Save to allow Catalyst Center to integrate.

   ![json](./images/module1-preparation/ise-pxgrid-settings.png?raw=true "Import JSON")
   ![json](./images/module1-preparation/ise-pxgrid-setup.png?raw=true "Import JSON")

### Step 2 - Catalyst Center and ISE Integration

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon and navigate to the System > Settings menu item.

   ![json](./images/module1-preparation/dnac-system-settings.png?raw=true "Import JSON")

2. Within the System Settings page navigate down the list on the left and select the Authentication and Policy Server section.

   ![json](./images/module1-preparation/dnac-system-settings-aaa.png?raw=true "Import JSON")

3. On the page select from the dropdown ISE to configure ISE integration.

   ![json](./images/module1-preparation/dnac-system-settings-aaa-ise.png?raw=true "Import JSON")

4. Enter the information as seen on the page and click save.

   ![json](./images/module1-preparation/dnac-system-settings-aaa-ise-config.png?raw=true "Import JSON")

5. A popup will appear as the ISE node is using an untrusted SelfSigned Certificate. For lab purposes Accept the certificate, this may appear a couple of times as shown.

   ![json](./images/module1-preparation/dnac-system-settings-aaa-ise-trust.png?raw=true "Import JSON")

6. You will see the the various stages of integration proceed and finally a success message as shown below.

   ![json](./images/module1-preparation/dnac-system-settings-aaa-ise-done.png?raw=true "Import JSON")
   ![json](./images/module1-preparation/dnac-system-settings-aaa-ise-complete.png?raw=true "Import JSON")

## Step 3 - Router Connectivity

Essentially we will be turning the 9300-2 switch into a distribution switch to allow for the access switch to be onboarded over a port channel. Port channels are typically how switches are connected for redundancy and it seems fair to use that as the basis for the lab. 

> [!NOTE]
> It is possible to use a routed connection, but then LAN Automation is typically used for routed access as it is in SD-Access. It is possible however to use PnP for routed access without LAN automation but that is outside the scope of todays lab.

### Configuring the 4331 Router 

To set up the lab to allow for the above connectivity we will complete , please log into the console connection of the **4331** by clicking on dropdown button under the icon in DCLOUD, and selecting 'Console'. New tab will open, click 'Connect' - you should now be connected to the console of the router. 

The credentials are noted above for reference, copy-paste the password into Hardware Console tab after issuing enable CLI.  Once you are in enable mode on 4331 hardware console, issue commands:

> **Warning:** *use commands against the LAB Environment.*

#### 4331 Router Configuration

```vtl
!
conf t
!
!disable port 0/0/1 for the templating lab
int gi 0/0/1
 shutdown
 end
!
wr

```

## Step 4 - Distribution Connectivity

To continue on, as we will be using the 9300-2 as a Distribution switch we will need to set it up appropriately for PnP processes to work. We intend to have a management interface on the device. In this lab, we will set up a VLAN interface for both management and connectivity. 

> [!NOTE]
> You don't have to do it this way; we are just giving a relatively uncomplicated example, and you can alter this to suit your needs. As the device connects to the front-facing ports, we have to rely on the default configuration. 

As you may recall, a factory default configuration uses VLAN 1 as no other VLAN exists, and by default, it accepts DHCP addresses. We can use this method in the PnP process. However, the management VLAN may be different, and so may the native VLAN structure of our environment. To that end, we must use the **`pnp startup-vlan`** command, which allows the device to use varying VLANs in PnP and should be set up and configured on the upstream switch. 

### Configuring the 9300-2 as a Distribution Switch

As depicted in the following image, the 9300-2 will serve as the upstream neighbor for this exercise and the environment's distribution switch. The Catalyst 9300-1 will act as the target switch, which we will deploy via PnP and DayN templates.

![json](./images/DCLOUD_Topology_PnPLab2.png?raw=true "Import JSON")

For the lab, we will utilize **VLAN 5** as the management VLAN. Connect to switch **c9300-2** and paste the following configuration:

#### 9300-2 Distribution VLAN Configuration

```vtl
config t
!
vlan 5
name "mgmtvlan"
!
int vlan 5 
 ip address 192.168.5.1 255.255.255.0
 ip ospf 1 area 0
 no shutdown
!
pnp startup-vlan 5
end
!
wr

```

The **`pnp startup-vlan 5`** command will program the target switches port connected with a trunk and automatically add the vlan and SVI to the target switch making that vlan ready to accept a DHCP address. 

> [!NOTE]
> The feature is available on switches running IOS-XE 16.6 code or greater as upstream neighbors. Older switches or upstream devices that cannot run the command should utilize VLAN 1 and then set up the correct management VLAN modified as part of the onboarding process.

### Configuring the 9300-2 Distribution Switch Downlink

Typically, the Target switch is connected via a trunk to a single port or a bundle of ports as part of a port channel. 

Building a single port connection to the target switch, requires using a simplified configuration; however, we will **not be utilizing** this method in this lab. 

<details closed>
<summary> Example of Building a single port connection to the target switch</summary>

```vtl
!
conf t
!
  interface gi 1/0/10
     description Single Port PnP Test Environment to Cataylist 9300
     switchport mode trunk
     switchport trunk allowed vlan 5
  interface gi 1/0/11
     description Shutdown for Single Port PnP Test Environent
     shutdown
     end
!
wr

```

</details>

#### 9300-2 Layer 2 Configuration

In this exercise, we will build a layer two trunk as part of a Port Channel. This bundle of ports will connect to the Target switch. The upstream ports on the 9300-1 will automatically be programmed as a result. 

If we are using a port-channel initially, you want to ensure that the port-channel can operate as a single link within the bundle and, for that reason, use passive methods for building the port-channel bundles on both the Target and Upstream Neighbor for maximum flexibility. 

Additionally, add the **no port-channel standalone-disable** command to ensure the switch does not automatically disable the port-channel if it does not come up properly.

```vtl
!
conf t
!
  interface range gi 1/0/10-11
     description PnP Test Environment to Catalyst 9300
     switchport mode trunk
     switchport trunk native vlan 5
     switchport trunk allowed vlan 5
     channel-protocol lacp
     channel-group 1 mode passive
!
  interface Port-channel1
     description PnP Test Environment to Catalyst 9300
     switchport trunk native vlan 5
     switchport trunk allowed vlan 5
     switchport mode trunk
     no port-channel standalone-disable
     end
!
wr

```

## Step 5 - Catalyst Center Discovery

In order for **Plug and Play (PnP)** to work, we need to the device to communicate with Catalyst Center. The device must get the address of Catalyst Center through the PnP process through what is known as discovery. 

The PnP components are as follows:

![json](../../ASSETS/COMMON/CATC/pnp-workflows.png?raw=true "Import JSON")

### Step 5.1 - PnP Requirements

#### Discovery Method

There are **3 automated discovery methods** that can be used to assist with Catalyst Center discovery process:

1. **DHCP with option 43**
```shell
   PnP string: 5A1D;B2;K4;I172.19.45.222;J80 added to DHCP Server 
``` 
2. **DNS lookup**
```shell
   pnpserver.localdomain resolves to Catalyst Center VIP Address
```
3. **Cloud re-direction https://devicehelper.cisco.com/device-helper**
   **which, re-directs to on-prem Catalyst Center IP Address**

Of the discovery methods **DHCP** is the easiest to implement as no changes are required with the *Self Signed Certificate (SSC)* on **Catalyst Center** as it already includes the IP address by default. 

If you are deploying PnP using **DNS** discovery or you are building a cluster then you will need to go through the process of acquiring a certificate with Subject Alternative Names to include the **DNS** and **IP** entries to allow for the following:

1. All Node IP Addresses
2. All VIP Addresses for Cluster
3. All DNS Host entries for Nodes
4. VIP DNS Host entry for Cluster
5. pnpserver Host or CNAME entries

<details closed>
<summary>To build a certificate in dCLOUD follow these steps </summary>

To Build a certificate for use in Catalyst Center for PnP, please follow this outline of steps. Each step can take some time so plan accordingly.

1. On the Active Directory Server add the roles for the Certificate Authority to allow WEB enrollment
2. Add the required DNS entries for Catalyst Center as per the sections below
3. On Catalyst Center in CLI create a CSR using openssl 
4. Enroll Catalyst Center via the CSR on the Windows CA
5. Upload the Certificate to Catalyst Center

To utilize DNS Entry for Discovery purposes Certificates will need to be rebuilt with Subject Alternative Names. Please utilize the process documented in the following [**Catalyst Center Certificates**](./Certificates.md) for information on that process.

Follow this guide for more information on the finer details.

[Catalyst Center Security Best Practices Guide](./DNACenter_security_best_practices_guide.pdf)

</details>

#### DHCP Addressing

Additionally, as the device will initially have no configuration at all, we will need to supply the Target switch with an IP address within the management network. Thus **DHCP** is a requirement for **PnP Onboarding**. This may be set up on the Distribution or Router but typically it is set up on a Server built for the purpose, like an IP Address Manager (IPAM).

We require a DHCP scope to supply the IP address within the management network temporarily in order to complete the device configuration and onboarding. The scope should be carved out from an unused range. It also can be a static reservation, as DHCP servers can reserve addresses for specific MAC addresses. 

The DHCP scope would incorporate the following parameters sufficient to issue an IP address:

* **network**
* **default gateway**
* **domain**                
  - *required for DNS PnP discovery*
* **name-server ip**        
  - *required for both DNS and CLOUD PnP discovery*
* **option 43**             
  - *required for DHCP discovery*

Obviously a dhcp relay or helper statement is required on the gateway router interface pointing towards the DHCP server.

> [!NOTE]
> Choose one method of discovery, to avoid frustration.

There are many options for DHCP services. Although you have many options for DHCP, we will utilize either Windows or IOS DHCP configurations in this lab. Configure the DHCP scope to one of the following:

1. Switch or Router
2. Windows DHCP Server
3. InfoBlox or other 3rd party server if available

During this lab setup, please choose which option you wish to use for DHCP for PnP services and follow those subsections.

### Step 5.2 - PnP Discovery Configuration

Within the DCLOUD environment we can accomodate the build and testing of the following Discovery methods. Please select one option link in the following list to move through the configuration instructions to continue the lab.

1. **DHCP Discovery Options**
   - [**Configure DHCP Discovery using IOS DHCP Service**](./module1a-dhcp-ios.md)
   - [**Configure DHCP Discovery using Windows DHCP Service**](./module1b-dhcp-svr.md)
2. **DNS Discovery Options**
   - [**Configure DNS Discovery using IOS DHCP and Windows DNS Services**](./module1c-dns-ios.md)
   - [**Configure DNS Discovery using Windows based DHCP and DNS Services**](./module1d-dns-svr.md)
