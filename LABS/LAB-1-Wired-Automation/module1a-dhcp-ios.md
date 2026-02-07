## DHCP Discovery using IOS DHCP Service

As you may recall, for a device to discover Catalyst Center, the device uses a discovery method to help it find Catalyst Center. 

The PnP components are as follows:

![json](../../ASSETS/COMMON/CATC/pnp-workflows.png?raw=true "Import JSON")

There are three automated methods to make that occur and in this section we will use DHCP Discovery. To aide in that we are goiing to utilize IOS DHCP services. The Target switch, commonly called Access switch will need to be offered option 43 with a string in order to find Catalyst Center.

**DHCP Option 43** 
  - *requires the DHCP server to offer a Vendor Spcecific Information (VSI) known as ***Option 43*** which serves the **pnp servers IP** address*

That string is offered as a scope option typically referred to as **Option 43** where the string **`5A1D;B2;K4;I198.18.129.100;J80`** can be explained as follows:

### Overview of Option 43 VSI String

The format of the Option 43 as a ascii text string is broken down as follows:

```shell
Option 43 format 
 The option 43 string has the following components, delimited by semicolons:
 
PnP string: 5A1D;B2;K4;I198.18.129.100;J80 
 
Description - dhcpc receiving DHCP Offer with option 43 info, pass the info to PNPA 
 *     5A = PnP DHCP ID
 *     1D = PnP DHCP debug on
 *     1N = PnP DHCP debug off
 *     token.B = <address type> 1:Host; 2:IPv4; 3:IPv6
 *     token.K = <protocol> 1: XMPP-starttls; 2: XMPP-socket; 3:: XMPP-tls; 4: HTTP; 5: HTTPS
 *     token.I = <remote server ip add / hostname>
 *     token.J = <remote server port> valid ports are 80 or 443
 
Further explanation of PnP string and how to read:

5A1N;             Specifies the DHCP suboption for Plug and Play, active operation, version 1, 
                  no debug information. It is not necessary to change this part of the string.
                  
B2;               IP address type: in this case IPv4 format
                  Alternates would be: 
                            B1 = hostname
                            B2 = IPv4 (default)

K4;               Transport protocol to be used between the device and the controller: In 
                  this example HTTP transport
                  K4 = HTTP (default)
                  K5 = HTTPS

Ixxx.xxx.xxx.xxx; IP address or hostname of the Catalyst Center controller (following a 
                  capital letter i). In this example, the IP address is 198.18.129.100.
                  
Jxxxx             Port number to use to connect to the Catalyst Center controller. 
                  In this example, the port number is 80. The default is port 80 for HTTP 
                  and port 443 for HTTPS.
```

### Step 5.2a - IOS DHCP and Option 43 Discovery Configuration

We will configure **DHCP Services** to run on the **Catalyst 9300-2** within the Lab. The DHCP pool elements could be configured either on a router or switch in the network. 

Within the scope below you will see the **Option 43** discovery method utilized and the relevant **ASCII** string added to the scope.

Additionally, we will configure the **`helper-address`** statement on the management VLAN's SVI to point to the router or switch hosting the **DHCP Service** configuration. In the lab as we are completing all this configuration on the **C9300-2** the **helper-address** will point to an IP hosted on itself.

Connect to switch **c9300-2** and paste the following configuration:

```vtl
!
conf t
!
  ip dhcp excluded-address 192.168.5.1 192.168.5.1
  ip dhcp pool pnp_device_pool                         
     network 192.168.5.0 255.255.255.0                  
     default-router 192.168.5.1 
     option 43 ascii "5A1N;B2;K4;I198.18.129.100;J80"
!
  interface Vlan 5                         
     ip helper-address 192.168.5.1                  
     end
!
wr

```

For a complete configuration example please see [Configuring the Cisco IOS DHCP Server](https://www.cisco.com/en/US/docs/ios/12_4t/ip_addr/configuration/guide/htdhcpsv.html#wp1046301)

### Step 5.2b - Client Windows DHCP and DNS Services Configuration

In this section we will prepare Domain Name System (DNS) and Dynamic Host Configuration Protocol (DHCP) on the Windows Server within the lab environment for the remaining client onboarding and connectivity. These services are required for the other VLANs for **host onboarding**.

#### Configuring DHCP and General DNS Services via Powershell

1. Download the powershell script to the **windows server** using the <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-DHCP.ps1">**⬇︎powershell-DHCP.ps1⬇︎**</a> file.

2. Once downloaded, extract the file.

   ![json](./images/Powershell-Extract.png?raw=true "Import JSON")
   ![json](./images/Powershell-Extract-Location.png?raw=true "Import JSON")

3. Right click on the file and run with powershell.

   ![json](./images/Powershell-Run.png?raw=true "Import JSON")

4. You may see a security warning. If you do accept it by entering **Y**.

   ![json](./images/Powershell-Security.png?raw=true "Import JSON")

At this point all the DNS and DHCP configuration on the **windows server** will be generated.

   ![json](./images/DNS-DHCP.png?raw=true "Import JSON")

#### Verification and Testing

To test the environment to ensure it's ready, we need to try a few things.

First, we need to ensure the Catalyst Center responds on the VIP, lets test that from the **9300-2**:

```bash
!
conf t
  !
  ip name-server 198.18.133.1
  !
  interface Vlan 5                         
    no autostate                  
    end

```

![json](./images/CC-Discovery-pretest-dhcp-ipv4.png?raw=true "Import JSON")

Second, lets check the configuration on the **9300-2**:

```bash
sh vlan id 5 | i active

sh run int vlan 5

ping 192.168.5.1 repeat 3

```

```bash
ping 198.18.129.100 repeat 3

```

```bash
ping 198.18.129.100 source vlan 5 repeat 3

```

The test results should look similar to this:

![json](./images/CC-Discovery-test-dhcp-ipv4.png?raw=true "Import JSON")

Last, we need to ensure the **9300-2** is in the normal state:

```bash
!
conf t
  !
  no ip name-server 198.18.133.1
  !
  interface Vlan 5                         
    autostate                  
    end

```

![json](./images/CC-Discovery-posttest-dhcp-ipv4.png?raw=true "Import JSON")

At this point, the environment should be set up to onboard devices within VLAN 5 using the network address **192.168.5.0/24** utilizing **DHCP discovery**

> [**Return to PnP Preparation Lab**](./module1e-reset.md#step-6---reset-eem-script-or-pnp-service-reset)
