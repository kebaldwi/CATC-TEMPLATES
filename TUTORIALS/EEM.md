# EEM - Embedded Event Manager [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

Embedded Event Manager is a Flexible and Powerful tool in Cisco IOS & IOS-XE Software which allows a switch to automate actions based on user enabled system events. Events trigger the execution of user defined set of actions. Triggers can come in many forms from Syslog through to Timers as depicted in the following slide. 

![json](../ASSETS/TUTORIALS/EEM/EEMDetectors.png?raw=true "Import JSON")

Actions can be then taken by the device utilizing cli commands through to TCL or Python Scripts. This section will start to dive into various capabilities and use cases for EEM scripts which can be deployed on Cisco Catalyst Products.

![json](../ASSETS/TUTORIALS/EEM/EEMOperation.png?raw=true "Import JSON")

## Capabilities and Uses

EEM can be used to:
1. Automate operational activities done manually
2. Change the behavior of Catalyst Switch or Cisco Router
   1. Customize switch or router behavior
   2. Automatically apply workarounds ( aka Fix bugs)
   3. Change configuration dynamically
3. Notify network admin on event for example send email on temperature, cpu or memory threshold crossing

The configuration of EEM will be examined in the following use cases along with the capabilities. From a configuration point of view

## Case 1 - ***Renaming Interfaces - Use Case***

Previously within the Composite Templating Lab, we introduced a methodology of automatically naming the interfaces within the switch. When a new device or switch/router/access point connects to a switch, we want to describe those interfaces. Naming the uplinks specifically and the various wireless access points and IP Phones would be an excellent addition. 

### ***Examine Code***

The script we used on the Composite Templates uses an EEM script that runs whenever a CDP event occurs.

```vtl
   event manager applet update-port
    event neighbor-discovery interface regexp GigabitEthernet.* cdp add
    action 101 regexp "(Switch|Router)" "$_nd_cdp_capabilities_string"
    action 102 if $_regexp_result eq "1"
    action 103  cli command "enable"
    action 104  cli command "config t"
    action 105  cli command "interface $_nd_local_intf_name"
    action 106  regexp "^([^\.]+)\." "$_nd_cdp_entry_name" match host
    action 107  regexp "^([^\.]+)" "$_nd_port_id" match connectedport
    action 108  cli command "no description"
    action 109  cli command "description Uplink to $host - $connectedport"
    action 110  cli command "interface port-channel 1"
    action 111  cli command "no description"
    action 112  cli command "description Uplink to $host"
    action 113  cli command "end"
    action 114  cli command "write"
    action 115 end
```

While this script will rename the uplinks connected to a Router or Switch, it is limited in terms of the following:
1. Timing, as it's not scheduled, and you cannot clear the CDP table from the template
2. Naming Access Points or other devices is also not taken into consideration

### ***Modify Code***

So let's modify the EEM script first to solve the naming aspect concerning connected devices with **CDP**.

```vtl
event manager applet update-port-cdp authorization bypass
 event neighbor-discovery interface regexp GigabitEthernet.* cdp add
 action 100 regexp "(Switch|Router|Trans-Bridge|Phone)" "$_nd_cdp_capabilities_string"
 action 110 if $_regexp_result eq "1"
 action 111  regexp "(Switch|Router)" "$_nd_cdp_capabilities_string"
 action 112  set cdp_switch $_regexp_result
 action 113  regexp "(Trans-Bridge)" "$_nd_cdp_capabilities_string"
 action 114  set cdp_wireless $_regexp_result
 action 115  regexp "(Phone)" "$_nd_cdp_capabilities_string"
 action 116  set cdp_phone $_regexp_result
 action 120  if $cdp_wireless eq "1"
 action 121   cli command "enable"
 action 122   cli command "config t"
 action 123   cli command "interface $_nd_local_intf_name"
 action 124   regexp "^([^.]+)" "$_nd_cdp_entry_name" match host
 action 125   regexp "^([^.]+)" "$_nd_port_id" match connectedport
 action 126   cli command "no description"
 action 127   cli command "description AP - $host - $connectedport"
 action 128   cli command "end"
 action 130  elseif $cdp_phone eq "1"
 action 131   cli command "enable"
 action 132   cli command "config t"
 action 133   cli command "interface $_nd_local_intf_name"
 action 134   regexp "^([^.]+)" "$_nd_cdp_entry_name" match host
 action 135   regexp "^([^.]+)" "$_nd_port_id" match connectedport
 action 136   cli command "no description"
 action 137   cli command "description Phone - $host - $connectedport"
 action 138   cli command "end"
 action 140  elseif $cdp_switch eq "1"
 action 141   cli command "enable"
 action 142   cli command "config t"
 action 143   cli command "interface $_nd_local_intf_name"
 action 144   regexp "^([^.]+)." "$_nd_cdp_entry_name" match host
 action 145   regexp "^(..).*([0-9]\/[0-9]\/[0-9]+)" "$_nd_port_id" match Type Port
 action 146   cli command "no description"
 action 147   cli command "description Link - $host - $Type$Port"
 action 148   cli command "do show running-config interface $_nd_local_intf_name | include channel-group"
 action 149   regexp "channel-group ([0-9]+)" "$_cli_result" match portchannel
 action 150   if $_regexp_result eq "1"
 action 151    cli command "interface port-channel $portchannel"
 action 152    cli command "no description"
 action 153    cli command "description Link - $host"
 action 154   end
 action 155   cli command "end"
 action 160  else
 action 161   cli command "enable"
 action 162   cli command "config t"
 action 163   cli command "interface $_nd_local_intf_name"
 action 164   regexp "^([^.]+)." "$_nd_cdp_entry_name" match host
 action 165   regexp "^(..).*([0-9]\/[0-9]\/[0-9]+)" "$_nd_port_id" match Type Port
 action 166   cli command "no description"
 action 167   cli command "description Link - $host - $Type$Port"
 action 168   cli command "end"
 action 170  end
 action 180 end
 action 200 cli command "write mem" 
 ```

First, let's address the primary problem, the naming of interfaces with descriptions.

You will see that lines *201 to 220* were added to the EEM script. We look for the keyword `Trans-Bridge` within the built-in variable to determine if the port is connected to an Access Point within that section. It results in a True or binary 1 state, and the included code from lines *211 to 220* runs line by line. The configuration adds a description to the interface for the phone of `description AP - KO-AP0C75 - GigabitEthernet0`, for example.

You will see that lines *250 to 260* were added to the EEM script. We look for the keyword `Phone` within the built-in variable to determine if the port is connected to a Phone within that section. It results in a True or binary 1 state, and the included code from lines *253 to 260* runs line by line. For example, the configuration adds a description to the interface for the phone of `description Phone - SEPB07D47D34910 - Port 1`.

In case you are interested in **LLDP** take a look at this.

```vtl
event manager applet update-port-lldp authorization bypass
 event neighbor-discovery interface regexp GigabitEthernet.* lldp add
  action 101 regexp "(B|R|W|T)" "$_nd_lldp_system_capabilities_string"
  action 110 if $_regexp_result eq "1"
  action 111  regexp "(B|R)" "$_nd_lldp_system_capabilities_string"
  action 112  set lldp_switch $_regexp_result
  action 113  regexp "(W)" "$_nd_lldp_system_capabilities_string"
  action 114  set lldp_wireless $_regexp_result
  action 115  regexp "(T)" "$_nd_lldp_system_capabilities_string"
  action 116  set lldp_phone $_regexp_result
  action 120  if $lldp_wireless eq "1"
  action 121   cli command "enable"
  action 122   cli command "config t"
  action 123   cli command "interface $_nd_local_intf_name"
  action 124   regexp "^([^\.]+)" "$_nd_lldp_system_name" match host
  action 125   regexp "^([^\.]+)" "$_nd_lldp_port_description" match connectedport
  action 126   cli command "no description"
  action 127   cli command "description AP - $host - $connectedport"
  action 128   cli command "end"
  action 130  elseif $lldp_phone eq "1"
  action 131   cli command "enable"
  action 132   cli command "config t"
  action 133   cli command "interface $_nd_local_intf_name"
  action 134   regexp "^([^\.]+)" "$_nd_lldp_system_name" match host
  action 135   regexp ":\s*P([0-9]+)" "$_nd_port_id" match connectedport
  action 136   cli command "no description"
  action 137   cli command "description Phone - $host - Port $connectedport"
  action 138   cli command "end"
  action 140  elseif $lldp_switch eq "1"
  action 141   cli command "enable"
  action 142   cli command "config t"
  action 143   cli command "interface $_nd_local_intf_name"
  action 144   regexp "^([^\.]+)\." "$_nd_lldp_system_name" match host
  action 145   regexp "^([^\.]+)" "$_nd_port_id" match connectedport
  action 146   cli command "no description"
  action 147   cli command "description Link - $host - $connectedport"
  action 148   cli command "do show running-config interface $_nd_lldp_system_name | include channel-group"
  action 149   regexp "channel-group ([0-9]+)" "$_cli_result" match portchannel
  action 150   if $_regexp_result eq "1"
  action 151    cli command "interface port-channel $portchannel"
  action 152    cli command "no description"
  action 153    cli command "description Link - $host"
  action 154   end
  action 155   cli command "end"
  action 160  else
  action 161   cli command "enable"
  action 162   cli command "config t"
  action 163   cli command "interface $_nd_local_intf_name"
  action 164   regexp "^([^\.]+)\." "$_nd_lldp_system_name" match host
  action 165   regexp "^([^\.]+)" "$_nd_port_id" match connectedport
  action 166   cli command "no description"
  action 167   cli command "description Link - $host - $connectedport"
  action 168   cli command "end"
  action 170  end
  action 180 end
  action 200 cli command "write mem" 
```

## Case 2 - ***Sending a IOS-XE command to clear a table - Use Case***

The second part of the problem within this use case is solving the issue presented by a lack of functionality when the code is configured on the switch. While we can get the configuration in place, it will only run when the port is cycled or when the CDP information for the port is cleared. Therefore, to solve the problem, we employ a *Self-Destructing EEM script*.

*Self-Destructing EEM scripts* are those that delete themselves on termination. Within the code below, you will notice that line 2.1 removes the EEM applet from the configuration, and then line 2.3 ensures the configuration is written to NVRAM before terminating.

```vtl
   event manager applet POST_PNP
    event timer countdown time 30
    action 1.0 cli command "enable"
    action 1.1 cli command "clear cdp table"
    action 2.0 cli command "config t"
    action 2.1 cli command "no event manager applet POST_PNP"
    action 2.2 cli command "end"
    action 2.3 cli command "wr
    action 2.4 cli command "exit
```

This code allows us to *clear the CDP table* and delete itself but leave the other EEM script on the switch for any moves, adds, and changes to the devices connected to the switch.

## Case 3 - ***Dynamic Port Configuration for Low-Impact Mode - Use Case***

To deal with the chicken and the egg scenario, whereby we can't use **Autoconf** with **Closed Mode** as no packets can pass, which can be used with the parameter map to configure the interface automatically. Additionally, we want to have a **Secure Access** environment with **Zero Trust** using a policy on the interface that initially blocks traffic until authentication occurs. 

So how do we have our cake and eat it too...

Luckily we can create a fully dynamic environment with a gated procedure. You might build out the following EEM scripts to give that Dynamic look and feel entirely. Typically, the types of devices where we might have issues like this where *MAB* or *EAP* are not going to work maybe those which identify themselves in another way. In the following instance, we can use **PoE** power events to trigger an EEM. See the following code:

```vtl
event manager applet DETECT_SW_IEEE_POE_UP
 event syslog pattern "%.*POWER.*GRANTED.* Interface.*"
 action 10    regexp "Interface ([^ ]+):" "$_syslog_msg" match intf
 action 20    cli command "enable"
 action 30    cli command "show run interface $intf | inc channel-group mode"
 action 40    regexp "(^channel-group)" "$_cli_result"
 action 50    if $_regexp_result ne "1"
 action 50.10  puts "POE Device Detected. INSTALL LOWIMPACT on Interface $intf"
 action 50.11  cli command "enable"
 action 50.12  cli command "conf t"
 action 50.13  cli command "default interface $intf"
 action 50.14  cli command "interface $intf"
 action 50.15  cli command " description AP CONFIG"
 action 50.16  cli command " switchport access vlan 10"
 action 50.17  cli command " switchport mode access"
 action 50.18  cli command " switchport port-security maximum 3"
 action 50.19  cli command " switchport port-security"
 action 50.20  cli command " device-tracking attach-policy IPDT_POLICY"
 action 50.21  cli command " snmp trap mac-notification change added"
 action 50.22  cli command " snmp trap mac-notification change removed"
 action 50.23  cli command " source template ACCESS_POINT"
 action 50.24  cli command " spanning-tree portfast"
 action 50.25  cli command " spanning-tree bpduguard enable"
 action 80    end
 action 90    cli command "write"
 action 99    cli command "exit"
``` 

## Case 4 - ***Dynamic Port Configuration for Closed Mode - Use Case***

But you may say, we have modified the physical interface configuration, well we can reset that too to the **BASE CONFIG** through another EEM script as follows:

```vtl
event manager applet DETECT_SW_INT_DOWN
 event syslog pattern "%LINK.* Interface.* changed state to .* down"
 action 10    regexp "Interface ([^ ]+)," "$_syslog_msg" match intf
 action 20    cli command "enable"
 action 30    cli command "show run interface $intf | inc channel-group mode"
 action 40    regexp "(^channel-group)" "$_cli_result"
 action 50    if $_regexp_result ne "1"
 action 50.10  puts "AP Trunk Interface DOWN. INSTALL BASECONFIG on Interface $intf"
 action 50.11  cli command "enable"
 action 50.12  cli command "conf t"
 action 50.13  cli command "default interface $intf"
 action 50.14  cli command "interface $intf"
 action 50.15  cli command "access-session inherit disable interface-template-sticky"
 action 50.16  cli command "default interface $intf"
 action 50.17  cli command "interface $intf"
 action 50.18  cli command " description BASE CONFIG"
 action 50.20  cli command " switchport mode access"
 action 50.21  cli command " switchport port-security maximum 3"
 action 50.22  cli command " switchport port-security"
 action 50.23  cli command " device-tracking attach-policy IPDT_POLICY"
 action 50.24  cli command " snmp trap mac-notification change added"
 action 50.25  cli command " snmp trap mac-notification change removed"
 action 50.26  cli command " source template WORKSTATION"
 action 50.27  cli command " spanning-tree portfast"
 action 50.28  cli command " spanning-tree bpduguard enable"
 action 60    else
 action 70     puts "Non-EMM port Interface $intf went down."
 action 80    end
 action 90    cli command "write"
 action 99    cli command "exit"
```

This EEM script makes sure the interface is not a portchannel member and then reverts the interface to the **BASE CONFIG** automatically.

## Case 5 - ***Using Scheduling capability to make changes - Use Case***

For situations where you need to automate a repeated task over a number of days at a specific set of times, you can make use of this type of design. Here we use the built-in scheduling system and tie the EEM script to the time. This script completes port resets at 8:30 am Monday through Friday.

```vtl
event manager applet DAILY-RESET
 event timer cron name DAILY-RESET cron-entry "30 08 * * 1-5"
 action 1.0 syslog msg "RUN: 'DAILY-RESET'  EEM applet."
 action 2.0 puts "DAILY-RESET"
 action 2.1 cli command "enable"
 action 2.2 cli command "config t"
 action 2.3 cli command "int ra gi 1/0/23-24"
 action 2.4 puts "SHUTDOWN"
 action 2.5 cli command "shut"
 action 2.6 puts "NO SHUTDOWN"
 action 2.7 cli command "no shut"
 action 2.8 cli command "exit"
```

Here is an example that does a periodic save of the configuration for compliance reasons.

```vtl
event manager applet PERIODIC-CONFIG-SAVE
 event timer cron name CONFIG-SAVE-TIMER cron-entry "55 23 * * 1-5" action 1.0 cli command "enable"
 action 1.0 cli command "copy running-config startup-config"
```

### Case 6 - ***Collecting Forensics when an event happens - Use Case***

For situations where you need to collect forensics using multiple show commands you can collapse the results of all those appending them to a file on flash and then attach them in the body of an email to be sent off to the companies Network Operations Center. This example helps with those situations.

```vtl
event manager session cli username admin 
event manager applet LINK-EVENT-NOTIFIER
event syslog pattern "%BGP-5-ADJCHANGE: neighbor 10.1.1.10 Down BGP Notification Sent"
action 1.0 cli command "enable"
action 1.5 cli command "term len 0"
action 2.0 cli command "show ip bgp summary | redirect flash:/output.txt"
action 2.5 cli command "show ip int br | ex un | append flash:/output.txt"
action 3.0 cli command "show ip bgp | append flash:/output.txt"
action 3.5 cli command "show ip bgp neigh 10.1.1.20 adv | append flash:/output.txt"
action 4.0 cli command "more flash:/UNION-EVENTS/output.txt"
action 4.5 cli command "term len 25"
action 5.0 mail server "10.100.100.25" to "noc@cisco.com" from "SomeRouter@cisco.com" subject "ASR-LINK-EVENT from ASR1002-EXTRANET" body "$_cli_result"
action 5.5 cli command "del /force flash:/output.txt"
```

### Case 7 - ***Configuration Change Notification and Tracking - Use Case***

For compliance reasons you might want a northbound notification to occur if the configuration is modified on a device. This can be accomplished in the following way.

First turn on Configuration Archiving and keep copies of the configurations over time locally or remotely.

```vtl
archive
 log config
  logging enable
  notify syslog contenttype plaintext
  hidekeys
 path flash:/BACKUP-CONFIG
 maximum 5
 write-memory
```

Then look for 
```vtl
event manager applet CONF_MODIFIED
 event syslog pattern "%PARSER.*LOGGEDCMD:.*logged command:.*"
 action 1.0 cli command "enable"
 action 1.1 set Check "!No changes were found"
 action 1.2 cli command "sh archive config diff nvram:startup-config"
 action 1.3 puts "$_cli_result"
 action 1.4 if $_cli_result ne $Check
 action 1.5  cli command "show clock | append flash:TESTCCIE.txt"
 action 1.6  cli command "wri mem"
 action 1.7  syslog msg "THE CONFIG WAS MODIFIED"
 action 1.8 end

```

### Case 8 - ***Configuring Customized Commands - Use Case***

The alias command is used as a short form for the `clear counters` cli command. The `cc` custom command is then mapped to the applet which clears the counters. Look more closely this applet also deals with questions the IOS presents when entering a command.

```vtl
event manager applet CLEAR-COUNTERS
event none
action 1.0 cli command "enable"
action 2.0 cli command "clear counters" pattern "\[confirm\]"
 action 3.0 cli command "y"
!
alias exec cc event manager run CLEAR-COUNTERS 
```

Another example which displays to screen multiple show commands in a specific way.

```vtl
alias exec showdemo event manager run showdemo

no event manager applet showdemo
event manager applet showdemo
event none sync yes
action 1000 cli command "enable"
action 1010 puts ""
action 1020 puts "Showing DEMO switch ASW-C9300-48-DEMO connectivity"
action 1030 puts ""
action 1110 puts "Showing Interface Switch connected on"
action 1120 cli command "show int status | i 1/1/4"
action 1130 puts "$_cli_result"
action 1140 puts ""
action 1210 puts "Showing IP Address for Downstream Switch"
action 1220 cli command "show cdp ne te 1/1/4 det | i IP|Device"
action 1230 puts "$_cli_result"
action 1240 puts ""
action 1310 puts "Showing if ISIS Routing Established"
action 1320 cli command "show isis ne | i .1.30"
action 1330 puts "$_cli_result"
action 1340 puts ""
```

### Case 9 - ***Automatically Configuring PnP Startup Vlan for PnP - Use Case***

Here we have two examples that will allow for the automated configuration of the `pnp startup-vlan` command on an interface for seed devices connected downstream. The latest modification allows for the applet to work even if the `pnp startup-vlan` command has not been set.

```vtl
 event manager applet pnp_checker authorization bypass
  event syslog pattern "%CDP-4-NATIVE_VLAN_MISMATCH:"
  action 010 cli command "enable"
  action 020 regexp ".* \(([1-9]+)\)," "$_syslog_msg" match native_vlan
  action 030 cli command "show run | i ^pnp startup-vlan"
  action 035 regexp "pnp startup-vlan (.*)\n" "$_cli_result" match current_pnp
  action 036 if $_regexp_result eq 0
  action 037  set current_pnp 10
  action 038 end
  action 039 puts "$current_pnp"
  action 040 puts "$native_vlan"
  action 041 string match "$current_pnp" "$native_vlan"
  action 042 puts "$_string_result"
  action 043 if $_string_result eq "0"
  action 044  syslog msg ">SETTING PNP VLAN FOR ONBOARDING"
  action 050  cli command "conf t"
  action 060  cli command "pnp startup-vlan $native_vlan"
  action 070  cli command "end"
  action 075  puts "end of config"
  action 080 end
```

```vtl
event manager applet pnp_checker authorization bypass
 event syslog pattern "%CDP-4-NATIVE_VLAN_MISMATCH:"
 action 010 cli command "enable"
 action 020 regexp ".* \((.*)\)," "$_syslog_msg" match nativevlan
 action 030 cli command "show run | i ^pnp startup-vlan"
 action 040 regexp "pnp startup-vlan ([^[:space:]]+)" $_cli_result match current_pnp
 action 050 if $current_pnp ne $nativevlan
 action 060  cli command "conf t"
 action 070  cli command "pnp startup-vlan $nativevlan"
 action 080  cli command "end"
 action 090 end
 ```

### Case 10 - ***Automatically converting a Catalyst 9300 between BUNDLE and INSTALL mode***

Here we have two examples that will allow for the conversion between BUNDLE and INSTALL mode for catalyst 9300 switches. These two were put together and will be designed to be deployed in a template to follow shortly.

```
conf t
no event manager applet bundleToInstall authorization bypass
event manager applet bundleToInstall authorization bypass
 event none maxrun 300
 action 100 cli command "enable"
 action 200 cli command "sh boot | include .bin"
 action 201 regexp "(bin)" "$_cli_result" match bootVariable
 action 202 if $bootVariable eq "bin"
 action 203  cli command "dir flash:*.bin | include cat9k_iosxe"
 action 204  regexp "(cat9k.*[.]bin)" "$_cli_result" match Exist
 action 205  if $Exist ne ""
 action 206   set _cli_output "$_cli_result"
 action 207   set high_version "0.0.0"
 action 208   foreach line "$_cli_output" "\n"
 action 209    regexp "(cat9k.*[.]bin)" "$line" match filename
 action 210    regexp "([0-9]+)\.([0-9]+)\.([0-9]+)" "$filename" match v1 v2 v3
 action 211    regexp "([0-9]+)\.([0-9]+)\.([0-9]+)" "$high_version" match c1 c2 c3
 action 212    if $v1 ge "$c1"
 action 213     if $v2 ge "$c2"
 action 214      if $v3 ge "$c3"
 action 215       set high_version "$v1.$v2.$v3"
 action 216       set binFilename "$filename"
 action 217      end
 action 218     end
 action 219    end
 action 220   end
 action 221   puts "Highest version found: $high_version in file $binFilename"
 action 222   puts "Boot System to INSTALL from flash file: $binFilename"
 action 301   cli command "sh switch detail | include Ready"
 action 302   regexp "(.*Ready)+" "$_cli_result" match _cli_output
 action 303   set COUNT "1"
 action 304   cli command "term len 0"
 action 305   foreach line "$_cli_output" "\n"
 action 306    cli command "dir flash-$COUNT:*.conf | include packages"
 action 307    regexp "(packages.conf)" "$_cli_result" match confExist
 action 308    if $confExist ne ""
 action 309     cli command "del /force flash-$COUNT:*.conf"
 action 310    end
 action 311    cli command "dir flash-$COUNT:*.pkg | include pkg"
 action 312    regexp "(cat9k.*[.]pkg)" "$_cli_result" match pkgExist
 action 313    if $pkgExist ne ""
 action 314     cli command "del /force /recursive flash-$COUNT:*.pkg"
 action 315    end
 action 316    increment COUNT 1
 action 317   end
 action 318   cli command "term len 25"
 action 400   cli command "enable"
 action 401   cli command "configure terminal"
 action 402   cli command "no boot system"
 action 403   cli command "boot system switch all flash:packages.conf"
 action 404   cli command "end"
 action 405   cli command "write memory"
 action 406   cli command "request platform software package expand switch all file flash:$binFilename auto-copy force"
 action 407   reload
 action 500  else
 action 501   puts "No Bin File Present - Exiting"
 action 502   if $Exist eq "" goto 999
 action 503  end
 action 600 else
 action 601  puts "Switch already in INSTALL mode - Exiting"
 action 999 end

end
event man run bundleToInstall
```

```
conf t
no event manager applet installToBundle authorization bypass
event manager applet installToBundle authorization bypass
 event none
 action 100  cli command "enable"
 action 200  cli command "sh boot | include packages.conf"
 action 201  regexp "(packages.conf)" "$_cli_result" match bootVariable
 action 202  if packages.conf eq "$bootVariable"
 action 203   cli command "dir flash:*.bin | include cat9k_iosxe"
 action 204   regexp "(cat9k.*[.]bin)" "$_cli_result" match Exist
 action 205   if $Exist ne ""
 action 206    set _cli_output "$_cli_result"
 action 207    set high_version "0.0.0"
 action 208    foreach line "$_cli_output" "\n"
 action 209     regexp "(cat9k.*[.]bin)" "$line" match filename
 action 210     regexp "([0-9]+)\.([0-9]+)\.([0-9]+)" "$filename" match v1 v2 v3
 action 211     regexp "([0-9]+)\.([0-9]+)\.([0-9]+)" "$high_version" match c1 c2 c3
 action 212     if $v1 ge "$c1"
 action 213      if $v2 ge "$c2"
 action 214       if $v3 ge "$c3"
 action 215        set high_version "$v1.$v2.$v3"
 action 216        set binFilename "$filename"
 action 217       end
 action 218      end
 action 219     end
 action 220    end
 action 221    puts "Highest version found: $high_version in file $binFilename"
 action 222    puts "Boot System to set to flash file: $binFilename"
 action 301    cli command "sh switch detail | include Ready"
 action 302    regexp "(.*Ready)+" "$_cli_result" match _cli_output
 action 303    set COUNT "1"
 action 304    cli command "term len 0"
 action 305    foreach line "$_cli_output" "\n"
 action 306     if $COUNT ne "1"
 action 307      cli command "dir flash-$COUNT:$binFilename | include cat9k_iosxe"
 action 308      regexp "(cat9k.*[.]bin)" "$_cli_result" match memberExist
 action 309      if $memberExist ne ""
 action 310       cli command "copy flash:$binFilename flash-$COUNT:$binFilename"
 action 311      end
 action 312     end
 action 313     increment COUNT 1
 action 314    end
 action 314    cli command "term len 25"
 action 400    cli command "enable"
 action 401    cli command "configure terminal"
 action 402    cli command "no boot system"
 action 403    cli command "boot system switch all flash:$binFilename"
 action 404    cli command "end"
 action 405    cli command "write memory"
 action 406    reload
 action 500   else
 action 501    puts "No Bin File Present - Exiting"
 action 502    if $Exist eq "" goto 999
 action 503   end
 action 600  else
 action 601   puts "Switch not in INSTALL mode - Exiting"
 action 999  end

end
event man run installToBundle
```

Catalyst Center template to follow with kron scheduling option and self deletion.

The examples are designed to get you thinking about operations, and what is possible. They may need heavy modification for a production use-case and so these are provided for LAB purposes only. Any use in a production environment should not be done without testing and validation.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](../README.md)