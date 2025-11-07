# ISE Integration with Active Directory (via API)

## Overview

Cisco Identity Services Engine (ISE) integrates with Active Directory (AD) to authenticate and authorize users and devices for secure network access. ISE supports multiple Active Directory domain joins, even without trust relationships between domains, allowing flexible multi-domain environments. It uses various authentication protocols supported by AD, such as EAP-FAST, PEAP, MS-CHAPv2, and EAP-TLS, to authenticate users and machines. During authentication, ISE verifies user status (e.g., disabled, locked out) and supports multiple username formats like SAM, UPN, and machine accounts. ISE also leverages AD group memberships and attributes for authorization policies, enabling dynamic network access control such as VLAN assignment or access control lists. Integration prerequisites include synchronized time via NTP, proper DNS configuration, and necessary AD permissions for machine account management. Additionally, ISE can gather session data passively from AD domain controllers to enhance identity visibility. This integration ensures secure, policy-driven network access based on AD identities and attributes.

## General Information

As you have likely noticed as we go through these lab modules, the lab utilizes a Windows Active Directory domain of `dcloud.cisco.com`.  This is spun up as part of the lab on the Windows AD Server (IP Address of 198.18.133.1) from the dCloud Session View.  Our ISE instance is preconfigured with the correct NTP and DNS configurations as well.  While viewing DNS configuration from the ISE GUI is not possible, from the Windows Jump Host you can open mRemoteNG, SSH into ISE, and run a `show running-config | include server` to see both the NTP and DNS configurations.  ISE <u>must</u> have its DNS pointed to a DNS Server that can find the domain you wish to join it to.  Thankfully, that is already setup for us!

In this lab module, we wont cover <u>every</u> Active-Directory-related API that ISE can utilize -- just some of the most common ones.  As always, we encourage you to check out the <a href="https://developer.cisco.com/docs/identity-services-engine/latest/ers-open-api-ers-open-api/">**Cisco ISE API Documentation**</a> for a full list of AD-related APIs.

>[!WARNING]
>You must have completed [**ERS API Admin**](./01-ERS-API-Admin) from this lab section, as well as the [**PKI Infrastructure**](../ise-automation-1-certificates/01-PKI-Infrastructure.md) and one of the [**ISE Certificates**](../ise-automation-1-certificates/03-ISE-Certificates.md) modules from Section 1 before completing this lab module.

>[!NOTE]
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host. <br><br>
>:mega: These tasks assume you have already imported and setup the collection and environment from the [***03b-ISE-API***](../ise-automation-1-certificates/03b-ISE-API.md) module.

This lab module consists of the following tasks:

1. [**Creating an Active Directory Join Point**](#creating-an-active-directory-join-point)
2. [**Getting an Join Point ID**](#getting-an-ad-join-point-id)
3. [**Joining the AD Join Point**](#joining-the-ad-join-point)
4. [**Getting a List of Users**](#getting-a-list-of-users)
5. [**Getting a List of Domain Groups**](#getting-a-list-of-domain-groups)

## Creating an Active Directory Join Point

***Complete the following tasks:***

1. From your Postman app, open ***lab-9-ise-automation-collection > ISE > Active Directory*** and select ***POST - AD Create Join Point***

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-1.png?raw=true "Import JSON")

2. In the ***Body*** of this POST request, we have prefilled the most very basic info needed to successfully create this Join Point. (Although there are many, many settings you can also configure with this POST request, they are beyond the scope of this lab module.). 

    1. Here we can see that we're providing a ***domain***, a ***name*** for the join point, and a ***description***

    2. Click ***Send***

        ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-2.png?raw=true "Import JSON")

3. For this POST request, we actually don't get a JSON response indicating a success.  Only a ***Status Code*** of `201 Created`

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-3.png?raw=true "Import JSON")

>[!NOTE]
>We <u>could</u> validate that our Join Point was created from the GUI (under ***Administration*** > ***Identity Management*** > ***External Identity Sources*** and expanding the ***Active Directory***), but why don't we validate using the API instead? 

## Getting an AD Join Point ID

***Complete the following tasks:***

1. From your Postman app, open ***lab-9-ise-automation collection > ISE > Active Directory*** and select ***GET - AD Join Points***

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-4.png?raw=true "Import JSON")

2. This GET request does not require anything in the Body.  

    1. Click ***Send***

    2. Here we can see that our Join Point was indeed successfully created from the last section.  Copy the `id` field, as we'll need it in the next task!

        ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-5.png?raw=true "Import JSON")

## Joining the AD Join Point

***Complete the following tasks:***

1. From your Postman app, open ***lab-9-ise-automation collection > ISE > Active Directory*** and select ***PUT - AD Join a Join Point by ID***

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-6.png?raw=true "Import JSON")

2. In our API calls up to this point, there is typically a field within the ***Body*** of a request that we would copy/paste in an `id`.  However, in many of the requests dealing with Active Directory (including this one), note that the `id` actually goes in the URL of the request itself.  

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-7.png?raw=true "Import JSON")


3. Next:
    
    1. Paste the ID value that you copied from the "Getting an AD Join Point ID" section above, replacing the entirety of the `{{join-point-id}}` field.  The rest of the Body has already been filled in with the required values.

        > [!IMPORTANT]
        > Make sure you leave the `/join` on the end!

    2. Click ***Send***

    3. For this API Call, we do not expect a JSON response.  A successful request here should yield a ***Status: 204 No Content***

        ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-8.png?raw=true "Import JSON")

4. We can validate that the ISE Node has joined our join point via the GUI.

    1. From a web browser, navigate to the ISE GUI via https://198.18.133.27 (or using the bookmark) and login with ***username: `admin`*** and ***password: `C1sco12345`***

    2. Under the hamburger menu:
    
        1. Select ***Administration*** 
        
        2. Then under "Identity Management" select ***External Identity Sources***

            ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-9.png?raw=true "Import JSON")

    3. On the left hand side under ***Active Directory***:

        1. Select our ***DCLOUD-Active-Directory*** that we created

        2. Note that the Status should read ***Operational***

            ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-10.png?raw=true "Import JSON")


## Getting a List of Users

***Complete the following tasks:***

1. From the Postman app, open ***lab-9-ise-automation collection > ISE > Active Directory*** and select ***PUT - AD List of Domain Users***

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-11.png?raw=true "Import JSON")

2. From here:

    1. We need to provide the Join Point ID as part of the URL

    2. Note the basic info provided as part of the Body.  In particular, note that the request is asking for the name of the <u>Domain</u> here, ***NOT*** the name of the <u>Join Point</u>.

        > [!TIP]
        > As in many of these examples, this is the most basic of requests.  There are many different filtering options available!  As always, consult the API Documentation!

    3. Click ***Send***

    4. Our response should be a JSON list of all of our Active Directory Users:

        ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-12.png?raw=true "Import JSON")


## Getting a List of Domain Groups

The API for getting a list of User Groups from ISE is almost identical to getting a list of Users - and is likely going to be even more helpful; as, in general, policies are going to be based on User Groups rather than individual Users.

***Complete the following tasks:***

1. From the Postman app, open ***lab-9-ise-automation collection > ISE > Active Directory*** and select ***PUT - AD List of Domain Groups***

    ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-13.png?raw=true "Import JSON")

2. From here:

    1. We need to provide the Join Point ID as part of the URL

    2. Note the basic info provided as part of the Body.  AND that the request is asking for the name of the <u>Domain</u> here, ***NOT*** the name of the <u>Join Point</u>.

    3. Click ***Send***

    4. Our response should be a JSON list of all of our Active Directory Domain Groups:

        ![json](../../../ASSETS/LABS/ISE/ISE-AD-API-14.png?raw=true "Import JSON")


Congrats!  Our ISE node is integrated with our DCLOUD Active Directory, and ready for use creating access policies based on our users!

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 


[**Catalyst Center/ISE Integration**](./03-Catalyst-Center.md)

[**Return to ISE Automation Lab Overview**](../README.md)