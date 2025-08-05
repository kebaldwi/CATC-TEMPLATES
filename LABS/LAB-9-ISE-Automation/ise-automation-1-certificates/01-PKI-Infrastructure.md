# PKI & System Certificates

## Overview

In order for Catalyst Center and ISE to function securely within our lab environment, we will rely on the use of certificates.  These certificates are used for many functions: such as the Web GUI, API authentication, as well as various endpoint authentication mechanisms like 802.1X with EAP.  To utilize certificates in our lab environment, we must first setup the Public Key Infrastructure (PKI) to generate and manage these certificates.


## General Information

 >[!NOTE]
   >While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host or the AD Server Web RDP.  Within the AD Server Web RDP - you may have issues copy/pasting things into the session, viewing the Lab GitHub page, etc.; so we recommend opening a web browser *within* the Web RDP session itself and navigating to this GitHub repo that you're currently at (URL below for convenience).  Note that you may download and install Chrome (recommended) or if using Firefox it is often best to start it in safe mode with Extensions disabled.

   ***URL for GitHub Repo***

   https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS

This lab consists of the following tasks:

1. [**PKI Infrastructure Build**](#pki-infrastructure-build)
2. [**PKI Certificate Template Build**](#pki-certificate-template-build)

## PKI Infrastructure Build

For lab purposes we will utilize a Microsoft Certificate authority to be built on the Active Directory (AD) server with in the lab. Normally this would be built separately with an offline root and then one (or more) online subordinate certificate authority servers; but within the confines of our lab we will make do with the single AD server provided.

From the dCloud Session View, select the AD server and open a Web RDP console.  Within the AD server, we will first set up the Certificate Authority utilizing Powershell. Open a RDP session to the AD server and we will initiate our PowerShell scripts from there.

>[!IMPORTANT]
>While the code sections below are provided to give you an idea of what the PowerShell scripts are doing in the background, it is **not recommended** to copy and paste them into a PowerShell window.  Instead, download the full PowerShell script from the link below to the AD Server and right click the file and choose "Run with PowerShell".  The reason for this is that there are wait timers built into the full PowerShell script that ensure the various features are fully configured before other tasks start.  Note that the full PowerShell script will take some time to run, so please be patient!  You will be prompted with questions asking if you want to perform certain actions -- choose "A" for "Yes to All" for any prompts you encounter.


<p>Download the full Powershell script here: <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-CA.ps1">⬇︎CA Setup Powershell⬇︎</a></p>

```ps
# Add domain admin account to IIS_IUSRS group in the domain
Add-ADGroupMember -Identity "IIS_IUSRS" -Members "admin"

# Install the Certificate Authority role
Install-WindowsFeature -Name AD-Certificate -IncludeManagementTools

# Configure the Certificate Authority service
$certConfig = @{
    CACommonName = "CA"
    CAType = "EnterpriseRootCA"
    CryptoProviderName = "RSA#Microsoft Software Key Storage Provider"
    HashAlgorithmName = "SHA256"
    KeyLength = 2048
    ValidityPeriod = "Years"
    ValidityPeriodUnits = 5
    DatabaseDirectory = "C:\Windows\System32\CertLog"
    LogDirectory = "C:\Windows\System32\CertLog"
}
Install-AdcsCertificationAuthority @certConfig
```

These are the scripts to get Certification Enrollment Web Services turned on to get a certificate (these are also part of the above PowerShell file, no need to run them separately)

```ps
# Enable the Certificate Authority Web Enrollment service
Install-WindowsFeature -Name ADCS-Web-Enrollment -IncludeManagementTools

# Configure the Certificate Authority Web Enrollment Service
Install-AdcsWebEnrollment 

# Enable the Certificate Authority Online Responder
Add-WindowsFeature Adcs-Online-Cert -IncludeAllSubFeature -IncludeManagementTools

# Configure the Certificate Authority Online Responder Service
Install-AdcsOnlineResponder -Force
```


## PKI Certificate Template Build

Once the certificate authority service is operational, we will then add a template which we will utilize for Catalyst Center, ISE, and various other features.  For a Template to function correctly we will need to provision a certificate which includes usage for both Client and Server Authentication roles. As it also needs to appear in the Web UI, we will need to duplicate a certificate template. The Web Server built in template will be used for duplication purposes.

***Complete the following tasks:***

1. On the AD server:

   1. Open a Web RDP session to the AD server and then open the Certificate Authority App by either finding it under Administrative tools or when the start menu is open typing `Certificate Authority` and clicking the App that appears.
   2. When the App is open then click `Certificate Templates`
   3. Then click `Manage` from the menu list.

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-1.png?raw=true "Import JSON")

2. When the Certificate Template Console is open do the following to duplicate a Certificate Template:

   1. Select the `Web Server` Template towards the bottom of the console
   2. Right click and on the menu select `Duplicate Template`

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-2.png?raw=true "Import JSON")

3. Within the `Properties of New Template` window complete the following:

   #### General Tab

   1. Select `General` tab and rename the template to `Cisco Server Template`

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-3.png?raw=true "Import JSON")
   
   #### Extensions Tab

   1. Select `Extensions` tab
   2. Select `Application Policies`
   3. Click `Edit` and `Edit Application Policies Extension` window  opens
   4. Click `Add` to open the `Add Application Policy` window
   5. Select `Client Authentication` from the list 
   6. Click `OK`

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-4.png?raw=true "Import JSON")

   7. Click `OK` on the `Edit Application Policies Extension` window

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-5.png?raw=true "Import JSON")

   8. Click `Apply` on the `Extension` tab of `Properties of New Template` window

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-6.png?raw=true "Import JSON")

   8. Click `OK` to close the `Properties of New Template` window
      
      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-7.png?raw=true "Import JSON")
   
   9. The new `Cisco Server Template` will appear in the list

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-8.png?raw=true "Import JSON")

4. We will now enable the use of the Newly created Certificate Template by completing the following:

   1. Right click `Certificate Templates` within the `Certificate Authority` app
   2. On the menu select `New` and then `Certificate Template to Issue`

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-9.png?raw=true "Import JSON")
      
   3. On the `Enable Certificate Templates` window select our new `Cisco Server Template` and click `OK`

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-10.png?raw=true "Import JSON")

   4. The new `Cisco Server Template` will appear in the list of `Certificate Templates` to be issued. This is the list which is used by the Certificate Web Services.

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-11.png?raw=true "Import JSON")

   5. To confirm its working in a web browser on the AD server type `http://localhost/certsrv` then log in with the username `admin` and password `C1sco12345`

   6. Navigate to an advanced certificate request and ensure the new `Cisco Server Template` appears in the Web UI.

      ![json](../../../ASSETS/LABS/AD/CERTS/AD-Cert-Template-12.png?raw=true "Import JSON")

Now that we've setup our PKI infrastructure, we can use these templates to provision certificates for Catalyst Center and ISE.

[**Catalyst Center Certificate Setup**](./02-Catatlyst-Center.md)

[**ISE Certificate Setup**](./03-ISE-Certificates)

[**Return to ISE Automation Lab Menu**](./../README.md)