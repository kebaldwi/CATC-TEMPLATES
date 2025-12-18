# ISE Certificate Setup (via API)

## Overview

In this lab module, we will setup ISE certificates via the API.  This is the recommended methodology for deploying a larger number of ISE nodes, or for any environment that is deployed programmatically.


## General Information

>[!WARNING]
>You must have completed [**PKI Infrastructure Setup Module**](./01-PKI-Infrastructure.md) before completing this lab module.

>[!NOTE]
>:mega: If you have already done these steps via the GUI in the [**03a-ISE-GUI**](./03a-ISE-GUI.md), the certificates you generated will need to be deleted first.<br><br>
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host.  

This lab module consists of the following tasks:

   1. [**Enabling APIs on ISE**](#enabling-apis-on-ise)
   2. [**Exporting Windows Root CA Certificate**](#exporting-the-windows-root-ca-certificate)
   3. [**Cleaning Up the Windows Root CA Certificate**](#cleaning-up-the-windows-root-ca-certificate)
   4. [**Installing the Root CA in ISE**](#installing-the-root-ca-in-ise)
   5. [**Generating a Certificate Signing Request**](#generating-a-certificate-signing-request)
   6. [**Signing the ISE CSR with the Certificate Authority**](#signing-the-ise-csr-with-certificate-authority)
   7. [**Cleaning Up the Signed ISE Certificate**](#cleaning-up-the-signed-ise-certificate)
   8. [**Getting the CSR "ID"**](#getting-the-csr-id)
   9. [**Binding the CSR with the Certificate**](#binding-the-csr-with-the-certificate)


## Enabling APIs on ISE

Unfortunately, by default, when an ISE instance is first spun up (as it is in this lab) - it has its API access disabled.  We must enable this via the GUI before we can use APIs.

***Complete the following tasks:***

1. From the Windows Jump Box, open a Chrome browser and navigate to ISE using https://198.18.133.27 (or using the bookmark) and login with ***username: `admin`*** and ***password: `C1sco12345`***

2. From the hamburger menu in the top left hand corner:

   1. Mouse over ***Administration*** then 
   
   2. Under ***System*** choose ***Settings***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-9.png?raw=true "Import JSON")

3. On the left, choose 
   
   1. ***API Settings*** then

   2. ***API Service Settings***

   3. Enable both ***ERS (Read/Write)*** and ***Open API (Read/Write)*** and then 
   
   4. ***Save***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-10.png?raw=true "Import JSON")


Now ISE should be ready for API calls, but before we can get to that...lets get our certificate ready!

## Exporting the Windows Root CA Certificate

>[!NOTE]
>If you have completed the certificate export as part of the [***02-Catalyst-Center module***](./02-Catatlyst-Center.md) (as part of this same lab slot)- you do not need to export the CA cert again as long as it is in Base 64 format.

***Complete the following tasks:***

1. From the Windows Jump Box, open Chrome browser and navigate to http://198.18.133.1/certsrv/ and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From here, click on ***Download a CA Certificate***

   ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-10.png?raw=true "Import JSON")

3. Since we only have a single CA in our lab environment, the only one that should show up should be "Current[CA]".  

   1. Set the ***Encoding Method*** as Base 64 and 
   
   2. click ***Download CA certificate***

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-GUI-CSR-1b.png?raw=true "Import JSON")

   You may see a prompt from the browser to ***Keep*** or ***Discard*** this download, choose ***Keep***.  By default, the file will save to the Downloads folder as `certnew.cer`

>[!TIP]
>We recommend changing the name of this .cer file to something like `RootCA.cer` as we will use this file multiple times over the course of these labs, and changing the name from the generic `certnew` will make it easier to find again.

## Cleaning Up the Windows Root CA Certificate

Because text editors tend to add either carriage returns or line feeds (or both) to certificate files, we need to modify the text of the Root CA file a bit so that we can use it within our Postman API call.  To do so, we will utilize Notepad++ for this example.  Similar ways of cleaning up certificate files exist either in PowerShell (for Windows) or the ***awk*** utility on MacOS/Linux - but these are outside the scope of this lab.

***Complete the following tasks:***

1. Locate the Root CA file in the Downloads folder of the Windows Jump Host (or wherever you saved it - reminder that by default it is named `certnew.cer`)

2. Right click and choose ***Edit with Notepad++***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-1.png?raw=true "Import JSON")

3. Here, we are going to use the ***Replace*** tool to perform several tasks.

   1. Select all text with either ***Ctrl+A*** or by highlighting all text with your mouse cursor

   2. In the menu bar, click ***Search > Replace*** this opens the Replace window.

   3. In the bottom left of the Replace window, change the "Search Mode" from Normal to ***Extended***

         ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-2.png?raw=true "Import JSON")

   3. In the ***Find what:*** field, enter "\n" (without quotes), leave the ***Replace with:*** field blank, and click ***Replace All***.

         ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-3.png?raw=true "Import JSON")

   4. Next, in the ***Find what:*** field, enter "\r" (without quotes), and in the ***Replace with:*** field enter "\\\n" (without quotes).  
         
         Again click ***Replace All***

         ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-4.png?raw=true "Import JSON")

   5. What we should now be left with is a very long string with several "\n" where line breaks used to be.

         ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-5.png?raw=true "Import JSON")

   6. Close out of the Replace window and copy the entirety of the line of text to the clipboard.

## Installing the Root CA in ISE

At this point, it is assumed that you have successfully opened Postman application and imported the Collection and Environment. If you have not, please go back and complete the [***03-Postman***](../ise-automation-0-orientation/03-Postman.md) module.

***Complete the following tasks:***

1. Under ***Collections > lab-9-ise-automation-collection > ISE***, expand the ***CERTIFICATES*** folder and look for ***POST - Import Trusted Certificate***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-6.png?raw=true "Import JSON")

2. When the request opens, click on the ***Body*** field and note that all of the entries have been prefilled with the exception of the "data" key:

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-7.png?raw=true "Import JSON")

3. Now:

   1. Paste the long string that we copied from the previous task (modifying the Certificate file) in between the double quotes of the "data" key.  Ensure that there are no errors (red squiggly lines or changes in color of the string of text would indicate something did not paste correctly).  
   
   2. Then click ***Send***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-8.png?raw=true "Import JSON")

4. In the bottom section of the window, we should see a JSON response indicating a Success:

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-11.png?raw=true "Import JSON")

5. We can further validate this by:

   1. Opening a web browser and navigating to ISE using https://198.18.133.27 (or using the bookmark) and login with ***username: `admin`*** and ***password: `C1sco12345`***

   2. Using the hamburger menu to navigate to 
   
      1. ***Administration*** then,
      
      2. Under ***System*** choose ***Certificates***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-12.png?raw=true "Import JSON")

   3. On the left, choose ***Trusted Certificates***

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-13.png?raw=true "Import JSON")

   4. From there, we should be able to scroll and see the certificate we uploaded

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-GUI-CSR-5.png?raw=true "Import JSON")

Now let's move on to generating a Certificate Signing Request

## Generating a Certificate Signing Request

***Complete the following tasks:***

1. Open up your Postman application again, and this time under

   1. ***Collections > lab-9-ise-automation-collection > ISE*** > ***Certificates*** select ***POST - Generate CSR***.  
   
   2. Notice in the ***Body*** section all keys/fields are already filled out for you here, with appropriate SanDNS name, SanIP, Subject, State, etc.  
   
   3. We simply need to click ***Send***

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-15.png?raw=true "Import JSON")

2. Here we receive our response success message:

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-16.png?raw=true "Import JSON")

3. Back in the ISE GUI, under ***Administration > System > Certificates*** on the left hand side

   1. Choose ***Certificate Signing Requests***.  
   
   2. Place a check next to the CSR in the table (should only be the one), and then...
   
   3. Choose ***Export***

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-17.png?raw=true "Import JSON")

4. Save the file in the Downloads folder, by default it will be named `iseMultiUse.pem`


## Signing the ISE CSR with Certificate Authority

***Complete the following tasks:***

1. Open the "Downloads" folder, right click on the .pem file that was just downloaded from ISE, and choose "Edit with Notepad++".  Thankfully, because Windows CertSrv can correctly parse carriage returns/line feeds, we do not need to modify this file.

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-GUI-CSR-10.png?raw=true "Import JSON")

2. Copy the entire contents of the Notepad++ file 


3. Open a new Chrome browser tab and enter the URL `http://198.18.133.1/certsrv` and log in with the credentials **username: `admin`** and **password: `C1sco12345`**

   ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-9.png?raw=true "Import JSON")

4. Within the Certificate Authority Web Site navigate the following:

   1. Click Request a Certificate

      ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-10b.png?raw=true "Import JSON")

   2. Click advanced certificate request

      ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-11.png?raw=true "Import JSON")

   3. To submit the Certificate Request paste the CSR as shown

      ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-12.png?raw=true "Import JSON")

   4. **Important** Select `Cisco Server Template` for the Certificate Template and click submit

      ![json](../../../ASSETS/LABS/AD/CERTS/Cert-CSR-13.png?raw=true "Import JSON")

   5. **Important** This time we'll actually select **Base 64 encoded** and then download the certificate

      ![json](../../../ASSETS/LABS/AD/CERTS/ISE-GUI-CSR-11.png?raw=true "Import JSON")

5. The certificate file should now be downloaded to the Downloads folder, by default it will be named `certnew.csr`, but you can save it as you wish.

## Cleaning Up the Signed ISE Certificate

Now that we have our signed ISE certificate, to use it within an API we have to do the same cleanup that we did previously.  Follow the steps in the [Cleaning Up The Windows Root CA Certificate](#cleaning-up-the-windows-root-ca-certificate) section, just using this newly downloaded file.

>[!NOTE]
>Keep this file open, we'll be using the text string from this in a couple tasks!

## Getting the CSR "ID"

In order to be able to "bind" the signed certificate we just downloaded to the appropriate Certificate Signing Request in ISE, we need to get the "id" of the CSR. Thankfully, since we only have a single CSR, this should be pretty easy!

>[!TIP]
>You may have noticed in the [Generating a Certificate Signing Request via API](#generating-a-certificate-signing-request-via-api) section above that the CSR "id" is included as part of the json response to the POST call.  In a production environment where you would be utilizing these API's in a programmatic way, you would likely be storing this "id" as a variable part of your code.  This section is simply demonstrating that you can *also* look up the "id" via an API should you need it.

***Complete the following tasks:***

1. In your Postman app, under ***Collections > lab-9-ise-automation-collection > ISE*** > ***Certificates*** select ***GET - CSR Listing***.  This GET request has an empty body (although you can use filters if you have multiple CSRs).  Simply press ***Send***

2. The return results should have the "id" that we need.  Copy this value from your Postman output.

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-19.png?raw=true "Import JSON")

## Binding the CSR with the Certificate

***Complete the following tasks:***

1. Open your Postman app, and now under ***Collections > lab-9-ise-automation-collection > ISE*** > ***Certificates*** 

      1. Select ***POST - Bind CSR***.  
      
      2. You will see that everything in the Body has been populated for you ***except*** the "id" value (which we just found in the previous task), and the "data" value (that we generated in the task before that).

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-18.png?raw=true "Import JSON")

2. For this step:

   1. Place your cursor in the "id" key and paste the id value that you copied from the previous task.  
   
   2. For the "data" key, as before, paste the entire certificate file string from the modified signed ISE certificate - looking out for any errors in the formatting (red squiggly lines, changes in text color, etc).  
   
   3. Then click ***Send***

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-20.png?raw=true "Import JSON")

3. And now we get a successful response.  ISE will now reboot - so wait ~5 minutes or so before attempting to login to the admin portal again.

   ![json](../../../ASSETS/LABS/AD/CERTS/ISE-API-CSR-21.png?raw=true "Import JSON")


Congrats, your ISE instance is now ...CERTIFIED!



>[!IMPORTANT]
>**Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

[**Go Back to ISE Certificates Overview**](./03-ISE-Certificates.md)

[**Next Section**](../ise-automation-2-integrations/01-ERS-API-Admin.md)

[**Return to ISE Automation Lab Overview**](../README.md)