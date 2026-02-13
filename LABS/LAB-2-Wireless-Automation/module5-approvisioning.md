# Wireless Access Point Provisioning

Within this lab module, we will concentrate our efforts on the PnP of each of the access points by **Catalyst Center**, so that we can onboard and gain management of those devices. 

Within this lab we will concentrate on the following which are typical in most Enterprise Networks today:

1. DHCP Address Scope
2. Catalyst Center Discovery
3. Access Point switch port configuration
4. Access Point Onboarding

To begin lets review the wireless within the Cisco DCLOUD environment.

## Required Components 

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

## Logical Topology

The lab envionment that is available is depicted here:

For routing in the environment an OSPF IGP process has been created to propogate internal route information. Within the access switches which are connected at Layer 3 to the router, we have estansiated a layer 2 port channel between them and initiated various vlans for Access Point connectivity and for the clients, whose gateway is built on an HSRP instance shared between the two switches.

The 9130AX and or 4800 Access Points are connected to both access switches and the ports are automatically configured via the AUTOCONF feature.

![json](../../ASSETS/LABS/WIRELESS/DCLOUD_Topology_Wireless-v2.png?raw=true "Import JSON")

# Lab Section 1 - Access Point PnP

In the preparation lab we discovered the rest of the topology, set up the required services, and part of those services were DHCP addresses which are help within scopes on the Windows AD Server. 

There are a few options for discovery using PnP. These were thoroughly discussed in the switching section and in a tutorial in the main menu. 

## Background 

In order to land on Catalyst Center though the device needs help in finding it. 

The PnP components are as follows:

![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/pnp-workflows.png?raw=true "Import JSON")

There are 3 automated methods to make that occur:

1. **DHCP with option 43**
```
   PnP string: 5A1D;B2;K4;I198.18.129.100;J80 added to DHCP Server
``` 
2. **DNS lookup**
``` 
   pnpserver.pnp.dcloud.cisco.com resolves to Catalyst Center VIP Address
```
3. **Cloud re-direction https://devicehelper.cisco.com/device-helper**
   **which, re-directs to on-prem Catalyst Center IP Address**

**Option 1:** requires that along with the IP address and gateway the DHCP server must offer a PnP string via option 43. This option is often used with Cisco wireless so you may want to incorporate option 60 and the use of vendor specific information to ensure the correct controller is referenced for the device in question. 

**Option 2:** requires that along with the IP address and gateway the DHCP server offer the domain suffix that the **pnpserver** record will reside in and a name server to resolve the address. Caveats here would be that if not all devices were to be landing on Catalyst Center then you may need sub domains.

**Option 3:** requires that along with the address and gateway the DHCP server offer a name server to resolve the address of **device-helper.cisco.com**. Additionally it requires the that Catalyst Center register a file with the PnP Connect portal which it will offer via SSL to a device which reaches out. In order to whitelist those devices, the serial number would have to be associated to the DNAC profile within software centrals pnp connect portal.

![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/pnp-connect.png?raw=true "Import JSON")

Once one of the options has been built devices will get the address and be pointed to and land on Catalyst Center within the PnP Device list.

<details open>
<summary> Click for Details and Sub Tasks</summary>

## Step 1 - ***DHCP as a Discovery Method***

DHCP services are important to understand primarily because along with the address and the gateway for connectivity is assigned option 43 which primes or directs the Cisco Access Point towards **Catalyst Center** or typically a **Wireless Controller**.

![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dhcp-lab-scope.png?raw=true "Import JSON")

Within the Scopes is a scope for the Access Point Vlan, aptly named *APVLAN* and within that you will see option 43 defined which is given to all clients within the scope.

![json](../../ASSETS/LABS/WIRELESS/module1-pnpdiscovery/dhcp-apvlan-option43.png?raw=true "Import JSON")

## Step 2 - ***Access Point Port Configuration***

The second part of the PnP equation is setting the environment up to allow for the device to get the address in question. This was previously accomplished in the setup procedure of the lab utilizing a template which was auto provisioned to the switch after discovery.

The Switch was configured to automatically configure switch ports with connected Access Points with the following configuration. This was accomplished through **AUTOCONF** as explained in previous labs 7 and 8.

This is only one way of accomplishing this task, many others can be used, as was proven out in lab 8, with zero trust environment, and change of authorization being the catalyst for deploying an `interface template`.

In this lab as we are focusing on Wireless, the port configuration was automatically assigned via **AUTOCONF** for simplicity.

The switch port configuration used in this lab is:

```
c9300-1#sh der int gi 1/0/2
  Building configuration...
  
  Derived configuration : 261 bytes
  !
  interface GigabitEthernet1/0/2
   description Access Point Interface
   switchport access vlan 999
   switchport trunk native vlan 10
   switchport trunk allowed vlan 10,20,30,40,999
   switchport mode trunk
   spanning-tree portfast
   spanning-tree bpduguard enable
  end
```

## Step 3 - ***Access Point Reset***

The Access Points are typically in varied states. Use the DCLOUD UI to console into each one then complete the following steps to clear them of any configuration:

1. Login to the Access Point with the following credentials: 
   - Username: `Cisco`
   - Password: `Cisco`
2. Enter privileged mode by issuing the command `enable`
3. when prompted for the enable password use the following credential:
   - Enable Password: `Cisco`
4. At the command prompt issue the following command, `capwap ap erase all`
5. When prompted enter at the `[confirm]` prompt.
6. The AP will clear its config and reboot.
7. After a few moments have passed check the PnP Claim page and the AP should be in the list.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-unclaimed.png?raw=true "Import JSON")

At this point of the process the Access Points should appear in the PnP Claim window.

## Step 4 - ***Access Point Claim***

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select **`Provision > Network Devices > Plug and Play`**.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-menu-provision-pnp.png?raw=true "Import JSON")

2. On the *Plug and Play* page the following will appear. Notice the two access points have discovered and landed on Catalyst Center.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-unclaimed.png?raw=true "Import JSON")

3. On the *Plug and Play* page select the two access points as shown, then click on *Actions > Claim* within the **Actions** menu. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim.png?raw=true "Import JSON")

4. Within the **Claim** workflow on page **1** you will notice the Access Points may already be within the site **`Global/DNAC Template Lab/Building/Floor 1`** if not you have an option to select the Floor1 at this time if necessary complete the task. When ready click **Next** to continue the workflow. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-1.png?raw=true "Import JSON")

5. Within the **Claim** workflow on page **2** we need to assign an *RF Profile*. When ready click **Assign** to continue on this section. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-2-assign-a.png?raw=true "Import JSON")

6. A slide out **Configuration** window will appear. Please complete the following:
   1. Click the **Radio Frequency Profile** drop down selection window
   2. From the list that appears select **BASIC-RFP** which we previously created and click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-2-rfprofile-1.png?raw=true "Import JSON")
   
   3. Then click the **`...`** on the right and a menu will appear. Select the option to duplicate the **BASIC-RFP** Profile to the other Access Point.

      ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-2-rfprofile-2.png?raw=true "Import JSON")

   4. Another window will appear and **select** the Access Point or multiple Access Points to assign. Then click **Assign**

      ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-2-rfprofile-3.png?raw=true "Import JSON")

7. Within the *Claim* workflow on page *2* ensure both access points have assigned *RF Profile's*. When ready click **Next** to continue the workflow. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-2-rfprofile-4.png?raw=true "Import JSON")

8. Within the *Claim* workflow on page *3* ensure both access points appear as shown. Click the **Preview Day-0 Config** links to discover what will be pushed to the access points.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-summary-1.png?raw=true "Import JSON")

9. Within the *Claim* workflow on page *3*  a *Summary Page* will slide out. Click on the details to display the relevant information. When ready click **X** at the top right to close the *Summary Page* and to continue the workflow. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-summary-2.png?raw=true "Import JSON")

10. Within the *Claim* workflow on page *3* when ready click **Claim** to Claim the access points and begin the Day-0 provisioning process. 

    ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claiming.png?raw=true "Import JSON")

11. A verification popup will appear, when ready click **Yes** to continue the Claim of the access points and begin the Day-0 provisioning process. 

    ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claiming-verify.png?raw=true "Import JSON")

12. The access points will be displayed within the *Plug and Play* *Unclaimed* window as shown here initally as **Planned**. They will over time show **Onboarding**. 

    ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-planned.png?raw=true "Import JSON")

13. Eventually will show as **Provisoned** under the *Provisioned* section

    ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-pnp-ap-claim-provisioned.png?raw=true "Import JSON")

At this point the access points will synchronize with the inventory and display there for Day-N Provisioning.

</details>

# Lab Section 2 - Access Point Provisioning

With the access points now onboarded through the claim process, they are now in a manageable state. We can now provision the *Wireless SSID* to them within the *Wireless RF Profile*. To accomplish this please follow the steps in this section. This will need to be completed whenever the SSID, are changed or modified within the Wireless Profile for the access points and normally AP provioning check box facilitates that operation. As this is the initial configuration of the access points we must complete this process.

<details open>
<summary> Click for Details and Sub Tasks</summary>

1. Click the *Inventory* tab within the Provision Window. The following page will appear in the *Inventory* focus. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-inventory.png?raw=true "Import JSON")

2. Please do the following:
   1. Select the two access points as shown
   2. Click the *Actions* menu and select `Actions > Provision > Provision Device` to begin the provisioning workflow.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap.png?raw=true "Import JSON")

3. Within the *Provisioning* workflow on page *1* observe the settings only. When ready click **Next** to continue the Day-N provisioning process. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-1.png?raw=true "Import JSON")

4. Within the *Provisioning* workflow on page *2* observe the settings only. When ready click **Next** to continue the Day-N provisioning process. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-2.png?raw=true "Import JSON")

5. Within the *Provisioning* workflow on page *3* observe the device summarys only. When ready click **Deploy** to continue the Day-N provisioning process. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-3.png?raw=true "Import JSON")

6. Within the *Provisioning* workflow a slide-out Provision Device window will appear on page *3*. Leave the default selection of **Now**. When ready click **Apply** to continue the Day-N provisioning process. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-start.png?raw=true "Import JSON")

7. A verification popup will appear, when ready click **Yes** to continue the Claim of the access points and begin the Day-N provisioning process. 

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-start-verify.png?raw=true "Import JSON")

8. Within the *Inventory* tab within the Provision Window change the focus by clicking the area indicated and select the *Provision* focus. Then click the **See Details** link beside one of the access points and view the information displayed.

   ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-focus-provision.png?raw=true "Import JSON")
                                        dnac-provision-ap-focus-provison
10. A summary of the tasks applied to the selected access point will be displayed. 

    ![json](../../ASSETS/LABS/WIRELESS/module3-approvisioning/dnac-provision-ap-device-summary.png?raw=true "Import JSON")

</details>

## Summary

Congratulations you have completed the Access Point Plug and Play, and Provisioning and now have two correctly configured access points with SSID that can be used for testing. Please use the navigation below to continue your learning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to AI RF Profiling Module**](../LAB-2-Wireless-Automation/module6-airfprofiles.md)

> [**Return to Lab Menu**](./README.md)
