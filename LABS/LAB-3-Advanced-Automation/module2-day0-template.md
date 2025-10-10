# Building PnP Templates

## Overview

This module is designed to be used after first completing the **[Lab Preparation](../LAB-3-Advanced-Automation/module1-prep.md)** and has been created to address how to build **Plug and Play (PnP)** to onboard devices into Catalyst Center. 

### Greenfield

When dealing with net **new** devices using the PnP process to onboard devices we utilize **Onboarding templates** within Catalyst Center to onboard network devices with no configuration on the device. 

**PnP** Onboarding allows for the **claiming** of a device and the ability to automate the deployment of configuration. It is important to note that Onboarding templates are transfered as a **flat file** via HTTP/HTTPS transfer. 

This allows for the manipulation of uplinks and addressing without disconnection during reconfiguration from the upstream neighboring device. Additional source commands can be used to allow the device to automatically inform Catalyst Center of a change in address through the PnP profile applied and the source of the HTTP client information.

### Overview Summary

In this section will go through the flows involved with **PnP** only. **Brownfield** will be **out of scope** for this module. This will allow us to create successful onboarding of network devices into Catalyst Center for Greenfield situations.

This is the lab we will be utilizing. Notice the **PnP Target Switch**. This is the C9300-1, which is a variant of the 9300 family. We will be building a configuration for this device from a sample configuration.

![json](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_PnPLab2.png?raw=true "Import JSON")

## Lab Credentials:

| Platform:       | IP Address:    | Username |  Password  | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| Router          | 198.18.133.145 | netadmin | C1sco12345 |
| Switch 1        | 198.18.128.22  | netadmin | C1sco12345 |
| Switch 2        | 198.18.128.23  | netadmin | C1sco12345 |

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

## Developing a PnP Template

So what should be in the PnP Template? Well that depends on the situation, but generally speaking we need to build the foundation of the device, and put that which cannot change without disrupting the communication from Device to Catalyst Center.

### Included items:

* System Configuration
  * Hostname
  * System MTU 
  * VTP 
  * Enable Netconf 
* Management Interface Configuration
  * IP address
  * Subnet Mask
  * Source Management Traffic
* Next Hop Configuration
  * Gateway or Routing Protocol

## Exercises

### Step 1 - Navigate to Template Hub

Navigate to the CLI Template Hub on Catalyst Center **`Tools > Template Hub`**

![json](../../ASSETS/LABS/CATC/MENU/catc-menu-5.png?raw=true "Import JSON")

### Step 2 - Create a Regular Template

Within the **Project Name** Section on the left locate the **Onboarding Configuration** Project and select it as shown

![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/project-onboarding-default.png?raw=true "Import JSON")

You will notice there is not much in there. What we will do is now Build our first template. To do this use the **&#8853; Add** action menu shown and select **New Template**

![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-start.png?raw=true "Import JSON")

In the **Add New Template** wizard fill in the following details as shown below:

|Section          |Details                                |
|-----------------|---------------------------------------|
|Template Name    |**PnP-Template-J2**                    |
|Project Name     |**Onboarding Configuration**           |
|Template Type    |**Regular Template**                   |
|Template Language|**JINJA**                              |
|Software Type    |**IOS-XE**                             |
|Device Family    |**Switches and Hubs**                  |
|Devices          |**Cisco Catalyst 9300 Series Switches**|

1. First enter the Template Name **PnP-Template-J2** from above then select the Onboarding Configuration project. This must be selected for this template to be offered within the PnP Onboarding Tab of the Network Profile.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-1.png?raw=true "Import JSON")

2. Ensure that for Template Type you have selected **Regular Template** and under Template Language that **JINJA** is selected as recommended earlier. For Software Type select **IOS-XE** as shown.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-2.png?raw=true "Import JSON")

3. Click the **Add Device Details** link to select the type of device to which to associate the template

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-3.png?raw=true "Import JSON")

4. In the **Add Device Details** page select for Device Family **Switches and Hubs**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-4.png?raw=true "Import JSON")

5. Enter **9300** in the search filter to find the 9300 switches

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-5.png?raw=true "Import JSON")

6. Then select for Devices **Cisco Catalyst 9300 Series Switches** and click **Add**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-6.png?raw=true "Import JSON")

7. You should now see the following **configured properties** for the template, click **Continue**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-7.png?raw=true "Import JSON")

8. The **PnP-Template-J2** will now open in the Editor allowing the configuration to be added.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/add-pnp-template-8.png?raw=true "Import JSON")

### Step 3 - Build the Template Logic

As previously stated the PnP Template should use the minimum configuration to adhere to the **Don't Repeat yourself (DRY)** philosophy. Remember No System Variables and limited bind functionality are available. This inhibits the ability to use logic without filling in all the details. Additionally we really want to track these things which is what DayN affords us. 

> [!TIP]
> As you go through this lab do not merely paste the configs, challenge yourself to understand what is going on with the logic in the template and how it was derived. </br></br> Additionally, Always Keep it **SIMPLE**

In this lab we are connecting a Layer 2 switch and utilizing the typical management VLAN. So at a minimum we need to get this configuration onto that device:

|Detail            |Configuration       |
|------------------|--------------------|
|Hostname          |`c9300-1`           |
|Management Vlan   |`5`                 |
|Uplink Interfaces |`Gi1/0/10, Gi1/0/11`|
|Management Address|`192.168.5.3`       |
|Subnet Mask       |`255.255.255.0`     |
|Gateway           |`192.168.5.1`       |
|VTP Domain        |`Cisco`             |

#### Basic Template

1. So in order to get this configuration on the switch we would typically configure something like this:

   ```j2
   hostname c9300-1
   !
   vlan 5
    name mgmtvlan
   !
   interface vlan 5
    ip address 192.168.5.3 255.255.255.0
    no shutdown
    exit
   !
   interface vlan 1
    shutdown
   ! 
   ip default-gateway 192.168.5.1
   !
   interface range gigabitethernet1/0/10-11
    switchport mode trunk
    switchport trunk allowed vlan 5
    channel-protocol lacp
    channel-group 1 mode active
    no shut
   !
   interface port-channel 1
    switchport trunk native vlan 5
    switchport trunk allowed vlan 5
    switchport mode trunk
    no port-channel standalone-disable
   !
   ```

2. So lets copy and paste that confiiguration into the **PnP-Template-J2**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-1.png?raw=true "Import JSON")

### Step 4 - Use Variables

Now we will adhere to the **DRY** philosophy because in our organization we want to use this template not just once but thousands of times in different locations. So we will modify the template to include **VARIABLES** and **LOGIC** to make it **reusable**.

These variables will be utilized with a form so that they can be mass entered via a comma separated value CSV file during the claiming process. 

1. Lets create the following variables by highlighting the detail replacing it with {{variable}} as shown in the table and in the image below:

   |Configuration       |Detail            |
   |--------------------|------------------|
   |c9300-1             |`{{Hostname}}`    |
   |5                   |`{{MgmtVlan}}`    |
   |Gi1/0/10, Gi1/0/11  |`{{Interfaces}}`  |
   |192.168.5.3         |`{{SwitchIP}}`    |
   |255.255.255.0       |`{{SubnetMask}}`  |
   |192.168.5.1         |`{{Gateway}}`     |

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-2.png?raw=true "Import JSON")

2. Now lets add some logic to make the interfaces more reusable. When we use the interface range command we can use various situational delimiters. The following are allowed:

   - Single Interface (ie: interface range `gi1/0/1`)
   - Comma Delimited List (ie: interface range `gi1/0/1, gi1/0/2`)
   - Dashes for From To (ie: interface range `gi1/0/1-2`)

   So how does this impact us, well we will need to make some logic to allow for the portchannel to be optional and for the logic to allow for the additional commands in the event they are needed. What if we want this to have a single uplink to a router in a small branch. 

   Lets incorporate that by modifying the interface section syntax to read:

   [//]: # ({% raw %})
   ```
   interface range {{Interfaces}}
    shut
    switchport mode trunk
    switchport trunk allowed vlan {{MgmtVlan}}
    {% if "," in Interfaces || "-" in Interfaces %}
       channel-protocol lacp
       channel-group 1 mode active
    {% endif %}
    no shut
   ```
   [//]: # ({% endraw %})

   The additional logic includes a conditional statement looking for the **`,` or `-`** operators and automatically adds the LACP commands adhering the interfaces to the port-channel interface if required.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-3.png?raw=true "Import JSON")

3. Lets now follow suit and allow for any Port-Channel interface number to be used by variablizing the Port-Channel numbering as shown:
  
   [//]: # ({% raw %})
   ```
   interface range {{Interfaces}}
    shut
    switchport mode trunk
    switchport trunk allowed vlan {{MgmtVlan}}
    {% if "," in Interfaces || "-" in Interfaces %}
       channel-protocol lacp
       channel-group {{Portchannel}} mode active
    {% endif %}
    no shut
   !
   {% if "," in Interfaces || "-" in Interfaces %}
     interface Port-channel {{Portchannel}}
      switchport trunk native vlan {{MgmtVlan}}
      switchport trunk allowed vlan {{MgmtVlan}}
      switchport mode trunk
      no port-channel standalone-disable
   {% endif %}
   ```
   [//]: # ({% endraw %})

   The additional logic includes a conditional statement looking for the **`,` or `-`** operators and automatically adds the Port-Channel configuring the **optional** port-channel interface if required. Notice that we additionally **added** a **variable** for the **number** of the **Port-Channel**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-4.png?raw=true "Import JSON")

4. Now lets make some further modifications to allow be a bit more pragmatic with the Vlan creation. First we will introduce a stabilizing element and set the **VTP configuration**, because most don't like VTP mode to be anything but **transparent** mode. 

   [//]: # ({% raw %})
   - Now you can manually set the VTP Domain to anything or remove the `{% set VtpDomain = Hostname %}` line to allow for it to be part of the entry fields if you desire. Within this Lab we will let it be the hostname and dynamically created.
   [//]: # ({% endraw %})

   - After the set command we will set the **vtp domain** and apply **transparent mode**.

   - Once we set the Management Vlan we introduce logic to optionally name the Vlan. If the Management Vlan were set to 1 then the name is default and may not be modified. Additionally Vlan 1 would not need to be shutdown. However if we utilize any other Vlan for management then we allow the naming of the Vlan within the Vlan database and automatically shutdown the SVI for Vlan 1.

     [//]: # ({% raw %})
     ```
     {% set VtpDomain = Hostname %}
     vtp domain {{VtpDomain}}
     vtp mode transparent
     !
     vlan {{MgmtVlan}}
     !
     {% if MgmtVlan > 1 %}
       name MgmtVlan
       interface Vlan 1
        shutdown
     {% endif %}
     ```
     [//]: # ({% endraw %})
   
   You will notice there were a few modifications on this iteration. This iterative approach allows us to test at each stage and or ensure that we think the entire process through ensuring maximum reusability.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-5.png?raw=true "Import JSON")

5. Finally lets add additional logic to ensure the success of the template in these sections:

   1. When building configuration its always wise to set the **System MTU**. The System MTU command is set immediately and does not require a reboot. So lets add that logic This logic should only be necessary if the MTU should be set to anything other than the default.

      [//]: # ({% raw %})
      ```
      {% if SystemMTU != 1500 %}
         system mtu {{SystemMTU}}
      {% endif %}
      ```
      [//]: # ({% endraw %})
    
   2. Lets set the **source interface** for **ALL** the **management traffic** so that its consistent in our management systems. Lets also enable **NETCONF** by default.

      [//]: # ({% raw %})
      ```
      ip domain lookup source-interface Vlan {{MgmtVlan}}
      ip http client source-interface Vlan {{MgmtVlan}}
      ip ftp source-interface Vlan {{MgmtVlan}}
      ip tftp source-interface Vlan {{MgmtVlan}}
      ip ssh source-interface Vlan {{MgmtVlan}}
      ip radius source-interface Vlan {{MgmtVlan}}
      logging source-interface Vlan {{MgmtVlan}}
      snmp-server trap-source Vlan {{MgmtVlan}}
      ntp source Vlan {{MgmtVlan}}
      !
      netconf-yang
      ```
      [//]: # ({% endraw %})

   3. Lets also add to the Vlan interface some protection for source traffic to exlude redirects and proxy arp to ensure the traffic being communicated is from the sources and destinations configured.

      [//]: # ({% raw %})
      ```
      interface Vlan {{ MgmtVlan }}
       description MgmtVlan
       ip address {{ SwitchIP }} {{ SubnetMask }}
       no ip redirects
       no ip proxy-arp
       no shut
      ```
      [//]: # ({% endraw %})

   4. Lastly there is an issue with creating a VARIABLE within logical constructs so I employ a workaround (hack) to allow for this right before the VARIABLE is introduced.
      
      [//]: # ({% raw %})
      ```
      !{{Portchannel}}
      ```
      [//]: # ({% endraw %})

      ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-6.png?raw=true "Import JSON")

6. **Save** the template and we can now start to Build the Form that will be filled in by our engineers during the claim process.
7. If your template **does not look like** the one below **expand the section** below **copy** it and **paste** it into the editor to replace the text:
   
[//]: # ({% raw %})

<details closed>
<summary> Expand this section if required </summary></br>

```
{% if SystemMTU != 1500 %} 
   system mtu {{SystemMTU}}
{% endif %}
!
hostname (Hostname}}
!
{% set VtpDomain = Hostname %} 
vtp domain {{VtpDomain}}
vtp mode transparent
!
vlan {{MgmtVlan}}
!
{% if MgmtVlan > 1 %} 
   name MgmtVlan
   interface Vlan 1 
     shutdown
{% endif %}
!
interface vlan {{MgmtVlan}}
 ip address {{SwitchIP}} {{SubnetMask}}
 no shutdown
 no ip redirects
 no ip proxy-arp exit
 exit
!
ip default-gateway {{Gateway}}
!
!{{Portchannel)}
interface range {{Interfaces)}
 shut
 switchport mode trunk
 switchport trunk allowed vlan {{MgmtVlan}}
 {% if "," in Interfaces || "-" in Interfaces %}
    channel-protocol lacp
    channel-group {{Portchannel}} mode active
 {% endif %}
 no shut
!
{% if "," in Interfaces || in Interfaces %} 
   interface Port-channel ((Portchannel}}
    switchport trunk native vlan {{MgmtVlan}}   
switchport trunk allowed vlan {{MgmtVlan}}   
switchport mode trunk
    no port-channel standalone-disable
{% endif %}
!
ip domain lookup source-interface Vlan {{MgmtVlan}}
ip http client source-interface Vlan {{MgmtVlan}}
ip ftp source-interface Vlan {{MgmtVlan}}
ip tftp source-interface Vlan {{MgmtVlan}}
ip ssh source-interface Vlan {{MgmtVlan}}
ip radius source-interface Vlan {{MgmtVlan}}
logging source-interface Vlan {{MgmtVlan}}
snmp-server trap-source Vlan {{MgmtVlan}}
ntp source Vlan {{MgmtVlan}}
!
netconf-yang
```

</details>

[//]: # ({% endraw %})

### Step 5 - Build Form

Now we will develop the interaction between the logic in the rendering language and the network engineer. The Form is presented to the engineer during the claim process, and so we need to edit the fields to make sure that they are presented in the correct and logical manner. 

1. Click on the **Variables** tab while editing the template. The following is presented. On the left a listing of the variables that the editor has parsed from the logic of the template and on the right a editor space.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-7.png?raw=true "Import JSON")

2. Select the **SystemMTU** variable on the left. Make the following modifications:
   
   - Type `System MTU` for the Field Name to make it more understandable. 
   - This is an optional variable in our logic so **untick** the **required variable** selection
   - Make this a numeric value by selecting **integer** for variable type
   - Enter the Default Variable Value of `1500`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-8.png?raw=true "Import JSON")

3. Select the **Hostname** variable on the left 

   - Enter the Default Variable Value of `c9300-1`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-9.png?raw=true "Import JSON")

4. Select the **MgmtVlan** variable on the left 

   - Type `Management Vlan` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **integer** for variable type
   - Enter the Default Variable Value of `5`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-10.png?raw=true "Import JSON")

5. Select the **SwitchIP** variable on the left 

   - Type `Management IP Address` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **IP Address** for variable type
   - Enter the Default Variable Value of `192.168.5.3`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-11.png?raw=true "Import JSON")

6. Select the **SubnetMask** variable on the left 

   - Type `Management Subnet Mask` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **IP Address** for variable type
   - Enter the Default Variable Value of `255.255.255.0`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-12.png?raw=true "Import JSON")

7. Select the **Gateway** variable on the left 

   - Type `Gateway Address` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **IP Address** for variable type
   - Enter the Default Variable Value of `192.168.5.1`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-13.png?raw=true "Import JSON")

8. Select the **Portchannel** variable on the left 

   - Type `Port-Channel Number` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **Integer** for variable type
   - Enter the Default Variable Value of `1`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-14.png?raw=true "Import JSON")

9. Select the **Interfaces** variable on the left 

   - Type `Uplink Interfaces` for the Field Name to make it more understandable. 
   - Make this a numeric value by selecting **String** for variable type
   - Enter the Default Variable Value of `Gi1/0/10, Gi1/0/11`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-15.png?raw=true "Import JSON")

10. Preview the form by clicking **Review Form** on the bottom right of the page.

    ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-16.png?raw=true "Import JSON")

11. **Save** the template and **Commit** and we can move on to simulation tests to see what it will render.

### Step 6 - Simulation

Now we will simulate the deployment of a device to check our rendered code. 

1. Click on the **Simulation** tab while editing the template. The following is presented. On the left a listing of the variables that the editor has parsed from the logic of the template and on the right a editor space.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-17.png?raw=true "Import JSON")

2. Click on the Create Simulation Button Presented, then fill in the Create Simulation Form and ensure the following is displayed and or chosen:

   |Field Name            |Data                    |
   |----------------------|------------------------|
   |Simulation Name       |`Test`                  |
   |System MTU            |`1500`                  |
   |Hostname              |`c9300-1`               |
   |Management Vlan       |`5`                     |
   |Management IP Address |`192.168.5.3`           |
   |Management Subnet Mask|`255.255.255.0`         |
   |Gateway Address       |`192.168.5.1`           |
   |Port-Channel Number   |`1`                     |
   |Uplink Interfaces     |`Gi1/0/10, Gi1/0/11`    |
   
3. Then click **Save**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-18.png?raw=true "Import JSON")

4. Select the **Test** simulation presented by clicking on the name.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-19.png?raw=true "Import JSON")

5. Select the **Device** `c9300-2.dcloud.cisco.com` and click **Run**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-20.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-21.png?raw=true "Import JSON")

6. Each time you do a test make sure the rendered template makes sense. Try changing the following and re running the simulation for:

   - Vlan number to `1`
   - Port-Channel number to `110`
   - Interfaces and delimiters used to `Gi1/0/10-11`
   - System MTU to `1450`

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-22.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PNPTEMPLATE/basic-pnp-template-23.png?raw=true "Import JSON")

## Summary

Congratulations you have completed the building and testing a PnP Template. Move on to the Claiming module where we will operationalize the template.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to PnP Claiming Module**](../LAB-3-Advanced-Automation/module3-pnp.md)

> [**Return to Lab Menu**](./README.md)