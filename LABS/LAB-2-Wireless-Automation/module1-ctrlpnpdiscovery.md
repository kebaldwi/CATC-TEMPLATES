# Wireless Controller Discovery or PnP

Within this lab module, we will concentrate our efforts on the discovery or PnP of each of the devices by **Catalyst Center**, so that we can onboard and gain management of those devices. 

Within this lab we will concentrate on the following which are typical in most Enterprise Networks today:

1. Controller Discovery
2. Access Point switch port configuration
3. Access Point Onboarding

To begin lets review the wireless within the Cisco DCLOUD environment.

### Required Components 

For these labs we will be focusing on the wireless aspects, and while the switching and routing has been setup ahead of time our focus will be on the following:

Virtual Machines:

    Catalyst Center 2.3.5.6 or better
    Identity Services Engine (ISE) 3.0 Patch 4 or better (deployed)
    Wireless LAN Controller - C9800 running IOS-XE Bengaluru 17.5.1 code or better
    Windows 10 Jump Host 
    Windows Server 2019 - Can be configured to provide identity, DHCP, DNS, etc.
    Windows 10 Clients

Hardware Devices:

    Catalyst 9300 Switch - 17.06.01 IOS-XE Code with Embedded Wireless Controller (EWC) and ThousandEyes Enterprise Agent
    9130AX Access Points
    Silex Controllers (3 Wired NIC's and 1 Wireless NIC)

### Logical Topology

The lab envionment that is available is depicted here:

For routing in the environment an OSPF IGP process has been created to propogate internal route information. Within the access switches which are connected at Layer 3 to the router, we have estansiated a layer 2 port channel between them and initiated various vlans for Access Point connectivity and for the clients, whose gateway is built on an HSRP instance shared between the two switches.

The 9130AX Access Points are connected to both access switches and the ports are automatically configured via the AUTOCONF feature.

![json](../../ASSETS/LABS/WIRELESS/DCLOUD_Topology_Wireless-v2.png?raw=true "Import JSON")

## Lab Credentials:

| Platform:       | IP Address:    | Username | Password   | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| 9800-1          | 198.19.11.2    | admin    | C1sco12345 |
| 9800-2          | 198.19.11.3    | admin    | C1sco12345 |
| Router          | 198.18.133.145 | netadmin | C1sco12345 |
| Switch 1        | 198.18.128.22  | netadmin | C1sco12345 |
| Switch 2        | 198.18.128.23  | netadmin | C1sco12345 |
| AP-1            | DHCP Assigned  | Cisco    | Cisco      |
| AP-2            | DHCP Assigned  | Cisco    | Cisco      |

## Lab Section 1 - Controller Discovery

To get started with Wireless configuration and automation we first need to onboard the Wireless Controller into Catalyst Center. In the preparation lab we discovered the rest of the topology, set up the required services, and so we will now concentrate her on the controller. 

While we have the ability to PnP a Wireless Controller typically these are estantiated initially with IP information on the physical hardware. As a result, and because of the current liimitations within the DCLOUD lab, we will concentrate on Discovery methods here. We will cover Controller PnP separately in another module (TBD).

<details open>
<summary> Click for Details and Sub Tasks</summary>

### Step 1 - ***Setup Discovery Job***

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Tools>Discovery`.

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-navigation-discovery.png?raw=true "Import JSON")

2. On the Discovery page click `Add Discovery`.

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-dashboard.png?raw=true "Import JSON")

3. The **New Discovery** workflow will begin. Click **Next** to continue.

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-wizard.png?raw=true "Import JSON")

4. On the **New Discovery** Page enter the following:
   1. *Discovery Name* for the discovery `WIRELESS`
   2. Select *Discovery Type* of `IP Address/Range`
   3. Enter *From - To* fields with `198.19.11.2`

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new.png?raw=true "Import JSON")

5. On the new Credentials page we will add credentials for the Wireless Controller. The credentials on the controller are different to those of the Global settings shown. Catalyst Center allows for us to use separate credentials where necesssary. 

   1. To Begin do the following;

      1. Click **CLI**
      2. Hover over the **Add CLI Credential** link
      3. In the sub menu select **Global** to add the credential to the Global store.

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-cli.png?raw=true "Import JSON")

   2. To add the details for the **CLI** Credential:
   
      1. Enter the following:
      - *Name* as `admin`
      - *Username* as `admin`
      - *Password* as `C1sco12345`
      - *Enable Password* as `C1sco12345`

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-cli-add.png?raw=true "Import JSON")

   3. To add **SNMPv2c Read** Credentials do the following;

      1. Click **SNMPv2c Read**
      2. Hover over the **Add SNMPv2c Read Credential** link
      3. In the sub menu select **Global** to add the credential to the Global store.

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-snmp-ro.png?raw=true "Import JSON")

   4. To add the details for the **SNMPv2c Read** Credential:
   
      1. Enter the following:
      - *Name* as `public`
      - *Read Community* as `public`

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-snmp-ro-add.png?raw=true "Import JSON")

      > [!NOTE] 
      > a Warning will appear after the Save. Click `Ok` this is expected.

   5. To add **SNMPv2c Write** Credentials do the following;

      1. Click **SNMPv2c Write**
      2. Hover over the **Add SNMPv2c Write Credential** link
      3. In the sub menu select **Global** to add the credential to the Global store.

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-snmp-rw.png?raw=true "Import JSON")

   6. To add the details for the **SNMPv2c Write** Credential:
   
      1. Enter the following:
      - *Name* as `private`
      - *Write Community* as `private`

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-new-snmp-rw-add.png?raw=true "Import JSON")

      > [!NOTE] 
      > a Warning will appear after the Save. Click `Ok` this is expected.

   7. To add **NETCONF** Credentials do the following;

      1. Click **NETCONF**
      2. Select the existing NETCONF port **830**
      3. Click **Next** to add the credentials

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-netconf-add.png?raw=true "Import JSON")

6. On the **Advanced Settings** page as no changes will be made, click **Next** to continue

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-advanced.png?raw=true "Import JSON")

7. On the **Assign Devices to Site** page, do the following:

   1. Select **Assign devices to an existing site** 
   2. Within the hierarchy click the **>** symbol to open each layer and select the **Building**
   3. Click **Next** to continue

      ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-assign.png?raw=true "Import JSON")

8. On the **Schedule Job** page click **Next** to continue the discovery

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-schedule.png?raw=true "Import JSON")

9. On the **Summary Job** page click **Start Discovery and Telemetry** to continue and **Start** the discovery task

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-summary.png?raw=true "Import JSON")

10. On the next page click **View Discovery** to return to the the **Discovery Dashboard**

    ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-view.png?raw=true "Import JSON")

### Step 2 - ***Verifying Discovery Job***

1. On the **Discovery Dashboard** click the **WIRELESS**  discovery to view the results

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-select.png?raw=true "Import JSON")

2. After a while the discovery will display the following results

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-discovery-results.png?raw=true "Import JSON")

3. Navigate to the Inventory through the menu. Select `Provision>Network Devices>Inventory`

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-navigation-inventory.png?raw=true "Import JSON")

4. After some time the Wireless Controller will appear as shown in the inventory.

   ![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dnac-inventory-controller-results.png?raw=true "Import JSON")

</details>

## Lab Section 2 - PnP of Wireless Controller 

The lab within DCLOUD does not today have the ability to run PnP of the Controller, but please check out this video which explains the process. 

<div align="center">
   <a href="https://www.youtube.com/watch?v=Vl7AfhNaGuc"><img src="https://img.youtube.com/vi/Vl7AfhNaGuc/0.jpg" style="width=560; height=315;"></a>
</div>

## Summary

Congratulations you have completed the Controller Discovery module of the lab and the Wireless LAN Controller is ready for configuration and provisioning. Please use the navigatation below to continue your learning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to WLAN Creation Module**](../LAB-2-Wireless-Automation/module2-wlans.md)

> [**Return to Lab Menu**](./README.md)
