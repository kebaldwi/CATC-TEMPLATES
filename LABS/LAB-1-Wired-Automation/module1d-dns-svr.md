## DNS Discovery using Windows based DHCP and DNS Services

As you may recall, for a device to discover Catalyst Center, the device uses a discovery method to help it find Catalyst Center. 

The PnP components are as follows:

![json](../../ASSETS/COMMON/CATC/pnp-workflows.png?raw=true "Import JSON")

There are three automated methods to make that occur and in this section we will use DNS Discovery. To aide in that we are goiing to utilize both Windows DHCP and DNS services. The Target switch, commonly called Access switch will need to do a DNS lookup in order to find Catalyst Center.

**DNS lookup** 
  - *requires the DHCP server to offer a domain suffix and a name server to resolve the **pnpserver** address*
  - *requires the **pnpserver** entry to appear in the Subject Alternative Name of the GUI Certificate*

### Step 5.2a - Windows DHCP with DNS Discovery

#### DHCP Overview

If we want to use the Windows DHCP service, connect to the windows **AD1** server. On the windows server, you have two options to deploy DHCP scopes the UI or PowerShell. We will deploy the scope via PowerShell. First we will create the required DHCP scope with the following options:

- Network
- Router
- Name Server IP
- Domain Suffix

When using the Windows DHCP Server with the DNS Lookup discovery method, we will add the appropriate DNS server IP addresses along with the domain suffix that the switch will use to resolve the **pnpserver** record within DNS. 

![json](../../ASSETS/LABS/WIRED/WindowsDHCPscope.png?raw=true "Import JSON")

This is an **example** of how you can build a **scope** below. For the **configuration** please download and use the **script** here: 

```ps
Add-DhcpServerv4Scope -Name "DNAC-Templates-Lab" -StartRange 192.168.5.1 -EndRange 192.168.5.254 -SubnetMask 255.255.255.0 -LeaseDuration 6.00:00:00 -SuperScope "PnP Onboarding"

Set-DhcpServerv4OptionValue -ScopeId 192.168.5.0 -Router 192.168.5.1 
Add-Dhcpserverv4ExclusionRange -ScopeId 192.168.5.0 -StartRange 192.168.5.1 -EndRange 192.168.5.1

Set-DhcpServerv4OptionValue -ScopeId 192.168.5.0 -DnsServer 198.18.133.1 -DnsDomain "pnp.dcloud.cisco.com"

```

#### DNS Overview

Next, we will add the relevant DNS entries into the Windows DNS service to allow for the Catalyst Center to be discovered. This script will add an A host entry for the VIP address and a CNAME entry as an alias for the pnpserver record required for DNS discovery.

The DNS Zone will look like this in Windows DNS Administrative tool: 

![json](../../ASSETS/LABS/WIRED/DNACenterDNSentries.png?raw=true "Import JSON")

![json](../../ASSETS/LABS/WIRED/DNACenterDNSentries2.png?raw=true "Import JSON")

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

### Step 5.2b - Windows DHCP and DNS Discovery Configuration

In this section we will prepare Domain Name System (DNS) and Dynamic Host Configuration Protocol (DHCP) on the Windows Server within the lab environment. 

#### Configuring DHCP and DNS via Powershell

1. Download the powershell script to the **windows server** using the <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-DNS.ps1">⬇︎powershell-DNS.ps1⬇︎</a> file.

2. Once downloaded, extract the file.

   ![json](../../ASSETS/LABS/WIRED/Powershell-Extract.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/WIRED/Powershell-Extract-Location.png?raw=true "Import JSON")

3. Right click on the file and run with powershell.

   ![json](../../ASSETS/LABS/WIRED/Powershell-Run.png?raw=true "Import JSON")

4. You may see a security warning. If you do accept it by entering **Y**.

   ![json](../../ASSETS/LABS/WIRED/Powershell-Security.png?raw=true "Import JSON")

At this point all the DNS and DHCP configuration on the **windows server** will be generated.

   ![json](../../ASSETS/LABS/WIRED/DNS-DHCP.png?raw=true "Import JSON")

### Step 5.2c - Windows DHCP Helper Configuration

Next, we will introduce the helper address statement on the management VLAN's SVI to point to the Windows DHCP server. Connect to switch **c9300-2** and paste the following configuration:

```vtl
!
conf t
!
  interface Vlan 5                         
     ip helper-address 198.18.133.1                  
     end
!
wr

```

#### Verification and Testing

To test the environment to ensure it's ready, we need to try a few things.

First, from a Windows host, use the *nslookup* command to resolve **pnpserver.dcloud.cisco.com**. Connect to the Windows workstation, and within the search window, search for CMD. Open the application and type the following command:

```bash
nslookup pnpserver.pnp.dcloud.cisco.com

```

The following output or something similar shows the resolution of the alias to the A host record entry which identifies the VIP address for the Catalyst Center Cluster will display.

![json](../../ASSETS/LABS/WIRED/CC-Discovery-dns-lookup-ipv4.png?raw=true "Import JSON")

Second, we need to ensure the Catalyst Center responds on the VIP, so use the ping command within the CMD application window previously opened as follows:

```bash
ping pnpserver.pnp.dcloud.cisco.com

```

The test results should look similar to this:

![json](../../ASSETS/LABS/WIRED/CC-Discovery-dns-ipv4.png?raw=true "Import JSON")

Third, we can ping Catalyst Center from the Distribution Switch utilizing the following scripts:

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

![json](../../ASSETS/LABS/WIRED/CC-Discovery-DNS-Test-ipv4.png?raw=true "Import JSON")

At this point, the environment should be set up to onboard devices within VLAN 5 using the network address **192.168.5.0/24** utilizing **DNS discovery **

> [**Return to PnP Preparation Lab**](./module1e-reset.md#step-6---reset-eem-script-or-pnp-service-reset)
