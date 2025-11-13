# PnP and Discovery

## Overview

This module is designed to be used after first completing the PnP preparation and has been created to address how to use both PnP and Discovery to onboard devices into Catalyst Center. This two fold approach allows us to onboard both Greenfield and Brownfield devices. 

### Greenfield

When dealing with net new devices using the PnP process to onboard devices we utilize Onboarding templates within Catalyst Center to onboard Day Zero network devices with no configuration on the device. 

PnP Onboarding allows for the claim of a device and the ability to automate the deployment of configuration. It is important to note that Onboarding templates are transfered as a flat file and loaded into the configuration by a configure replace. 

This allows for the manipulation of uplinks and addressing without disconnectivity during reconfiguration from the upstream neighboring device. Additional source commands can be used to allow the device to automatically inform Catalyst Center of a change in address through the PnP profile applied and the source of the HTTP client information.

### Brownfield

When dealing with existing infrastructure, we want to absorb the device and its configuration into Catalyst Center to allow for monitoring and a gradual shift to automated management, as the device usually is in a running state supporting the network, and the configuration pre-exists.

Be aware that with Brownfield device configurations, there is no template learning capability for switching. As such configuration on the device may need modification prior to provisioning in some situations. If this is required you may want to Discover and then push a normalization template via REST API to remove settings that would cause ongoing provisioning errors.

### Overview Summary

In this section will go through the flows involved with PnP and Discovery to allow for the successful onboarding of network devices into Catalyst Center in both Brownfield and Greenfield situations.

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

## Greenfield Environments and Plug and Play (PnP)

Catalyst Center can be used for not only Plug and Play (PnP) but also Day N or ongoing changes to the network via templates. Customers will start by building out a PnP Onboarding Template which typically deploys only enough information to intially bring the device. 

### Considerations about Templates

While a PnP template could include the entire configuration for a traditional network device, it is Cisco's strong recommendation to utilize DayN Templates for the bulk of the configuration and to utilize PnP only for bringing up a stable reliable network connection for the network device.

The inventory database is not populated with specific information about a device prior to the completion of the claim process. This presents a challenge to onboarding as system variables, and bind variables cannot be utilized. Additionally, this means that the scripts irrespective of the language used would require a lot of manual inputs to variables, rather than pulling information known about the device post claim.

Another challenge is ongoing modifications. Templates used after the initial provisioning for DayN operations are within a Project, where as Onboarding templates are in a specific location in Catalyst Centers Template Hub. Use of an Onboarding Template post PnP is not practical. One because we would want to introduce afformentioned System and Bind Variables to simplify code, and remove repetition. Secondarily because those may change over time.

Remember that DayN templates are primarily used to apply ongoing changes to device configurations and allow ongoing modifications after initial deployment. They allow for the data collected in the inventory database to be used to automate without the need for a lot of input.

Another consideration is that part of a typical configuration would include some lines of code which could or should be built out automatically from information entered within the **Network Settings** of Catalyst Center. 

If a Design component is used for a specific task you should not deploy the cli code in a template to configure the task on the device or vice versa. Its a decision you have to make upfront and avoids a lot of lines in the templates and allows for a more UI centric configuration which is easier to maintain. 

As guidance try and use Design settings for as much of the configurations as you can leaving templates light and nimble for configurations which might change ongoing. Its both easier to maintain and troubleshoot.

## Section 1 - Prepare Postman 

We will use Postman to push a collection of REST API which will utlize data within environment variables to prepare the Catalyst Center for use in our lab

### Step 1 - Prepare Postman Collection **(REQUIRED)** 

While a more extensive set of settings can be built out for a deployment we will limit the configuration to the minimal necessary to perform this step. We will augment the Design Settings during the **DayN Provisioning Lab** to include others that may be required.

> [!NOTE]
> While there are newer versions of Postman out there the DCLOUD environment is using an older version which does not restrict the number of users using the application which was added in later versions. As such nomenclature like Tests and images used are here for the older version. Please check Postman for updated documentation when using on production or your own computer.

Before Catalyst Center can automate the deployment we have to do a couple of tasks to prepare. Please log into the Catalyst Center using a browser within the Windows **Jump host**. Use the credentials of username: **`admin`** password: **`C1sco12345`**. Then browse to [Catalyst Center](https://198.18.129.100). Use the credentials of username: **`admin`** password: **`C1sco12345`** within the DCLOUD environment.

Although you can manually set up the hierarchy we will use automation scripts built to implement the hierarchy via **postman** which will utilize the **Catalyst Center API's** To do this we will make use of the application `postman` in the Windows workstation and install json files.

1. Download the following two files by right clicking and opening each in a new tab to download them to the downloads folder on the workstation:

   <p><a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POSTMAN/lab-1-wired-auto-postman-collection.json">⬇︎COLLECTION⬇︎</a></p>
   <p><a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POSTMAN/lab-1-wired-auto-postman-environment.json">⬇︎ENVIRONMENT⬇︎</a></p>

2. Extract both files to the desktop using **Winrar** to expand them
3. Open the **postman** application from the desktop. Once the application is open click the *Import* link.

   ![json](./images/Postman-Pre-Collection-Import.png?raw=true "Import JSON")

4. A popup import window should appear. Ensure File is selected and click the Upload Files button. Select the downloads folder and select both files named:

   - `lab-1-wired-auto-postman-collection.json`
   - `lab-1-wired-auto-postman-environment.json`

   Click open to import them both into Postman

   ![json](./images/Postman-Collection-Select.png?raw=true "Import JSON")

5. When the files are selected and ready for import a window will appear, click Import to complete the import process.

   ![json](./images/Postman-Collection-Selected.png?raw=true "Import JSON")

6. Then click import and the collection should be loaded into the collections as shown.

   ![json](./images/Postman-Post-Collection-Import.png?raw=true "Import JSON")

7. Then click import and the environment should be loaded into the environments as shown.

   ![json](./images/Postman-Post-Environment-Import.png?raw=true "Import JSON")

### Step 2 - Select Postman Environment **(REQUIRED)** 

1. We will select the environment by hovering over the environment shown and selecting the three dots which appear and from that clicking **`Set Active`** as shown.

   ![json](./images/Postman-Environment-Selection.png?raw=true "Import JSON")

### Step 3 - Prepare Postman SSL Settings

1. Click the **Gear** icon to select **settings** 

    ![json](./images/Postman-Settings.png?raw=true "Import JSON")

2. **Deselect** `SSL certificate verification` and then close the settings window. 

    ![json](./images/Postman-SSL-Deselect.png?raw=true "Import JSON")

## Section 2 - Catalyst Center Design Preparation

The **Hierarchy** within Catalyst Center will be used to roll out code and configurations ongoing so my guidance around this is to closely align this to the change management system. If you need change management down to floors or even Intermediate/Main Distribution Facilities then its a good idea to build your hierarchy to suit this. 

**Network Settings** can then be added hierarchically being either inherited and or overidden at each level throughout the hierarchy. The following is a description of the Network Settings and configurations that we will push as part of this lab **(required)**

   1. **DHCP Servers**
   2. **DNS Servers**
   3. **SYSLOG Servers**
   4. **SNMP Servers**
   5. **Netflow Collector Servers** 
   6. **NTP Servers**
   7. **Timezone**

**Device Credentials** can also be added hierarchically being either inherited and or overidden at each level throughout the hierarchy. The following is a description of the credentials and configurations that can be pushed **(required)**:

   1. **CLI Credentials** 
   2. **SNMP Read and Write Credentials**

The collection previously imported along with the ennvironment variables will push all the required design criteria for the Hierarchy, Settings, and Credentials. For more information regarding REST API, please checkout the other labs on REST API within the lab section.

### Step 1 - Deploy Design Hierarchy, Settings and Credentials **(REQUIRED)** 

1. Within **postman** click **`Collections`** and hover over the right side of the collection **`Catalyst Center - Wired Automation Design`** click the Elipsis **`...`** to display a menu. Select **Run collection**. 

   ![json](./images/Postman-Run-Collection-Begin.png?raw=true "Import JSON")

2. Ensure the all the requests are selected and click the blue **`Run Catalyst Center - Wired Automation Design`** button.

   ![json](./images/Postman-Run-Collection-Start.png?raw=true "Import JSON")

3. A summary of all the request steps run will appear and a green pass lamp beside those that were successful as shown.    

   ![json](./images/Postman-Run-Collection-Summary.png?raw=true "Import JSON")

### Step 2 - Verify Design Hierarchy, Settings and Credentials **(REQUIRED)** 

1. Then open a browser and log back into Catalyst Center and navigate the hamburger menu **`Design > Network Hierarchy`** as shown. You will see the hierarchy has been built within Catalyst Center under the Global Site.

   ![json](./images/Verify_Hierarchy.gif?raw=true "Import JSON")

2. Then on the side of Global click the Elipsis **`...`** to display a menu. Select **View Settings**. You will be taken to the **`Network`** page where you will see the various settings for the hierarchy. Click **`Device Credentials`** to see the credentials and **`Telemetry`** to view the telemetry settings set.

   ![json](./images/Verify_Settings.gif?raw=true "Import JSON")

### Step 3 - Image Repository (DO NOT DO IN DCLOUD)

If using DCLOUD lab images should not be modified. In that case please ignore this task.

<details closed>
<summary> Image Repository Steps for NON DCLOUD ONLY </summary></br>

The image used in this lab for the **9300** is downloadable from here [⬇︎Cupertino-17.9.4a MD⬇︎](https://software.cisco.com/download/home/286315874/type/282046477/release/Cupertino-17.9.4a) 

> [!NOTE]
> The process outlined in the pictures uses an older image but the steps remain the same. You should use an image that is marked as MD or **Assurwave** for best results.

1. Within Catalyst Center Navigate to *Design>Image Repository*  

   ![json](./images/DNAC-NavigateImageRepo.png?raw=true "Import JSON")

2. **Image Repository** should be populated with the image of the network device you wish to deploy. You can import the image using the **Import** link which will open a popup allowing you to choose a file from the local file system, or allow you to reference a URL for either HTTP or FTP transfer.    

   ![json](./images/DNAC-ImportImageRepo.png?raw=true "Import JSON")

3. You then indicate whether the file is Cisco or 3rd Party and click import. 
4. The file will then import into Catalyst Center.    

   ![json](./images/DNAC-ImportedImageRepo.png?raw=true "Import JSON")

5. Once the file is imported if there is no instance of the device on the system you can go into the imported images section and assign it to a specific type of device. First click the **Assign** link as shown

   ![json](./images/DNAC-AssignImageRepo.png?raw=true "Import JSON")

   1. Then on the windo that appears select the **All Device Series** dropdown, and then select *switches and hubs* and filter for the **9300** and click assign.   

      ![json](./images/DNAC-AssignSiteImageRepo.png?raw=true "Import JSON")

   2. Next expand the hierarchy on the window that appears and select **Floor1** then **Assign**.    

      ![json](./images/DNAC-SiteImageRepo.png?raw=true "Import JSON")

   3. You will then have a save button to save the assignment. Click Save.    

      ![json](./images/DNAC-SaveImageRepo.png?raw=true "Import JSON")

   4. Your screen should look as shown.    

      ![json](./images/DNAC-DeviceAssigned-ImageRepo.png?raw=true "Import JSON")

6. Select the image and mark it as golden for PnP to use it.   
   ![json](./images/DNAC-GoldenImageRepo.png?raw=true "Import JSON")

</details>

## Section 3 - Catalyst Center Onboarding Template 

You can create onboarding templates within the **Template Hub** previously known as **Template Editor** within **Catalyst Center**. Go to the **Template Hub**  to complete the next task.

The Onboarding template has the minimal configuration and is designed to bring up device connectivity with Catalyst Center. Below are Velocity and Jinja2 examples for explanation purposes only. 

### Example Velocity Template

```vtl
## <------Onboarding-Template------->
## To be used for onboarding when using Day N Templates
## Define Variables provision with vlan and port channel
!
##MTU Adjust (if required)
#if(${SystemMTU} != 1500)
    system mtu ${SystemMTU}
#end
!
##Set hostname
hostname ${Hostname}
!
#set(${VtpDomain} = ${Hostname})
!
##Set VTP and VLAN for onboarding
vtp domain ${VtpDomain}
vtp mode transparent
!
##Set Management VLAN
vlan ${MgmtVlan}
!
#if(${MgmtVlan} > 1)
  name MgmtVlan
  ## Disable Vlan 1 (optional)
  interface Vlan 1
   shutdown
#end

##Set Interfaces and Build Port Channel 
interface range ${Interfaces}
 shut
 switchport mode trunk
 switchport trunk allowed vlan ${MgmtVlan}
 #set($pc = $Interfaces.split(','))
 #if($pc.size() > 1)
   channel-protocol lacp
   channel-group ${PortChannel} mode active
 #end
 no shut
!
#if($pc.size() > 1)
  interface port-channel ${PortChannel}
   switchport trunk native vlan ${MgmtVlan}
   switchport trunk allowed vlan add ${MgmtVlan}
   switchport mode trunk
   no port-channel standalone-disable
#end
!
##Set up managment vlan ${MgmtVlan}
interface Vlan ${MgmtVlan}
 description MgmtVlan
 ip address ${SwitchIP} ${SubnetMask}
 no ip redirects
 no ip proxy-arp
 no shut
!
ip default-gateway ${Gateway}
!
##Set Source of Management Traffic
ip domain lookup source-interface Vlan ${MgmtVlan}
ip http client source-interface Vlan ${MgmtVlan}
ip ftp source-interface Vlan ${MgmtVlan}
ip tftp source-interface Vlan ${MgmtVlan}
ip ssh source-interface Vlan ${MgmtVlan}
ip radius source-interface Vlan ${MgmtVlan}
logging source-interface Vlan ${MgmtVlan}
snmp-server trap-source Vlan ${MgmtVlan}
ntp source Vlan ${MgmtVlan}
!
netconf-yang
!
```

### Example Jinja2 Template

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

Both of these Templates have the settings necessary to bring up a Layer2 access switch with enough configration to be supported by Catalyst Center for the rest of the provisioning process. As guidance it is recommended that you use **Jinja2** moving forward, due to its modularity and capabilities. You can however achieve the same results with **Velocity**, but the scripting language is not as feature rich.

The onboarding template is designed to set up static addressing and a hostname entry along with updating the management source interfaces for management connectivity. This file is transfered to the target device in a single file as opposed to linne by line configuration which accomodates the changes in network connectivity which may be lost when iterating line by line.

Please note the modifications to the source addressing for all protocols and specifically the **HTTP Client** source interface. This helps Catalyst Center to know if or when the IP address changes for a device and update it in the inventory automatically.

### Step 1 - Install an Onboarding Template **(REQUIRED)**

We will now **download** and **import** one of the following PnP Onboarding Templates and install into the **Template Hub** previously known as the **Template Editor**. Please choose and download one from the following:

#### Velocity:

<!---
> [!NOTE]
> For older versions of Catalyst Center formerly known as Cisco DNA Center 2.2 and lower use the following for easy import:
--->
&emsp;&emsp;&emsp; <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/VELOCITY/ONBOARDING/JSON/Platinum_PnP_Velocity_Template.json">⬇︎Platinum_PnP_Velocity_template.json⬇︎</a></br>

<!---
<details closed>
<summary> New Version for NON DCLOUD ONLY </summary></br>
<a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/VELOCITY/ONBOARDING/JSON/Titanium_PnP_Velocity_template.json">⬇︎Titanium_PnP_Velocity_template.json⬇︎</a> 
</details>
--->

#### Jinja2:

<!---
> [!NOTE]
> For older versions of Catalyst Center formerly known as Cisco DNA Center 2.2 and lower use the following for easy import:
--->
&emsp;&emsp;&emsp; <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/ONBOARDING/JSON/Platinum_PnP_Jinja2_Template.json">⬇︎Platinum_PnP_Jinja2_template.json⬇︎</a> 

<!---
<details closed>
<summary> New Version for NON DCLOUD ONLY </summary></br>
<a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/ONBOARDING/JSON/Titanium_PnP_Jinja2_template.json">⬇︎Titanium_PnP_Jinja2_template.json⬇︎</a>
</details></br>
--->

1. Navigate to the **Template Hub** formerly known as the **Template Editor** within Catalyst Center through the menu **`Tools > Template Hub`**.

   ![json](./images/DNAC-NavigateTemplate.png?raw=true "Import JSON")

2. Click **Import** then select **Template(s)** from the menu.    

   ![json](./images/DNAC-TemplateImport-1.png?raw=true "Import JSON")

3. Click the link to select files from the local computer. In the Windows explorer window search for the extracted json file, select it and open it into the import window.

   ![json](./images/DNAC-TemplateSelection-1.png?raw=true "Import JSON")

4. Click import to install and import the template.

   ![json](./images/DNAC-TemplatedSelected-1.png?raw=true "Import JSON")

### Step 2 - Create a Network Profile **(REQUIRED)**

Next we need to assign the Onboarding Template to a site using the Network Profile. 

   1. Navigate to Network Profiles by selecting *Design> Network Profiles* 

      ![json](./images/DNAC-NavigateProfile.png?raw=true "Import JSON")

   2. Select *Switching* under **Add Profile**

      ![json](./images/DNAC-SelectProfile.png?raw=true "Import JSON")

   3. Enter the following: 

      1. Enter the **Profile name** 
      2. Select the **Onboarding Template** tab and click **Add Template** to add a template

         ![json](./images/DNAC-Onboard-Add.png?raw=true "Import JSON")

      3. Select the correct PnP Onboarding template that you imported earlier and click **Add**   

         ![json](./images/DNAC-ChoosePnPTemplate.png?raw=true "Import JSON") 

   4. On the Onboarding Template page confirm the template(s) to be used for onboarding then **Save** the profile

      ![json](./images/DNAC-ProfileComplete.png?raw=true "Import JSON")

   5. Assign the network profile to the hierarchy 

      ![json](./images/DNAC-ProfileAssign.png?raw=true "Import JSON")

   6. Select the sites to apply the profile within the hierarchy and click **Save**.

      ![json](./images/DNAC-ProfileAssigned.png?raw=true "Import JSON")

## Section 4 - PnP Claim and Onboarding Device

At this point Catalyst Center is set up and ready for Plug and Play to onboard the first device. Provided the discovery and dhcp assignment are aligned, the device should when plugged in find Catalyst Center and land in the plug n play set of the devices section within the provisioning page.

### Step 1 - Claiming the Device **(REQUIRED)**

At this point you can claim the device putting it in a planned state for onboarding onto the system. To do this do the following:

   1. Within Catalyst Center Navigate to **`Provision > Plug and Play`**      

      ![json](./images/DNAC-NavigatePnP.png?raw=true "Import JSON")

   2. Put a checkmark next to the device *Switch* to be claimed
   3. Click the **Actions>Claim** link and walk through the workflow    

      ![json](./images/DNAC-BeginClaim.png?raw=true "Import JSON")

   4. Section 1 click the **Assign** link to select the part of the hierarchy to assign the device

      ![json](./images/DNAC-AssignSite-Start.png?raw=true "Import JSON")

   5. Click the part of the hierarchy to assign the device to and then click **Assign**
   
      ![json](./images/DNAC-AssignSite-Save.png?raw=true "Import JSON")

   6. The assigned site will appear on the section page, click **next** to continue

   7. Section 2 you can click the hyperlinks to the right of the workflow page and view or amend the templates and images utilized. We will make no changes so click **next** to continue   

      ![json](./images/DNAC-SiteClaim.png?raw=true "Import JSON")

   8. Section 3 select the device **serial number** on the left and fill in the variables within the template click **next**. Please use the following:
   
      * Hostname type `c9300-1`
      * Management Vlan enter `5`
      * Interfaces `Gi1/0/10, Gi1/0/11`
      * IP Management Address `192.168.5.3`
      * Subnet Mask `255.255.255.0`
      * Gateway `192.168.5.1`
      * VTP Domain `Cisco` ***(if required)***

      > [!NOTE] 
      > Leave the rest of the settings default 

        ![json](./images/DNAC-TemplateClaim.png?raw=true "Import JSON")

   9. Section 4 review the elements including configuration to be deployed. Click **claim** to initiate

      ![json](./images/DNAC-Claim.png?raw=true "Import JSON")

   10. At this stage the device will be placed in **Planned** state, and will cycle through **Onboarding** and **Provisioned** when complete     

       ![json](./images/DNAC-Claimed.png?raw=true "Import JSON")

   11. After the device is completed it will appear in the device inventory after being sync'd with Catalyst Center.      

       ![json](./images/DNAC-Inventory.png?raw=true "Import JSON")

### Step 2 - Post PnP Onboarding - **(OPTIONAL)**

To complete this exercise, the port where the Target switch connects is a layer two trunk as part of a Port Channel got a tweak to the configuration lets discuss. The default behaviour which we have built into the scripts allows for Individual mode to be used in case one port in the Port Channel Bundle is down. This ensure the Bundling and unbundling of ports does not entirely take down connectivity. The cli entry ``` no port-channel standalone-disable ``` is a **default** setting on a port channel which can be seen when using the show run all command. 

This accomplishes **two** things, it places the **upstream** switch negotiating LACP in **Passive** mode **against** an **Active downstream peer** allowing for a correct LACP bonded Port-Channel when used, and **simultaniously** allows for **Individual mode** and **Passive mode** during **PnP** to make sure both ports are configured correctly on the downstream switch. Any other combination results in one port being in the port-channel and that happens unpredicatbly.

### Automating Claiming and Provisioning

While it is possible to click through the claiming and process, for bulk deployments its important to be able to address that as well. With Catalyst Center after the templates are built and assigned to the network profile and assigned to a site they may be referenced and used by uploading a csv file to Catalyst Center via REST API.

## Section 5 - Catalyst Center Device Discovery 

We will now discover the other devices on the network and import them into the Inventory for additional configurations to be applied. We do this with Brownfield equipment to initially put this into Catalyst Center, so that we can begin to automate it over time.

### Step 1 - Create an Discovery Task

To create a Discovery task complete the following actions:

1. Navigate to the Discovery Tool **`Tools > Discovery`**

   ![json](./images/DNAC-Tools-Discovery.png?raw=true "Import JSON")

2. On the Discovery Portal click **Add Discovery**

   ![json](./images/DNAC-DiscoveryPortal.png?raw=true "Import JSON")

3. On the **New Discovery** page complete the following:

   1. Enter the **Discovery Name** (use hierarchy)
   2. Select **IP Address/Range** and enter the following ranges:
      * `192.168.5.1 - 192.168.5.1`
      * `198.18.133.145 - 198.18.133.145`
   3. Click **Next**

      ![json](./images/DNAC-Discovery-1.png?raw=true "Import JSON")

   4. Select the **CLI** and then select the tick box for `netadmin` which should already appear from the **Settings**

      ![json](./images/DNAC-Discovery-2a.png?raw=true "Import JSON")

   5. Select the **SNMPv2c Read** and then select the tick box for `RO` which should already appear from the **Settings**

      ![json](./images/DNAC-Discovery-2b.png?raw=true "Import JSON")

   6. Select the **SNMPv2c Write** and then select the tick box for `RW` which should already appear from the **Settings**

      ![json](./images/DNAC-Discovery-2c.png?raw=true "Import JSON")
      
   7. Select the **NETCONF** then **Add NETCONF Port** and select `Global` from the menu

      ![json](./images/DNAC-Discovery-2d.png?raw=true "Import JSON")
      
   8. Enter `NETCONF` as the description and the port as `830` then click **Next**

      ![json](./images/DNAC-Discovery-2e.png?raw=true "Import JSON")
      
   9. Click **Next** to accept the given Protocols and Timers

      ![json](./images/DNAC-Discovery-2f.png?raw=true "Import JSON")
      
   10. Select **Assign Device to Site** and navigate the hierarchy and select the `Floor 1` then click **Next**

       ![json](./images/DNAC-Discovery-2g.png?raw=true "Import JSON")

   11. Click **Next** to begin the schedule the discovery for **Now**

       ![json](./images/DNAC-Discovery-2h.png?raw=true "Import JSON")

4. Click **Start Discovery and Telemetry** to initiate the discovery task.

   ![json](./images/DNAC-Discovery-3.png?raw=true "Import JSON")

### Step 2 - Verify the Discovery Completed

1. Select **View Discovery** to Exit the Discovery Workflow tool

   ![json](./images/DNAC-Discovery-ExitWorkflow.png?raw=true "Import JSON")

1. Select the `WIRED` discovery within the Discovery Portal to view the results

   ![json](./images/DNAC-DiscoveryPortal-3.png?raw=true "Import JSON")

1. View the results

   ![json](./images/DNAC-Discovery-Verify.png?raw=true "Import JSON")

2. Navigate to the Inventory to see the discovered devices **`Provision > Inventory`**

   ![json](./images/DNAC-NavigateInventory2.png?raw=true "Import JSON")

3. Notice the additional Brownfield devices learned through the discovery process

   ![json](./images/DNAC-Discovery-Done.png?raw=true "Import JSON")

## Summary

The next step will be to build DayN Templates for the switches to be pushed out to the various devices in the network infrastructure.

## Acknowledgments

Thanks to Chanii Haley for taking on the task of creating Jinja 2 templates for use as an option in this lab. If there is any feedback or you as a reader wish to contribute in any way to help this community please reach out on the feedback form. 

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Day N Provisioning Lab**](./module3-dayn.md)

> [**Return to LAB Menu**](./README.md)
