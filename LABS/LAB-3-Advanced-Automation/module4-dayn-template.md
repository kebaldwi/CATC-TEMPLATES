# Building DayN Templates

## Overview

This Module is designed and built to address how to use DayN templates within Catalyst Center to configure network devices at Day 1 through N. This Lab is designed to be used after first completing the previous modules. 

The purpose of DayN templates is to allow for **ongoing configuration** of features on devices beyond those deployed on the Claiming process. With Catalyst Center, if devices are not within a fabric, the host onboarding part of the UI will not be available. To that end, templates are an easy way of deploying those types of configuration and much more. Before starting this Lab, please make sure you have finished all the steps in the previous modules.

## Considerations about Templates

* PnP vs. DayN Templates: Cisco recommends using DayN Templates for most configurations, reserving PnP templates for establishing a stable network connection.

* Inventory Database Limitations: The inventory database is inaccessible before the claim process, complicating onboarding. This results in a need for manual input in scripts instead of leveraging known device information.

* Ongoing Modifications: DayN operations templates are stored within a project, while onboarding templates are located in the project Onboarding Configuration. Using onboarding templates post-PnP is impractical due to the absence of **system** and **bind** variables, which could simplify code and reduce repetition.

* Automation Potential: DayN templates facilitate ongoing modifications and automate configurations using data from the inventory database, minimizing manual input.

* Mandatory configuration is deployed by Catalyst Center during the PnP Onboarding process and it is impossible to disable currently. This facilitates the need to perhaps make modifications post PnP. Configuration seen below:

<div style="padding-left:80px">
   <details open>
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
</div>

* Due to the nature of PnP onboarding, and as the device is not yet in the system database, **compliance** is not tracked for any template used in the PnP onboarding process. For this reason **ONLY** do enough to bring up the switch. All other configuration should be done in DayN

* Configuration Best Practices: Typical configurations should automatically derive from the Network Settings in Catalyst Center. Avoid deploying CLI code in templates for tasks already defined by design components, promoting a more UI-centric and maintainable configuration approach.

* Guidance: Utilize design settings for as much configuration as possible, keeping templates streamlined for configurations that may change frequently, enhancing maintainability and troubleshooting.

* **Jinja** vs **Velocity**, choose wisely. My recommendation is to use Jinja simply because it is the defacto template rendering language used in multiple platforms. It is modular, and the logic constructs are based on **Python**. 

## Developing a DayN Template

So what should be in the DayN Templates? Well that depends on the situation, but generally speaking we need to build the onboarding capability of the device, and put that which cannot change without disrupting the communication from Device to Catalyst Center.

Additionally, while a more extensive set of settings can be built out for deployment, we will limit the configuration to the **minimum** necessary to perform this step, building off the completed tasks in module 2.

You can create Regular Day N Templates using Jinja2 and Velocity scripting languages within the **Template Hub** within **Catalyst Center**. There are two basic types of templates we can utilize. **Regular** templates, as well as **Composite** templates. Use a combiination of these templates to adhere to the **DRY** philosophy.

### Regular Templates

**Regular** templates are templates which are typically designed to address a specific use case. Regular templates are written in either Jinja2 or Velocity scripting languages. Each Language has features which may be leveraged to make the script more reusable, allowing the user to not have to repeat themselves. This modular capability allows us to keep a script written to address a specific need small. At the same time each form of scripting language allows for features like variables, conditional logic, and looping constructs. This allows for a small powerful script to be written making it more light weight and easier to fault find and maintain.

### Composite Templates

**Composite** templates are logical templates used for grouping together multiple **Regular** templates. They allow you to use Jinja2 and Velocity **Regular** templates within the same logical template. This allows us to make templates in mutliple languages and to be able to reuse long standing Velocity scripts with newer Jinja2 templates within the same **Composite** Template. This allows for people to code in the language they are more accustomed too, and to continue to support existing scripts.

### Included items:

* Model Configuration Analysis
* Modularization of Features for Reusability
  * System Configuration
    * Services
    * LLDP Neighbor Protocol 
    * Source-Destination Load Balancing 
    * Spanning Tree
	* Logging
	* Time Configuration 
  * AAA Configuration for Local Device Administration
    * AAA Configuration
	* HTTP Configuration
	* Login Banner Configuration
	* Console, VTY and Netconf Configuration
  * Interface Configuration
    * Vlans
	* Port Channel Configuration
    * Uplink Configurations
    * Host Interface Configurations

## Exercises

This section will go through the build and provisioning of **Composite** and **Regular** templates via Catalyst Center to a Catalyst 9k switch. We will deal with the **Greenfield** scenario only during this module. Remember that a similar approach could be used for **Brownfield**.

### Step 1 - Navigate to Template Hub

Navigate to the CLI Template Hub on Catalyst Center **`Tools > Template Hub`**

![json](../../ASSETS/LABS/CATC/MENU/catc-menu-5.png?raw=true "Import JSON")

### Step 2 - Create a Project

We will create a **Project** for the deployment of these switches within the lab. You may notice that there is a Project which was deployed during the lab preparation module. We will not be utilizing that here, but you could if you desired.

1. What we will do is now Build our first Project. To do this use the **&#8853; Add** action menu shown and select **New Project**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-1.png?raw=true "Import JSON")

2. In the **Add New Project** wizard type in the **`DayN-Templates-J2`** as the project name

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-2.png?raw=true "Import JSON")

3. Select **Composite Sequence** as the **Template Type**. Then select **IOS-XE** from the **Software Type** drop down.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-3.png?raw=true "Import JSON")

4. Click **Add Device Details**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-4.png?raw=true "Import JSON")

5. In the **Add Device Details** page select for Device Family **Switches and Hubs**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-5.png?raw=true "Import JSON")

6. Enter **9300** in the search filter to find the 9300 switches

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-6.png?raw=true "Import JSON")

7. Then select for Devices **Cisco Catalyst 9300 Series Switches** and click **Add**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-7.png?raw=true "Import JSON")

8. You should now see the following **configured properties** for the template, click **Continue**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-8.png?raw=true "Import JSON")

9. The **PnP-Template-J2** will now open in the Editor allowing the configuration to be added.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-9.png?raw=true "Import JSON")

10. You should now see the following **Composite Sequence** created which we will populate later.

    ![json](../../ASSETS/LABS/TEMPLATEEDITOR/PROJECT/add-project-10.png?raw=true "Import JSON")

### Step 3 - Analyze Configuration

Lets now take a look at a sample typical switch configuration from our network. We are going to review this in some detail in the next few sections and build modularized templates. As we do we will disect this configuration showing **how** and **where** specific configuration should be placed for scalability.

<details open>
<summary> Expand to review the complete example configuration</summary>

```
service tcp-keepalives-in
service tcp-keepalives-out
service timestamps debug datetime msec localtime show-timezone
service timestamps log datetime msec show-timezone year
service password-encryption
service sequence-numbers
service call-home
no platform punt-keepalive disable-kernel-core
!
hostname c9300-1
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
 address-family ipv6
 exit-address-family
!
logging buffered 16384 informational
no logging console
aaa new-model
!
aaa group server radius CON-VTY
 server-private 198.18.133.1 key 7 <redacted>
 ip radius source-interface Vlan5
 deadtime 6
!
aaa authentication login default local
aaa authentication login CON-LAB local-case
aaa authorization console
aaa authorization exec default local 
aaa authorization exec CON-LAB local 
aaa authorization network default group dnac-client-radius-group 
aaa accounting network default start-stop group radius
aaa session-id common
!
clock timezone EST -5 0
clock summer-time EDT recurring
switch 1 provision c9300-48u
!
ip routing
!
ip name-server 198.18.133.1
ip domain lookup source-interface Vlan5
ip domain name base2hq.com
!
lldp run
!
vtp domain base2hq.com
vtp mode transparent
vtp version 1
!
port-channel load-balance src-dst-ip
!
spanning-tree mode rapid-pvst
spanning-tree portfast default
spanning-tree portfast bpduguard default
spanning-tree extend system-id
!
enable secret 9 <redacted>
username admin privilege 15 secret 9 <redacted>
!
redundancy
 mode sso
!
vlan 5
 name mgmtvlan
vlan 10
 name apvlan
vlan 20
 name datavlan
vlan 30
 name voicevlan
vlan 40
 name guestvlan
!
interface Port-channel1
 switchport trunk native vlan 5
 switchport trunk allowed vlan 5,10,20,30,40
 switchport mode trunk
!
interface GigabitEthernet0/0
 vrf forwarding Mgmt-vrf
 no ip address
 shutdown
 negotiation auto
!
interface range GigabitEthernet1/0/1-48
 switchport access vlan 20
 switchport voice vlan 30
 spanning-tree portfast
!
interface TenGigabitEthernet1/1/1, TenGigabitEthernet1/1/2 
 switchport trunk allowed vlan 1,5,10,20,30,40
 switchport mode trunk
 channel-group 1 mode active
 channel-protocol lacp 
!
interface Vlan5
 description MgmtVlan
 ip address 192.168.5.3 255.255.255.0
 no ip redirects
 no ip proxy-arp
!
ip forward-protocol nd
ip http server
ip http authentication local
ip http secure-server
ip http secure-trustpoint <redacted>
ip http client source-interface Vlan5
ip ssh source-interface Vlan5
ip ssh version 2
!
ip radius source-interface Vlan5 
logging origin-id ip
logging source-interface Vlan5
logging host 10.10.0.20
logging host 198.18.133.27 transport udp port 20514
!
snmp-server community private RW
snmp-server community public RO
snmp-server trap-source Vlan5
snmp-server enable traps all
snmp-server host 10.10.0.20 version 2c private 
snmp-server host 198.18.133.27 version 2c private 
snmp-server host 10.10.0.20 version 2c public 
snmp-server host 198.18.133.27 version 2c public 
!
radius-server attribute 6 on-for-login-auth
radius-server attribute 6 support-multiple
radius-server attribute 8 include-in-access-req
radius-server attribute 25 access-request include
radius-server attribute 31 mac format ietf upper-case
radius-server attribute 31 send nas-port-detail mac-only
radius-server dead-criteria time 5 tries 3
radius-server retransmit 2
radius-server deadtime 3
!
radius server dnac-radius_198.18.133.27
 address ipv4 198.18.133.27 auth-port 1812 acct-port 1813
 timeout 4
 retransmit 3
 automate-tester username dummy ignore-acct-port probe-on
 pac key 7 <redacted>
!
banner login ^
 ******************************************************************
 * CISCO SYSTEMS EXAMPLE                                          *
 ******************************************************************
 *                                                                *
 * THIS DEVICE IS PART OF A DEMONSTRATION COMPUTER NETWORK AND IS *
 * PROVIDED FOR OFFICIAL USE BY AUTHORIZED USERS ONLY. ANY        *
 * INFORMATION, DOCUMENTS, OR MATERIALS IN THE NETWORK ARE THE    *
 * PROPERTY OF THIS FIRM. UNAUTHORIZED USE, DUPLICATION, OR       *
 * DISCLOSURE OF INFORMATION OR SYSTEMS IN THIS NETWORK IS        *
 * STRICTLY PROHIBITED BY FEDERAL LAW (18 USC 10130). USE OF THIS *
 * NETWORK CONSTITUTES CONSENT TO MONITORING WHICH MAY BE         *
 * RELEASED TO FIRM MANAGEMENT AND/OR LAW ENFORCEMENT AGENCIES    *
 * AND MAY RESULT IN DISCIPLINARY ACTION, CIVIL ACTION, AND/OR    *
 * CRIMINAL OR CIVIL LITIGATION.                                  *
 *                                                                *
 ******************************************************************
   Hostname: $(hostname)
 ******************************************************************
 * CISCO SYSTEMS EXAMPLE *
 ******************************************************************
^
!
line con 0
 exec-timeout 0 0
 privilege level 15
 authorization exec CON-LAB
 logging synchronous
 login authentication CON-LAB
 stopbits 1
line vty 0 31
 exec-timeout 0 0
 authorization exec CON-LAB
 logging synchronous
 login authentication CON-LAB
 terminal-type mon
 length 0
 transport input ssh
!
ntp source Vlan5
ntp server 198.18.133.1
!
end
```

</details>

1. Lets discount any config that is automated by default from Catalyst Center claim process. This config that is **deployed automatically**. Along with this we will discount any configuration which is **default configuration** on the switch as that will already be there. Thus they do not need a place in our template.

   <details open>
   <summary> Expand to review the complete configuration</summary>
   
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

2. Lets also discount any configurations which will be in the **Design** section or have been deployed via the **PnP Claiming Process**. These are the number of lines **REMOVED** at this point.

   <details open>
   <summary> Expand to review the removed configuration</summary>
   
   ```
   service password-encryption
   service sequence-numbers
   service call-home
   no platform punt-keepalive disable-kernel-core
   !
   hostname ASW-9300-ACCESS
   !
   vrf definition Mgmt-vrf
    address-family ipv4
    exit-address-family
    address-family ipv6
    exit-address-family
   !
   switch 1 provision c9300-48u
   !
   ip name-server 198.18.133.1
   ip domain lookup source-interface Vlan5
   ip domain name base2hq.com
   !
   vtp domain base2hq.com
   vtp mode transparent
   vtp version 1
   !
   spanning-tree mode rapid-pvst
   spanning-tree extend system-id
   !
   enable secret 9 <redacted>
   username admin privilege 15 secret 9 <redacted>
   !
   vlan 5
    name mgmtvlan
   !
   interface Port-channel1
    switchport trunk native vlan 5
    switchport trunk allowed vlan 5
    switchport mode trunk
   !
   interface GigabitEthernet0/0
    vrf forwarding Mgmt-vrf
    no ip address
    negotiation auto
   !
   interface TenGigabitEthernet1/1/1, TenGigabitEthernet1/1/2 
    switchport trunk allowed vlan 1,5
    switchport mode trunk
    channel-group 1 mode active
    channel-protocol lacp 
   !
   interface Vlan5
    description MgmtVlan
    ip address 192.168.5.3 255.255.255.0
    no ip redirects
    no ip proxy-arp
   !
   ip ssh source-interface Vlan5
   ip ssh version 2
   !
   ip radius source-interface Vlan5 
   logging source-interface Vlan5
   logging host 10.10.0.20
   logging host 198.18.133.27 transport udp port 20514
   !
   snmp-server community private RW
   snmp-server community public RO
   snmp-server trap-source Vlan5
   snmp-server enable traps all
   snmp-server host 10.10.0.20 version 2c private 
   snmp-server host 198.18.133.27 version 2c private 
   snmp-server host 10.10.0.20 version 2c public 
   snmp-server host 198.18.133.27 version 2c public 
   !
   ntp source Vlan5
   ntp server 198.18.133.1
   !
   end
   ```
   
   </details>

3. The remaining configuration shown here can be modularized to simplify it. Here is what is left which we will use templates to build.

   <details open>
   <summary> Expand to review the complete configuration</summary>
   
   ```
   service tcp-keepalives-in
   service tcp-keepalives-out
   service timestamps debug datetime msec localtime show-timezone
   service timestamps log datetime msec show-timezone year
   !
   logging buffered 16384 informational
   no logging console
   !
   clock timezone EST -5 0
   clock summer-time EDT recurring
   !
   ip routing
   !
   udld enable
   lldp run
   !
   port-channel load-balance src-dst-ip
   !
   spanning-tree portfast default
   spanning-tree portfast bpduguard default
   !
   redundancy
    mode sso
   !
   vlan 5
    name mgmtvlan
   vlan 10
    name apvlan
   vlan 20
    name datavlan
   vlan 30
    name voicevlan
   vlan 40
    name guestvlan
   !
   interface Port-channel1
    switchport trunk allowed vlan 5,10,20,30,40
   !
   interface GigabitEthernet0/0
    shutdown
   !
   interface range GigabitEthernet1/0/1-48
    switchport access vlan 20
    switchport voice vlan 30
    spanning-tree portfast
   !
   interface TenGigabitEthernet1/1/1, TenGigabitEthernet1/1/2 
    switchport trunk allowed vlan 1,5,10,20,30,40
   !
   ip forward-protocol nd
   ip http server
   ip http authentication local
   ip http secure-server
   ip http secure-trustpoint <redacted>
   ip ssh source-interface Vlan5
   ip ssh version 2
   !
   logging origin-id ip
   !
   banner login ^
    ******************************************************************
    * CISCO SYSTEMS EXAMPLE                                          *
    ******************************************************************
    *                                                                *
    * THIS DEVICE IS PART OF A DEMONSTRATION COMPUTER NETWORK AND IS *
    * PROVIDED FOR OFFICIAL USE BY AUTHORIZED USERS ONLY. ANY        *
    * INFORMATION, DOCUMENTS, OR MATERIALS IN THE NETWORK ARE THE    *
    * PROPERTY OF THIS FIRM. UNAUTHORIZED USE, DUPLICATION, OR       *
    * DISCLOSURE OF INFORMATION OR SYSTEMS IN THIS NETWORK IS        *
    * STRICTLY PROHIBITED BY FEDERAL LAW (18 USC 10130). USE OF THIS *
    * NETWORK CONSTITUTES CONSENT TO MONITORING WHICH MAY BE         *
    * RELEASED TO FIRM MANAGEMENT AND/OR LAW ENFORCEMENT AGENCIES    *
    * AND MAY RESULT IN DISCIPLINARY ACTION, CIVIL ACTION, AND/OR    *
    * CRIMINAL OR CIVIL LITIGATION.                                  *
    *                                                                *
    ******************************************************************
      Hostname: $(hostname)
    ******************************************************************
    * CISCO SYSTEMS EXAMPLE *
    ******************************************************************
   ^
   !
   line con 0
    exec-timeout 0 0
    privilege level 15
    logging synchronous
    stopbits 1
   line vty 0 31
    exec-timeout 0 0
    logging synchronous
    terminal-type mon
    length 0
    transport input ssh
   !
   end
   ```
   
   </details>

### Step 4 - Modularize the Configuration

The next step is to modularize the configuration so as to group the various configurations in one place for reusability to adhere to the **DRY** philosophy.

1. As there are some commands that are system based that need to be there and as the default is different than what we need in the end we will make modifications.

   ```
   no service pad
   service tcp-keepalives-in
   service tcp-keepalives-out
   service timestamps debug datetime msec localtime show-timezone
   service timestamps log datetime msec show-timezone
   service password-encryption
   service sequence-numbers
   !
   lldp run
   port-channel load-balance src-dst-ip
   !
   spanning-tree mode rapid-pvst
   spanning-tree portfast default
   spanning-tree portfast bpduguard default
   !
   logging buffered 16384 informational
   no logging console
   logging origin-id ip
   !
   clock timezone EST -5 0
   clock summer-time EDT recurring
   ```

2. As AAA configurations can be deployed via settings, and since we are deploying the client AAA in that manner we will show how you can also at the same time make use of AAA configurations for Device Admin from a template at the same time. Lets group all the Network Admin and AAA configuration together and make some slight modifications.

   ```
   aaa new-model
   aaa authentication username-prompt "Authorized Username: "
   aaa authentication login admin local
   aaa authorization console
   aaa authorization exec admin local
   aaa authentication login admin local-case
   aaa authorization exec admin local 
   !
   ip forward-protocol nd
   no ip http server
   no ip http authentication local
   no ip http secure-server
   ip ssh version 2
   !
   banner login ^
    ******************************************************************
    * CISCO SYSTEMS EXAMPLE                                          *
    ******************************************************************
    *                                                                *
    * THIS DEVICE IS PART OF A DEMONSTRATION COMPUTER NETWORK AND IS *
    * PROVIDED FOR OFFICIAL USE BY AUTHORIZED USERS ONLY. ANY        *
    * INFORMATION, DOCUMENTS, OR MATERIALS IN THE NETWORK ARE THE    *
    * PROPERTY OF THIS FIRM. UNAUTHORIZED USE, DUPLICATION, OR       *
    * DISCLOSURE OF INFORMATION OR SYSTEMS IN THIS NETWORK IS        *
    * STRICTLY PROHIBITED BY FEDERAL LAW (18 USC 10130). USE OF THIS *
    * NETWORK CONSTITUTES CONSENT TO MONITORING WHICH MAY BE         *
    * RELEASED TO FIRM MANAGEMENT AND/OR LAW ENFORCEMENT AGENCIES    *
    * AND MAY RESULT IN DISCIPLINARY ACTION, CIVIL ACTION, AND/OR    *
    * CRIMINAL OR CIVIL LITIGATION.                                  *
    *                                                                *
    ******************************************************************
      Hostname: $(hostname)
    ******************************************************************
    * CISCO SYSTEMS EXAMPLE *
    ******************************************************************
    ^
   !
   netconf-yang
   !
   line con 0
    exec-timeout 15 0
    login authentication admin
    logging synchronous
    authorization exec admin
    stopbits 1
   line vty 0 15
    exec-timeout 15 0
    login authentication admin
    logging synchronous
    authorization exec admin
    transport input ssh
   ```

3. Vlan and interface Configuration needs to be deployed.

   ```
   vlan 5
    name mgmtvlan
   vlan 10
    name apvlan
   vlan 20
    name datavlan
   vlan 30
    name voicevlan
   vlan 40
    name guestvlan
   !
   interface Port-channel1
    switchport trunk allowed vlan 5,10,20,30,40
   !
   interface GigabitEthernet0/0
    shutdown
   !
   interface range GigabitEthernet1/0/1-48
    switchport access vlan 20
    switchport voice vlan 30
    spanning-tree portfast
   !
   interface TenGigabitEthernet1/1/1, TenGigabitEthernet1/1/2 
    switchport trunk allowed vlan 1,5,10,20,30,40
   ```

This pretty much sums up the templates we will need. Now lets start building them in the Template Hub. So we will be making perhaps 3 or four templates based on the configuration snippets we have here.

### Step 5 - Create System Configuration Regular Templates

The next step is to create modularized Jinja templates from the configuration sections so as to continue to group the various configurations in one place for reusability to adhere to the **DRY** philosophy.

1. What we will do is now Build our first DayN Template. To do this use the **&#8853; Add** action menu shown and select **New Template**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-1.png?raw=true "Import JSON")

2. For Template Name select **`DayN-SysConfig-J2`** as shown.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-2.png?raw=true "Import JSON")

3. Ensure that for Template Type you have selected **Regular Template** and under Template Language that **JINJA** is selected as recommended earlier. For Software Type select **IOS-XE** as shown.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-3.png?raw=true "Import JSON")

4. Click the **Add Device Details** link to select the type of device to which to associate the template

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-4.png?raw=true "Import JSON")

5. In the **Add Device Details** page select for Device Family **Switches and Hubs**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-5.png?raw=true "Import JSON")

6. Enter **9300** in the search filter to find the 9300 switches

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-6.png?raw=true "Import JSON")

7. Then select for Devices **Cisco Catalyst 9300 Series Switches** and click **Add**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-7.png?raw=true "Import JSON")

8. You should now see the following **configured properties** for the template, click **Continue**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-8.png?raw=true "Import JSON")

9. The **DayN-SysConfig-J2** template will now open in the Editor allowing the configuration to be added. Take this snippet and add it to the template you just created and **save** and **commit** it.

    [//]: # ({% raw %})
    ```J2
    {#System Configuration#}
    no service pad
    service tcp-keepalives-in
    service tcp-keepalives-out
    service timestamps debug datetime msec localtime show-timezone
    service timestamps log datetime msec show-timezone
    service password-encryption
    service sequence-numbers
    !
    lldp run
    port-channel load-balance src-dst-ip
    !
    spanning-tree mode rapid-pvst
    spanning-tree portfast default
    spanning-tree portfast bpduguard default
    !
    logging buffered 16384 informational
    no logging console
    logging origin-id ip
    !
    clock timezone EST -5 0
    clock summer-time EDT recurring
    ```
    [//]: # ({% endraw %})

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/SysConfig/add-dayn-template-9.png?raw=true "Import JSON")

### Step 6 - Create AAA Configuration Regular Templates

In the continuation of the creation of modularized Jinja templates we will clone the **DayN-SysConfig-J2** template and then modify the configuration sections so as to continue to group the various configurations in regular templates for reusability and adhere to the **DRY** philosophy. This speeds up the template creation process reducing the number of clicks.

1. What we will do is **Clone** our first **DayN-SysConfig-J2** template. To do this click the **&#8230;** entry action menu shown and select **Clone**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/AaaConfig/add-dayn-template-1.png?raw=true "Import JSON")

2. Replace the Template Name with **`DayN-AaaConfig-J2`** as shown and then click **Clone**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/AaaConfig/add-dayn-template-2.png?raw=true "Import JSON")

3. The new **DayN-AaaConfig-J2** template will now be as shown. Click on the template name **DayN-AaaConfig-J2** to **edit** it.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/AaaConfig/add-dayn-template-3.png?raw=true "Import JSON")

4. The **DayN-AaaConfig-J2** template will now open in the Editor allowing the configuration to be added. Take this snippet and add it to the template you just created and **save** and **commit** it.

    [//]: # ({% raw %})
    ```J2
    {#AAA Configuration#}
    aaa new-model
    aaa authentication username-prompt "Authorized Username: "
    aaa authentication login admin local
    aaa authorization console
    aaa authorization exec admin local
    aaa authentication login admin local-case
    aaa authorization exec admin local 
    !
    ip forward-protocol nd
    no ip http server
    no ip http authentication local
    no ip http secure-server
    ip ssh version 2
    !
    <MLTCMD>
    banner login ^
     ******************************************************************
     * CISCO SYSTEMS EXAMPLE                                          *
     ******************************************************************
     *                                                                *
     * THIS DEVICE IS PART OF A DEMONSTRATION COMPUTER NETWORK AND IS *
     * PROVIDED FOR OFFICIAL USE BY AUTHORIZED USERS ONLY. ANY        *
     * INFORMATION, DOCUMENTS, OR MATERIALS IN THE NETWORK ARE THE    *
     * PROPERTY OF THIS FIRM. UNAUTHORIZED USE, DUPLICATION, OR       *
     * DISCLOSURE OF INFORMATION OR SYSTEMS IN THIS NETWORK IS        *
     * STRICTLY PROHIBITED BY FEDERAL LAW (18 USC 10130). USE OF THIS *
     * NETWORK CONSTITUTES CONSENT TO MONITORING WHICH MAY BE         *
     * RELEASED TO FIRM MANAGEMENT AND/OR LAW ENFORCEMENT AGENCIES    *
     * AND MAY RESULT IN DISCIPLINARY ACTION, CIVIL ACTION, AND/OR    *
     * CRIMINAL OR CIVIL LITIGATION.                                  *
     *                                                                *
     ******************************************************************
       Hostname: $(hostname)
     ******************************************************************
     * CISCO SYSTEMS EXAMPLE *
     ******************************************************************
     ^
    </MLTCMD>
    !
    netconf-yang
    !
    line con 0
     exec-timeout 15 0
     login authentication admin
     logging synchronous
     authorization exec admin
     stopbits 1
    line vty 0 15
     exec-timeout 15 0
     login authentication admin
     logging synchronous
     authorization exec admin
     transport input ssh
    ```
    [//]: # ({% endraw %})

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/AaaConfig/add-dayn-template-4.png?raw=true "Import JSON")

### Step 7 - Create Interface Configuration Regular Templates

In the continuation of the creation of modularized Jinja templates we will clone the **DayN-SysConfig-J2** template and then modify the configuration sections so as to continue to group the various configurations in regular templates for reusability and adhere to the **DRY** philosophy. This speeds up the template creation process reducing the number of clicks.

1. What we will do is **Clone** our first **DayN-SysConfig-J2** template. To do this click the **&#8230;** entry action menu shown and select **Clone**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/IntConfig/add-dayn-template-1.png?raw=true "Import JSON")

2. Replace the Template Name with **`DayN-IntConfig-J2`** as shown and then click **Clone**.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/IntConfig/add-dayn-template-2.png?raw=true "Import JSON")

3. The new **DayN-IntConfig-J2** template will now be as shown. Click on the template name **DayN-IntConfig-J2** to **edit** it.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/IntConfig/add-dayn-template-3.png?raw=true "Import JSON")

4. The **DayN-IntConfig-J2** template will now open in the Editor allowing the configuration to be added. Take this snippet and add it to the template you just created and **save** and **commit** it.

    [//]: # ({% raw %})
    ```J2
    {#Interface Configuration#}
    !
    {#Vlan Build#}
    {#Vlan Dictionary#}
    {% set VlanData = [
      {'vlan':'5','name':'mgmtvlan'},
      {'vlan':'10','name':'apvlan'},
      {'vlan':'20','name':'datavlan'},
      {'vlan':'30','name':'voicevlan'},
      {'vlan':'40','name':'guestvlan'},
      {'vlan':'999','name':'disabledvlan'}
      ]%}
    !
    {#MACRO Vlan Database Build#}
    {% macro configure_vlans(vlanpairs)  %}
      {% for vlanpair in vlanpairs %}
        vlan {{vlanpair['vlan']}}
        name {{vlanpair['name']}}
      {% endfor %}
    {% endmacro %}
    !
    {# MACRO Vlan Search Function #}
    {% macro search_vlans(vlanpairs) %}
      {% for vlanpair in vlanpairs %}
        {% do vlanArray.append(vlanpair['vlan']) %}
      {% endfor %}
    {% endmacro %}
    !
    {#Macro for Workstation Interface#}
    {# Interface Workstations with Voice Macro #}
    {% macro workstation_interface(vlan_number, voice_number) %}
      description Workstation Interface
      switchport access vlan {{vlan_number}}
      switchport voice vlan {{voice_number}}
      switchport mode access
    {% endmacro %}
    !
    {#Vlan Configuration#}
    {% set vlanArray = [] %}
    {{ configure_vlans(VlanData) }}
    {{ search_vlans(VlanData) }}
    !
    {#Interface Configuration#}
    {#Update PortChannel with Vlans#}
    interface Port-channel 1
     switchport trunk allowed vlan add {{vlanArray|join(',')}}
    !
    {#Management Shutdown#}
    interface GigabitEthernet0/0
     shutdown
    !
    {#Determine Uplinks Target#}
    {% set portarray = [] %}
    {% for interface in __interface %}
      {% if interface.portMode == "trunk" && interface.interfaceType == "Physical" %}
        {% do portarray.append(interface.portName) %}
      {% endif %}
    {% endfor %}
    !
    {#Automatically Configure Workstation non uplink interfaces#}
    {% for interface in __interface %}
      {% if interface.interfaceType == "Physical" && interface.portName.replaceAll("(^[a-zA-Z]+).*","$1") ==     "GigabitEthernet"  %}
        {% if interface.portName.replaceAll("(^[a-zA-Z]+.).*", "$1") != "GigabitEthernet0" %}
          {% if interface.portName.replaceAll("^[a-zA-Z]+(\\d+)/(\\d+)/(\\d+)", "$2") != 1 %}
            {% if interface.portName in portarray %}
            {% else %}
              default interface {{interface.portName}}
              interface {{interface.portName}}
                {{workstation_interface(vlanArray[1],vlanArray[2])}}
            {% endif %}
          {% endif %}
        {% endif %}
      {% endif %}
    {% endfor %}
    ```
    [//]: # ({% endraw %})

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/IntConfig/add-dayn-template-4.png?raw=true "Import JSON")

### Step 8 - Configure Composite Template

Now we will configure the **DayN-Templates-J2** composite template. This allows us to logically group any DayN templates that exist in the project or the system with a network profile for deployment. Lets get started. 

1. Within the Template Hub click on the **DayN-Templates-J2** composite template

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-1.png?raw=true "Import JSON")

2. Within the composite template **DayN-Templates-J2** click on **Add Templates**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-2.png?raw=true "Import JSON")

3. Add a filter of **`DayN`** in the search field to filter in on the DayN templates we have just built.

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-3.png?raw=true "Import JSON")

4. Click the **+** icon beside each template or **drag** them to add them as in the image below

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-4.png?raw=true "Import JSON")

5. Remove the filter of **`DayN`** in the search field and click the **+** icon beside **AutoNaming-EEM-Scripting** to add it as in the image below 

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-5.png?raw=true "Import JSON")

6. When the templates match the image below, click **Done**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-6.png?raw=true "Import JSON")

7. Now we need to reorder the templates to ensure they occur in the right order for switches. Click **Reorder**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-7.png?raw=true "Import JSON")

8. You will see the various templates but not in the correct order. We will reorder the templates by **clicking** and **holding** and **dragging** them into the correct order as shown in the **before** and **after**. Finally click **Done** when complete.

   #### Before
   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-8.png?raw=true "Import JSON")
   #### After
   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-9.png?raw=true "Import JSON")

9. Finally click **Save** and **Commit**

   ![json](../../ASSETS/LABS/TEMPLATEEDITOR/DAYNTEMPLATE/Composite/mod-dayn-composite-10.png?raw=true "Import JSON")

## Summary

Congratulations you have completed the process of creating a DayN Project with Composite and Regular Templates. In the next module we will deploy the templates to the switch. There are plenty of Tutorials and additional examples available in this repository please take the time to understand all that is possible.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to DayN Provisioning Module**](../LAB-3-Advanced-Automation/module5-dayn.md)

> [**Return to Lab Menu**](./README.md)