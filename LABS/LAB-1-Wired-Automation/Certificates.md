# System Certificates

## Overview

Cisco Catalyst Center has a Graphical User Interface (GUI), which is protected by SSL encryption. This GUI utilizes a certificate which is automatically generated when the system is configured for the first time, and automatically incorporates the FQDN at that time. 

Obviously, most organizations do not want self signed certificates used in their infrastructure, and so want to tie Cisco Catalyst Centers certificates into their PKI infrastructure. 

In this small set of tasks we will accomodate that ask. It is important to note that while this set of tasks will always work, a new GUI tool has been incorporated in the newest version of Cisco Catalyst Center to facilitate the building of the Certificate Signing Request. For all versions prior to Cisco Catalyst Center **2.3.5.x** this method is detailed in the following [Cisco Catalyst Center Security Best Practices Guide](./DNACenter_security_best_practices_guide.pdf) guide.

## PKI Infrastructure Build

For lab purposes we will utiize a Microsoft Certificate authority to be built on the Active Directory (AD) server with in the lab. Normally this would be built separately with an offline root, and subordinate certificate authority servers, but within the confines of our lab we will make do with the AD server provided.

Within the AD server, we will first set up the Certificate Authority utilizing Powershell. Open a RDP session to the AD server and then the Powershell application and utilize this script:

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

Next we need the Certification Enrollment Web Services turned on to get a certificate

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

<p>Download the full Powershell script here: <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-CA.ps1">⬇︎CA Setup Powershell⬇︎</a></p>

## PKI Certificate Template Build

Once the certificate authority service is operational, we will then add a template which we will utilize for Cisco Catalyst Center.
This same template may also be used for ISE. For a Template to function correctly we will need to provision a certificate which includes usage for both Client and Server Authentication roles. As it also needs to appear in the Web UI, we will need to duplicate a certificate template. The Web Server built in template will be used for duplication purposes.

1. Follow the following steps on the AD server:

   1. Open a Web RDP session to the AD server and then open the Certificate Authority App by either finding it under Administrative tools or when the start menu is open typing `Certificate Authority` and clicking the App that appears.
   2. When the App is open then click `Certificate Templates`
   3. Then click `Manage` from the menu list.

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-1.png?raw=true "Import JSON")

2. When the Certificate Template Console is open do the following to duplicate a Certificate Template:

   1. Select the `Web Server` Template towards the bottom of the console
   2. Right click and on the menu select `Duplicate Template`

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-2.png?raw=true "Import JSON")

3. Within the `Properties of New Template` window complete the following:

   #### General Tab

   1. Select `General` tab and rename the template to `Cisco Server Template`

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-3.png?raw=true "Import JSON")
   
   #### Extensions Tab

   1. Select `Extensions` tab
   2. Select `Application Policies`
   3. Click `Edit` and `Edit Application Policies Extension` window  opens
   4. Click `Add` to open the `Add Application Policy` window
   5. Select `Client Authentication` from the list 
   6. Click `OK`

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-4.png?raw=true "Import JSON")

   7. Click `OK` on the `Edit Application Policies Extension` window

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-5.png?raw=true "Import JSON")

   8. Click `Apply` on the `Extension` tab of `Properties of New Template` window

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-6.png?raw=true "Import JSON")

   8. Click `OK` to close the `Properties of New Template` window
      
      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-7.png?raw=true "Import JSON")
   
   9. The new `Cisco Server Template` will appear in the list

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-8.png?raw=true "Import JSON")

4. We will now enable the use of the Newly created Certificate Template by completing the following:

   1. Right click `Certificate Templates` within the `Certificate Authority` app
   2. On the menu select `New` and then `Certificate Template to Issue`

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-9.png?raw=true "Import JSON")
      
   3. On the `Enable Certificate Templates` window select our new `Cisco Server Template` and click `OK`

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-10.png?raw=true "Import JSON")

   4. The new `Cisco Server Template` will appear in the list of `Certificate Templates` to be issued. This is the list which is used by the Certificate Web Services.

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-11.png?raw=true "Import JSON")

   5. To confirm its working in a web browser on the AD server type `http://localhost/certsrv` then log in with the username `admin` and password `C1sco12345`

   6. Navigate to an advanced certificate request and ensure the new `Cisco Server Template` appears in the Web UI.

      ![json](../../ASSETS/LABS/WIRED/AD-Cert-Template-12.png?raw=true "Import JSON")

Now that we have successfully enabled the Certificate Authority and templates lets go ahead and build the Cisco Catalyst Center certificate.

## Cisco Catalyst Center Certificate Installation

### Building the Certificate Signing Request 

To build the Certificate Signing Request we will utilize openssl and use a config file. This process can be completed on any platform with openssl installed. It does not necessarily need to be Cisco Catalyst Center. 

Open an RDP session to the `Jump Host` and from within the desktop session open the mRemoteNG application for SSH sessions.

![json](../../ASSETS/LABS/WIRED/Cert-CSR-1.png?raw=true "Import JSON")

**Complete the following tasks:**

1. Double click on the Cisco Catalyst Center link to open a session

2. Log in to Cisco Catalyst Center with the following credentials **username: `maglev`** and **password: `C1sco12345`**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-2.png?raw=true "Import JSON")

3. Within Cisco Catalyst Center issue the `pwd` command and ensure we are in the path `/home/maglev`

4. Create and then change directory to `/home/maglev/certs` by issuing the command `mkdir certs && cd certs`

5. create the openssl.cnf file used for configuration using the command `touch ./openssl.cnf`

6. Open the VI terminal with the **openssl.cnf** file using `vi ./openssl.cnf` 

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-3.png?raw=true "Import JSON")

7. Paste the following into the window by right click.

```
req_extensions = v3_req
distinguished_name = req_distinguished_name
default_bits = 4096
default_md = sha512
prompt = no
[req_distinguished_name]
C = US
ST = NC
L = RTP
O = CISCO
OU = DCLOUD
CN = dnac-vip.dcloud.cisco.com
emailAddress = kebaldwi@cisco.com

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = dnac-vip.dcloud.cisco.com
DNS.2 = dnac.dcloud.cisco.com
DNS.3 = pnpserver.dcloud.cisco.com
DNS.4 = pnpserver.pnp.dcloud.cisco.com
IP.1 = 198.18.129.100
```
8. Write and Close the file by typing `:` then `wq!`

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-5.png?raw=true "Import JSON")

9. Create a **CSR Key** using the command `openssl genrsa -out csr.key 4096`

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-6.png?raw=true "Import JSON")

10. Using the premade **csr.key** we will now create the **CSR** to be submitted to Cisco Catalyst Center. Use the command `openssl req -config openssl.cnf -new -key csr.key -out DNAC.csr`

    ![json](../../ASSETS/LABS/WIRED/Cert-CSR-7.png?raw=true "Import JSON")

11. We will then display the file and copy and paste it within Certificate Authority Web Server Application. To display the file use the command `more ./DNAC.csr`

    ![json](../../ASSETS/LABS/WIRED/Cert-CSR-8.png?raw=true "Import JSON")

### Submitting the Certificate Signing Request

1. Open Chrome and enter the URL `http://198.18.133.1/certsrv` and log in with the credentials **username: `admin`** and **password: `C1sco12345`**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-9.png?raw=true "Import JSON")

2. Within the Certificate Authority Web Site navigate the following:

   1. Click Request a Certificate

      ![json](../../ASSETS/LABS/WIRED/Cert-CSR-10.png?raw=true "Import JSON")

   2. Click advanced certificate request

      ![json](../../ASSETS/LABS/WIRED/Cert-CSR-11.png?raw=true "Import JSON")

   3. To submit the Certificate Request paste the CSR as shown

      ![json](../../ASSETS/LABS/WIRED/Cert-CSR-12.png?raw=true "Import JSON")

   4. **Important** Select `Cisco Server Template` for the Certificate Template and click submit

      ![json](../../ASSETS/LABS/WIRED/Cert-CSR-13.png?raw=true "Import JSON")

   5. On the Certificate Issued page:
      1. **Important** select **DER encoded**
      2. **Important** download from the link **Download Certificate Chain** and save it as `dnac-chain.p7b`

         ![json](../../ASSETS/LABS/WIRED/Cert-CSR-14.png?raw=true "Import JSON")

   7. Open the windows command prompt `CMD` application and do the following:
      1. Change directory to the Downloads directory `cd Downloads`
      2. Check the directory to ensure the file `dnac-chain.p7b` exists via the command `dir`
      3. Copy the file to Cisco Catalyst Center using scp usint the following command `scp -P 2222 ./dnac-chain.p7b maglev@198.18.129.100:/home/maglev/certs` and when prompted the **username: `maglev`** and the **password: `C1sco12345`**

         ![json](../../ASSETS/LABS/WIRED/Cert-CSR-16.png?raw=true "Import JSON")

   8. On Cisco Catalyst Center via the mRemoteNG SSH session we now will take the certificate chain and create a Privacy Enhanced Mail (PEM) file for import into Cisco Catalyst Centers GUI. Use the command `openssl pkcs7 -in dnac-chain.p7b -inform DER -out dnac-chain.pem -print_certs`

      ![json](../../ASSETS/LABS/WIRED/Cert-CSR-17.png?raw=true "Import JSON")


Congratulations the Certificate is prepared, now we will import it into Cisco Catalyst Center.

### Installing Cisco Catalyst Centers Certificate

1. First lets download the **Certificate** to our workstation using the scp command `scp -P 2222 maglev@198.18.129.100:/home/maglev/certs/dnac-chain.pem ./` and when prompted the **username: `maglev`** and the **password: `C1sco12345`**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-18.png?raw=true "Import JSON")

2. Second lets download the **CSR KEY** to our workstation using the scp command `scp -P 2222 maglev@198.18.129.100:/home/maglev/certs/csr.key ./` and when prompted the **username: `maglev`** and the **password: `C1sco12345`**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-19.png?raw=true "Import JSON")

3. Log into Cisco Catalyst Center with the credentials **username: `admin`** and **password: `C1sco12345`**

4. Navigate to the Menu and then Select **System > Settings**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-22.png?raw=true "Import JSON")

5. On the Settings page scroll on the left down to and select **Certificates**

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-23.png?raw=true "Import JSON")

6. On the System tab click the **Replace Certificate** button

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-24.png?raw=true "Import JSON")

7. On the **Certificates** page select **PEM** then click the link to choose the file `dnac-chain.pem` from the Downloads directory. When opened into the UI click the **Upload** button

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-26.png?raw=true "Import JSON")

8. Scroll down the page to the Private Key section. Then click the link to choose the file `csr.key` from the Downloads directory. When opened into the UI click the **Upload** button

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-28.png?raw=true "Import JSON")

9. Scroll down to the Encryption question and select **No** as we did not encrypt the certificate. Then click **Save** and lastly **Continue**.

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-29.png?raw=true "Import JSON")

Cisco Catalyst Center will now log out. After a few minutes refresh the GUI from the browser then display the certificate within the Browser and it should look like this.

   ![json](../../ASSETS/LABS/WIRED/Cert-CSR-30.png?raw=true "Import JSON")

Congratulations you have changed the certificate and are now ready to use DNS for discovery purposes. The Root CA may also be used in this lab for Identity Services Engine, and through a CAP Profile EAP certificates. All that would be needed would be in ISE to import the ROOT CA certificate into the trust store in ISE, and then create a CSR from the UI which includes the SAN IP and DNS names for the ISE environment. Then once binding the certificate ensure the roles for the Certificate are enabled. Once the Certificate is installed and operational for the roles desired, policy may be used. This will be discussed in a future lab in detail.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Lab**](./README.md)