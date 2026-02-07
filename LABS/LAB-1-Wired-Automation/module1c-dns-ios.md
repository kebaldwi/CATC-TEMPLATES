## DNS Discovery using IOS DHCP and Windows DNS Services

As you may recall, for a device to discover Catalyst Center, the device uses a discovery method to help it find Catalyst Center. 

The PnP components are as follows:

![json](../../ASSETS/COMMON/CATC/pnp-workflows.png?raw=true "Import JSON")

There are three automated methods to make that occur and in this section we will use DNS Discovery. To aide in that we are goiing to utilize a combination of IOS DHCP with DNS services. The Target switch, commonly called Access switch will need to do a DNS lookup in order to find Catalyst Center.

**DNS lookup** 
  - *requires the DHCP server to offer a domain suffix and a name server to resolve the **pnpserver** address*
  - *requires the **pnpserver** entry to appear in the Subject Alternative Name of the GUI Certificate*

### Step 5.2a - IOS DHCP with DNS Discovery 

#### DHCP Overview

If we want to use the IOS-XE DHCP service configured on an IOS device, the DHCP pool elements would be configured either on a router or switch in the network. We will configure the DHCP scope, and add DHCP options to the switch or router providing the DHCP services. Additionally we will add the helper address statement on the management VLAN's SVI to point to the router or switch to the DHCP configuration. First we will create the required DHCP scope with the following options:

- Network
- Router
- Name Server IP
- Domain Suffix

When using the IOS-XE DHCP Service with the DNS Lookup discovery method, we will add the appropriate DNS server IP addresses along with the domain suffix that the switch will use to resolve the **pnpserver** record within DNS. 

#### DNS Overview

Next, we will add the relevant DNS entries into the Windows DNS service to allow for the Catalyst Center to be discovered. This script will add an A host entry for the VIP address and a CNAME entry as an alias for the pnpserver record required for DNS discovery.

The DNS Zone will look like this in Windows DNS Administrative tool: 

![json](./images/DNACenterDNSentries.png?raw=true "Import JSON")

![json](./images/DNACenterDNSentries2.png?raw=true "Import JSON")

> [!NOTE] 
> To utilize DNS Entry for Discovery purposes Certificates will need to be rebuilt with Subject Alternative Names. Please utilize the process documented in the following page [**Certificate Deployment**](./Certificates.md) for information on that process.

This is an **example** of how you can build a **DNS Records** below. For the configuration please download and use the script here: 

```ps
Add-DnsServerResourceRecordA -Name "dnac-vip" -ZoneName "dcloud.cisco.com" -AllowUpdateAny -IPv4Address "198.18.129.100" -TimeToLive 01:00:00
Add-DnsServerResourceRecordCName -Name "dnac" -HostNameAlias "dnac-vip.dcloud.cisco.com" -ZoneName "dcloud.cisco.com"

Add-DnsServerPrimaryZone -Name "pnp.dcloud.cisco.com" -ReplicationScope "Forest" -PassThru

#Pause required to allow Zone to be created prior to CNAME Entry
Start-Sleep -Seconds 60

Add-DnsServerResourceRecordCName -Name "pnpserver" -HostNameAlias "dnac-vip.dcloud.cisco.com" -ZoneName "pnp.dcloud.cisco.com"
```

### Step 5.2b - IOS DHCP and DNS Discovery Configuration

In this section we will prepare Domain Name System (DNS) on the Windows Server and Dynamic Host Configuration Protocol (DHCP) on the IOS-XE Switch within the lab environment. 

#### Configuring DNS via Powershell

1. Download the powershell script to the **windows server** using the <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-DNS.ps1">⬇︎powershell-DNS.ps1⬇︎</a> file.

2. Once downloaded, extract the file.

   ![json](./images/Powershell-Extract.png?raw=true "Import JSON")
   ![json](./images/Powershell-Extract-Location.png?raw=true "Import JSON")

3. Right click on the file and run with powershell.

   ![json](./images/Powershell-Run.png?raw=true "Import JSON")

4. You may see a security warning. If you do accept it by entering **Y**.

   ![json](./images/Powershell-Security.png?raw=true "Import JSON")

At this point all the DNS and DHCP configuration on the **windows server** will be generated.

   ![json](./images/DNS-DHCP.png?raw=true "Import JSON")

### Step 5.2c - IOS DHCP Service Configuration

Next, we will introduce the IOS DHCP Service and helper address configurations. This is an **example** of how you can build a **scope** below. Connect to switch **c9300-2** and please copy and paste the **script** to **configure** the **c9300-2** switch:

```vtl
!
conf t
!
  ip dhcp excluded-address 192.168.5.1 192.168.5.1
  ip dhcp pool pnp_device_pool                         
     network 192.168.5.0 255.255.255.0                  
     default-router 192.168.5.1 
     dns-server 198.18.133.1                           
     domain-name dcloud.cisco.com                       
!
  interface Vlan 5                         
     ip helper-address 192.168.5.1                  
     end
!
wr

```

#### Verification and Testing

To test the environment to ensure it's ready, we need to try a few things.

First, from a Windows host, use the *nslookup* command to resolve **pnpserver.dcloud.cisco.com**. Connect to the Windows workstation, and within the search window, search for CMD. Open the application and type the following command:

```bash
nslookup pnpserver.dcloud.cisco.com

```

The following output or something similar shows the resolution of the alias to the A host record entry which identifies the VIP address for the Catalyst Center Cluster will display.

![json](./images/DNACenterDNStests.png?raw=true "Import JSON")

Second, we need to ensure the Catalyst Center responds on the VIP, so use the ping command within the CMD application window previously opened as follows:

```bash
ping pnpserver.dcloud.cisco.com

```

The test results should look similar to this:

![json](./images/DNACenterDNStestPing.png?raw=true "Import JSON")

Third, we can ping Catalyst Center from the Distribution Switch utilizing the following:


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

```bash
ping 198.18.129.100 source vlan 5 repeat 3

```

```bash
ping pnpserver.pnp.dcloud.cisco.com source vlan 5 repeat 3

```

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
The test results should look similar to this:

![json](./images/CC-Discovery-DNS-Test-ipv4.png?raw=true "Import JSON")

At this point, the environment should be set up to onboard devices within VLAN 5 using the network address **192.168.5.0/24** utilizing **DNS discovery**

> [**Return to PnP Preparation Lab**](./module1e-reset.md#step-6---reset-eem-script-or-pnp-service-reset)
