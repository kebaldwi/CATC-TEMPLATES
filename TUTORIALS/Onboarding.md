# Onboarding Templates and Flows [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

In this section will go through the flow involved in creating a Template from an IOS configuration script for a Catalyst switch and various thoughts around how to link it to a Switch profile and deploy it through Catalyst Center using Plug and Play workflows.

Catalyst Center can be used for not only Plug and Play but also Day N or Ongoing Templates. Typically customers will start by building out an Onboarding Template which might deploy only enough information to bring the device up initially or it might include the entire configuration typical for a traditional networking device.

Of note is that Onboarding templates are deployed one time only when the device is being brought online. While there is nothing wrong in doing only this, its important to understand that there is a lot more power gained by being able to modify templates and redeploy them or parts of them for ongoing changes and modifications. For ongoing modifications Day N templates should be considered for those parts of device configuration that undergo routine changes. Additionally, keeping your onboarding configuration lightweight means that you gain the maximum flexibility of being able to make ongoing changes later.

Another important consideration is that part of a typical configuration would include some lines of code which will be built out with the *Design >Network Settings >* application within Catalyst Center. If the Design component of Catalyst Center is used you should not deploy additional CLI code to the device from that point on to avoid conflicting statements between Design component generated code and manual CLI supplied via a template. Its a decision you have to make upfront and avoids a lot of lines in the templates. 

As a guidance try and use Design settings for as much of the configurations as you can, leaving Templates light and nimble for ongoing changes.

## Considerations about Templates

* PnP vs. DayN Templates: Cisco recommends using DayN Templates for most configurations, reserving PnP templates for establishing a stable network connection.

* Inventory Database Limitations: The inventory database is inaccessible before the claim process, complicating onboarding. This results in a need for manual input in scripts instead of leveraging known device information.

* Ongoing Modifications: DayN operations templates are stored within a project, while onboarding templates are located in the project Onboarding Configuration. Using onboarding templates post-PnP is impractical due to the absence of **system** and **bind** variables, which could simplify code and reduce repetition.

* Automation Potential: DayN templates facilitate ongoing modifications and automate configurations using data from the inventory database, minimizing manual input.

* Mandatory configuration is deployed by Catalyst Center during the PnP Onboarding process and it is impossible to disable currently. This facilitates the need to perhaps make modifications post PnP. Configuration seen below:

   <details closed>
   <summary> Expand to review the complete configuration</summary></br>
   
   This is configuration that is automated by default from Catalyst Center claim process. This config that is **deployed automatically**.</br>

   ```
   archive
    log config
     logging enable
     logging size 500
     hidekeys
     !
    !
   !
   service timestamps debug datetime msec
   service timestamps log datetime msec
   service password-encryption
   service sequence-numbers
   !
   ! Disable external HTTP(S) access
   ! Disable external Telnet access
   ! Enable external SSHv2 access
   !
   no ip http server
   !
   no ip http secure-server
   !
   crypto key generate rsa label dnac-sda modulus 2048
   ip ssh version 2
   !
   ip scp server enable
   !
   line vty 0 15
    ! maybe redundant
   login xxxxxx
    transport input ssh
    ! maybe redundant
    transport preferred none
   !
   ! Set VTP mode to transparent (no auto VLAN propagation)
   ! Set STP mode to Rapid PVST+ (prefer for non-Fabric compatibility)
   ! Enable extended STP system ID
   ! Set Fabric Node to be STP Root for all local VLANs
   ! Enable STP Root Guard to prevent non-Fabric nodes from becoming Root
   ! Confirm whether vtp mode transparent below is needed
   vtp mode transparent
   !
   spanning-tree mode rapid-pvst
   !
   spanning-tree extend system-id
   ! spanning-tree bridge priority 0
   ! spanning-tree rootguard
   ! spanning-tree portfast bpduguard default
   no udld enable
   !
   errdisable recovery cause all
   !
   errdisable recovery interval 300
   !
   ! Enable SNMP and RW access
   !
   snmp-server xxxxxxxx
   !
   username xxxxxx
   !
   enable algorithm-type scrypt secret xxxxxxxx
   !
   hostname Switch
   ! DNS settings
   !
   ip domain name base2hq.com
   !
   ip name-server 10.10.0.250
   !
   ```
   </details>

* Due to the nature of PnP onboarding, and as the device is not yet in the system database, **compliance** is not tracked for any template used in the PnP onboarding process. For this reason **ONLY** do enough to bring up the switch. All other configuration should be done in DayN

* Configuration Best Practices: Typical configurations should automatically derive from the Network Settings in Catalyst Center. Avoid deploying CLI code in templates for tasks already defined by design components, promoting a more UI-centric and maintainable configuration approach.

* Guidance: Utilize design settings for as much configuration as possible, keeping templates streamlined for configurations that may change frequently, enhancing maintainability and troubleshooting.

* **Jinja** vs **Velocity**, choose wisely. My recommendation is to use Jinja simply because it is the defacto template rendering language used in multiple platforms. It is modular, and the logic constructs are based on **Python**. 

## Catalyst Center Design Preparation

Before Catalyst Center can automate the deployment we have to complete a few tasks in preparation:

1. The **Hierarchy** within Catalyst Center. This will be used to roll out code and configurations continuously, so my guidance around this is to closely align this to the change management process. If you need change management scoped to floors or even Intermediate/Main Distribution Facilities then its a good idea to build your hierarchy to suit this. There are plenty of blogs and guides about how to do this. Good place to start is [Design the Network Hierarchy](https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center/2-3-3/user_guide/b_cisco_dna_center_ug_2_3_3/m_design-the-network-hierarchy.html). **(required)**
2. **Network Settings** can then be added hierarchically - either inherited and/or overidden at each subordinate level throughout the site hierarchy. The following is a description of the Network Settings and configurations that can be applied **(optional)**:
   1. **AAA Servers** - *both Network Administration and Client/Endpoint Authentication*
   2. **DHCP Servers** - *DHCP Server Addresses for Vlan Interfaces for example*
   3. **DNS Servers** - *both the Domain Suffix and the DNS servers used for lookups*
   4. **SYSLOG Servers** - *the servers to which logging will be sent*
   5. **SNMP Servers** - *the servers to which SNMP traps will be sent and or that will poll the device*
   6. **Netflow Collector Servers** - *the server to which Netflow is sent*
   7. **NTP Servers** - *NTP Server Addresses*
   8. **Timezone** - *Timezone to be used in logging*
   9. **Message of Day** - *Banner displayed when you log into a device*

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/DesignSettings.png?raw=true "Import JSON")

3. **Device Credentials** can then be added hierarchically being either inherited and or overidden at each subordinate level throughout the site hierarchy. The following is a description of the credentials and configurations that can be applied **(required)**:
   1. **CLI Credentials** - *Usernames, Passwords and Enable Passwords*
   2. **SNMP Credentials** - *SNMP v1, v2 for both Read and Write as well as SNMP v3*
   3. **HTTP(S) Credentials** - *HTTP(S) usernames and passwords for both Read and Write Access*
4. **Image Repository** should be populated with the image of the network device you wish to deploy. You can import the image using the **+Import** link which will open a popup allowing you to choose a file from the local file system, or allow you to reference a URL for either HTTP or FTP transfer. You then indicate whether the file is Cisco or 3rd Party image and click import. Once the file is imported, you can go into the imported images section and assign it to a specific type of device. Select the image and mark it as golden for PnP to use it. **(required)**

![json](../ASSETS/TUTORIALS/DAY0DAYN/imported_images.png?raw=true "Import JSON")

## Onboarding Templates

Onboarding templates are regular templates which serve the purpose of onboarding the device as mentioned with the minimal amount of code necessary to get connectivity up to the device in a consistent manner and to allow for further configuration via DayN templates, and device provisioning. Typically, there are two types of configurations that are used here: Layer3 routed, or Layer2 access. Both have different use cases, and while they are typical, they are by no means the only types of configuration used in this context. Onbaording Templates make use of [**Regular Templates**](#regular-templates) which make use of a specific scripting language.

### Regular Templates 

The use of regular templates allows you to reuse build code in the form of a set of IOS commands listed out very much like a configuration file. Those commands may be nested within logical constructs using either Velocity or Jinja2 scripting language, but the intent is that this regular template is a set of instructions initiated on a target device to create a configuration. Here we may introduce Variables, Conditional Logic and Looping constructs to address the delivery of conficguration. 

#### **Jinja2 Scripting Language** 

Catalyst Center allows for the use of Jinja2 Scripting Language which bares some resembelance to Python. It uses similar Variable, Conditional Logic and Looping constructs as Python and allows for developers who use Python to make an easy quick transition to utilizing this form of scripting language. Additionally, Jinja2 incorporates **include** and **extend** functionality which Velocity 1.7.5 does not have implemented within Catalyst Center. This allows for better modularization and reuse of code, in addition to the Composite Template approach.

**Examples:**

   - [Onboarding Template Examples](../CODE/TEMPLATES/JINJA2/ONBOARDING/)

#### **Velocity Scripting Language**

Catalyst Center allows for the use of Velocity Scripting Language which was previously used in Prime Infrastruture. It uses typical Variable, Conditional Logic and Looping constructs and allows for not only developers but also network engineers who may not have experience with programming languages to make an easy quick transition to utilizing this form of scripting language. Modularization and reuse of code, can be supported with the use of Composite Templates.

**Examples:**

   - [Onboarding Template Examples](../CODE/TEMPLATES/VELOCITY/ONBOARDING/)

### Example Template

To that end, a set of examples has been provided in the [**Jinja2**](#jinja2-scripting-language) and [**Velocity**](#velocity-scripting-language) folders above. One of those examples is the one I most typically see used with customer deployments. Included there is a [⬇︎Full Catalyst Center PnP Onboarding Template⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/ONBOARDING/DNAC-SAMPLE-TEMPLATES-01302023-PnP-template.json) for import into Catalyst Center.

#### Example Velocity Template

```vtl
##<------Onboarding-Template------->
##To be used for onboarding when using Day N Templates
##Define Variables provision with vlan and port channel
!
##MTU Adjust (if required)
##system mtu 9100
!
##Set hostname
hostname ${Hostname}
!
##Set VTP and VLAN for onboarding
vtp domain ${VtpDomain}
vtp mode transparent
!
vlan ${MgmtVlan}
!
##Set Interfaces and Build Port Channel 
interface range gi 1/0/10-11
 shut 
 switchport trunk allowed vlan add ${MgmtVlan}
 channel-protocol lacp
 channel-group 1 mode passive
 no shut
!
interface Port-channel1
 switchport trunk native vlan ${MgmtVlan}
 switchport mode trunk
 no port-channel standalone-disable
!
##Set Up Managment Vlan ${MgmtVlan}
interface Vlan ${MgmtVlan}
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
##Disable Vlan 1
interface Vlan 1
 shutdown
!
```

#### Example Jinja2 Template
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
 {% if "," in Interfaces %}
    channel-protocol lacp
    channel-group {{ Portchannel }} mode active
 {% endif %}
 no shut
!
{% if "," in Interfaces %}
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
```
[//]: # ({% endraw %})

Both of these Templates have the settings necessary to bring up a Layer2 access switch with enough configration to be supported by Catalyst Center for the rest of the provisioning process.

## Onboarding Template Deployment

Once you have built your onboarding template you then have to let **Catalyst Center** know where you want it to apply it. We will assume at this point you have already created/imported the above template. You would then follow the following steps:
   1. Create network profile Under *Design> Network Profiles* you will select **+Add Profile**

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/NetworkProfile.png?raw=true "Import JSON")

   2. Select the type of device (ie Switching)
   3. Profile name

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/NetworkProfileTabs.png?raw=true "Import JSON")

   4. On the Onboarding Template page select device type **(required)**

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/OnboardingDevice.png?raw=true "Import JSON")

   5. On the Onboarding Template page select the template(s) to be used for onboarding **(required)**

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/OnboardingTemplate.png?raw=true "Import JSON")

   6. On the DayN Template page select device type **(optional)** (for more info [DayN Templates](./DayN.md))

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/DayNtemplates.png?raw=true "Import JSON")

   7. On the DayN Template page select the template(s) to be used for Day N provisioning **(optional)** (for more info [DayN Templates](./DayN.md))
   8. Save the network profile
   9. Assign the network profile to the site hierarchy element

If the Network Profile is already deployed it can be edited at a later date to add Onboarding templates by following these steps:
   1. Click edit next to the network profile Under *Design> Network Profiles*  
   2. On the Onboarding Template page select device type **(required)**

      ![json](../ASSETS/TUTORIALS/DAY0DAYN/DayNtemplates.png?raw=true "Import JSON")

   3. On the Onboarding Template page select the template(s) to be used for onboarding **(required)**
   4. Save the network profile
   5. Assign the network profile to the hierarchy

> [!CAUTION] 
> If you populate the Catalyst Center Design section, those parameters should **not** be in your templates CLI payload as they will conflict and device provisioning will fail. While it is easy to populate these settings it is best to test with a switch to see what resultant CLI configuration statements are pushed.

## Claiming and Provisioning

At this point Catalyst Center is set up and ready for Plug and Play to onboard the first device. Provided Catalyst Center discovery methods are properly configured (ie DHCP-based, or DNS record-based), the out-of-box device during boot up process discover Catalyst Center, and register itself in the plug n play section of the provisioning page.

At this point you can claim the device putting it in a planned state for onboarding onto the system. To do this do the following:

   1. Put a checkmark next to the device to be claimed
   2. Click the Claim link and walk through the workflow
   3. Section 1 select the part of the hierarchy to which the device will be deployed then click next
   4. Section 2 you can click the device hyperlink and view or amend the template and image utilized then click next
   5. Section 3 you can manipulate any of the variables within the template if used then click next
   6. Section 4 review the elements including configuration to be deployed 
   7. Click claim to initiate
   
At this stage the device will be placed in **Planned** state, and will cycle through **Onboarding** and **Provisioned** when complete. After the device is completed it will appear in the device inventory after being sync'd with Catalyst Center.

![json](../ASSETS/TUTORIALS/DAY0DAYN/pnp-registered.png?raw=true "Import JSON")

## Automating Claiming and Provisioning

While it is possible to click through the claiming and process, for bulk deployments its important to be able to automate this process as well. With Catalyst Center after the templates are built and assigned to the network profile and assigned to a site, they may be referenced and used by uploading a csv file to Catalyst Center via REST API.

This methodology allows for you to specify variables within the csv, serial numbers, and put devices into a planned state waiting for them to land on the Plug and Play page on Catalyst Center.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](../README.md)