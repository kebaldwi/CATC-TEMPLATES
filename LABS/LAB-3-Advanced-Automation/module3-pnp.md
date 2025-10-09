# PnP Claiming

## Overview

This module is designed to be used after first completing the **[Building PnP Templates](../LAB-3-Advanced-Automation/module2-day0-template.md)** and has been created to address how to operationalize **Plug and Play (PnP) Templates** to onboard devices into Catalyst Center. This module will go through the network profile, and how to claim devices as well as the claim process. 

### Overview Summary

In this section will go through the flows involved with **PnP**. This will allow us to create successful onboarding of network devices into Catalyst Center for Greenfield situations.

This is the lab we will be utilizing. Notice the **PnP Target Switch**. This is the C9300-1, which is a variant of the 9300 family. We will be building a configuration for this device from a sample configuration.

![json](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_PnPLab2.png?raw=true "Import JSON")

## Exercises

### Step 1 - Navigate to Template Hub

Navigate to the CLI Template Hub on Catalyst Center **`Tools > Template Hub`**

![json](../../ASSETS/LABS/CATC/MENU/catc-menu-5.png?raw=true "Import JSON")

### Step 2 - PnP Template 

We have previously built a PnP template within the **Template Hub** within **Catalyst Center**. The Onboarding template has the minimal configuration and is designed to bring up device connectivity with Catalyst Center. Below is an example of a Jinja2 for comparison only. 

Compare your template with the example in the section below. Did you miss anything important?

<details closed>
<summary> Expand to review the Jinja Example </summary></br>

[//]: # ({% raw %})

```J2
{# <------Onboarding-Template-------> #}
{# To be used for onboarding when using Day N Templates #}
{# Define Variables provision with vlan and port channel #}
!
{# Set MTU if required #}
{% if SystemMTU != 1500 %}
    system mtu {{ SystemMTU }}
{% endif %}
!
{# Set hostname #}
hostname {{ Hostname }}
!
{% set VtpDomain = Hostname %}
!
{# Set VTP and VLAN for onboarding #}
vtp domain {{ VtpDomain }}
vtp mode transparent
!
{# Set Management VLAN #}
vlan {{ MgmtVlan }}
!
{% if MgmtVlan > 1 %}
  name MgmtVlan
  {# Disable Vlan 1 (optional) #}
  interface Vlan 1
   shutdown
{% endif %}
!
{# Set Interfaces and Build Port Channel #}
!{{ Portchannel }}
interface range {{ Interfaces }}
 shut
 switchport mode trunk
 switchport trunk allowed vlan {{ MgmtVlan }}
 {% if "," in Interfaces || "-" in Interfaces %}
    channel-protocol lacp
    channel-group {{ Portchannel }} mode active
 {% endif %}
 no shut
!
{% if "," in Interfaces || "-" in Interfaces %}
  interface Port-channel {{ Portchannel }}
   switchport trunk native vlan {{ MgmtVlan }}
   switchport trunk allowed vlan {{ MgmtVlan }}
   switchport mode trunk
   no port-channel standalone-disable
{% endif %}
!
{# Set Up Managment Vlan {{ MgmtVlan }} #}
interface Vlan {{ MgmtVlan }}
 description MgmtVlan
 ip address {{ SwitchIP }} {{ SubnetMask }}
 no ip redirects
 no ip proxy-arp
 no shut
!
ip default-gateway {{ Gateway }}
!
{# Set Source of Management Traffic #}
ip domain lookup source-interface Vlan {{ MgmtVlan }}
ip http client source-interface Vlan {{ MgmtVlan }}
ip ftp source-interface Vlan {{ MgmtVlan }}
ip tftp source-interface Vlan {{ MgmtVlan }}
ip ssh source-interface Vlan {{ MgmtVlan }}
ip radius source-interface Vlan {{ MgmtVlan }}
logging source-interface Vlan {{ MgmtVlan }}
snmp-server trap-source Vlan {{ MgmtVlan }}
ntp source Vlan {{ MgmtVlan }}
!
netconf-yang
!
```

[//]: # ({% endraw %})

</details></br>

This Jinja2 PnP Template has the settings necessary to bring up a Layer2 access switch with enough configration to be supported by Catalyst Center for the rest of the provisioning process. 

As guidance it is **highly recommended** that you use **Jinja2** moving forward, due to its modularity and capabilities. You can however achieve the same results with **Velocity**, but the scripting language is not as feature rich.

The onboarding template is designed to set up static addressing and a hostname entry along with updating the management source interfaces for management connectivity. This file is transfered to the target device in a single file as opposed to linne by line configuration which accomodates the changes in network connectivity which may be lost when iterating line by line.

Please note the modifications to the source addressing for all protocols and specifically the **HTTP Client** source interface. This helps Catalyst Center to know if or when the IP address changes for a device and update it in the inventory automatically.

> [!TIP]
> We will attempt to use the template that you built in the previous module, but this will be kept in reserve as a fall back plan.

</br>
<details closed>
<summary> Expand if needed for Files and Import Instructions</summary>

### Step 2.b - Optional PnP Template Import - **(OPTIONAL)**

1. Should you have issues with the template you built you can always import this into the Onboarding Configuration Project.
  
   <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/ONBOARDING/JSON/Platinum_PnP_Jinja2_Template.json">⬇︎Platinum_PnP_Jinja2_template.json⬇︎</a> 

2. Navigate to the **Template Hub** within Catalyst Center through the menu **`Tools > Template Hub`**.

   ![json](../../ASSETS/LABS/CATC/MENU/catc-menu-5.png?raw=true "Import JSON")

3. Click **Import** then select **Template(s)** from the menu.    

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/IMPORT/template-import-1.png?raw=true "Import JSON")

4. Select **Onboarding Configuration** for the Network Profile from the dropdown selection. 

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/IMPORT/template-import-2.png?raw=true "Import JSON")

5. Click the link to select files from the local computer. In the Windows explorer window search for the **Platinum_PnP_Jinja2_Template** json file, select it and open it into the import window.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/IMPORT/template-import-4.png?raw=true "Import JSON")

6. Click **import** to install and import the template.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/IMPORT/template-import-5.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/IMPORT/template-import-6.png?raw=true "Import JSON")

</details>

### Step 3 - Create a Network Profile

Next we need to assign the Onboarding Template to a site using the Network Profile. 

   1. Navigate to Network Profiles by selecting **`Design > Network Profiles`** 

      ![json](../../ASSETS/LABS/CATC/MENU/catc-menu-1.png?raw=true "Import JSON")

   2. Select **Switching** under **Add Profile**

      ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-1.png?raw=true "Import JSON")

   3. Click **&#8853;** and complete the following: 

         ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-2.png?raw=true "Import JSON")

      1. Enter the **Profile name** 
      2. Select the **Onboarding Template** tab and click **Add Template** and select the **PnP-Template-J2** template

         ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-3.png?raw=true "Import JSON")

      3. With the **PnP-Template-J2** template selected that you either built or imported earlier and click **Add** then close the **Add Template** wizard    

         ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-4.png?raw=true "Import JSON")

   4. On the Onboarding Template page confirm the template(s) to be used for onboarding then **Save** the profile

      ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-5.png?raw=true "Import JSON")

   5. Click **Assign** to attach the network profile to the hierarchy 

      ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-6.png?raw=true "Import JSON")

   6. Select the sites to apply the profile within the hierarchy and click **Save**.

      ![json](../../ASSETS/LABS/NETWORKPROFILES/LAB3/switch-pnp-7.png?raw=true "Import JSON")

### Step 4 - Claiming the Device 

At this point Catalyst Center is set up and ready for Plug and Play to onboard the first device. Provided the discovery and dhcp assignment are aligned, the device should when plugged in find Catalyst Center and land in the plug n play set of the devices section within the provisioning page.

At this point you can claim the device putting it in a planned state for onboarding onto the system. To do this do the following:

   1. Within Catalyst Center Navigate to **`Provision > Plug and Play`**      

      ![json](../../ASSETS/LABS/CATC/MENU/catc-menu-3.png?raw=true "Import JSON")

   2. Put a checkmark next to the device *Switch* to be claimed
   3. Click the **Actions>Claim** link and walk through the workflow    

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-1.png?raw=true "Import JSON")

   4. Section **1** click the **Assign** link to select the part of the hierarchy to assign the device

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-2.png?raw=true "Import JSON")

   5. Click the part of the hierarchy to assign the device to and then click **Assign**
   
      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-3.png?raw=true "Import JSON")

   6. The assigned site will appear on the section page, click **next** to continue

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-4.png?raw=true "Import JSON")

   7. Section **2** you can click the hyperlinks to the right of the workflow page and view or amend the templates and images utilized. We will make no changes so click **next** to continue   

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-5.png?raw=true "Import JSON")

   8. Section **3** select the device **serial number** on the left and fill in the variables within the template click **next**. Please use the following:
   
      * Hostname type `c9300-1`
      * Management Vlan enter `5`
      * Interfaces `Gi1/0/10, Gi1/0/11`
      * IP Management Address `192.168.5.3`
      * Subnet Mask `255.255.255.0`
      * Gateway `192.168.5.1`
      * VTP Domain `Cisco` *(if required)*

      > [!NOTE] 
      > Leave the the settings default as we built them as default values

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-6.png?raw=true "Import JSON")

   9. Section **4** review the elements including configuration to be deployed. Click **Claim** followed by **Yes** to initiate

      ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-7.png?raw=true "Import JSON")

   10. At this stage the device will be placed in **Planned** state, and will cycle through **Onboarding** and **Provisioned** when complete     

       ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-8.png?raw=true "Import JSON")

   11. After the device is completed it will appear in the device inventory after being sync'd with Catalyst Center.      

       ![json](../../ASSETS/LABS/DAY0DAYN/LAB3-PNP-CLAIM/c9300-1-claim-9.png?raw=true "Import JSON")

## Summary

Congratulations you have completed the onboarding of the **c9300-1** and deployed the **PnP Template** via the PnP Claim process. The next modules will cover **DayN Templating** and **Provisioning**.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Building DayN Templates Module**](../LAB-3-Advanced-Automation/module4-dayn-template.md)

> [**Return to Lab Menu**](./README.md)