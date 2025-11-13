# ISE ERS API Admin

## Overview

In Cisco ISE, there are two "collections" of APIs -- ERS based and Open API based.  The key differences between ERS APIs and Open APIs within Cisco ISE are as follows: ERS (External RESTful Services) APIs are REST APIs that support basic authentication, and are primarily used for managing Cisco ISE nodes with read/write or read-only access depending on user roles.  On the other hand, Open APIs are newer REST APIs introduced from Cisco ISE Release 3.1, based on the OpenAPI specification, and routed through the Cisco ISE API Gateway for better security and traffic management. Open APIs cover a broader range of functionalities including repository management, backup and restore, certificates, policies, licensing, and system settings. If you've completed the [***03b-ISE-API***](../ise-automation-1-certificates/03b-ISE-API.md) module from the "ise-automation-1-certificates" section, you were using the Open API to do those tasks.  Both API types require appropriate user privileges and authentication configurations, but Open APIs follow a more modern, standardized approach for API development and integration.

To get an idea of what types of API endpoints exist as ERS based vs. Open API based, visit the <a href="https://developer.cisco.com/docs/identity-services-engine/latest/ers-open-api-ers-open-api/">**Cisco ISE API Documentation**</a>

## General Information

While Open APIs are what we are going to use for a large number of tasks/modules within this ISE Lab, there are certain features - such as creating Join Points for External Identity Sources and then <u>joining</u> those join points - are **only** available using ERS-based APIs.  To use ERS-based APIs, an administrator account must be added to the **ERS Admin** Admin Group.  This brings us to a (purposeful) limitation within ISE, which is that the default "admin" account that we have been using thus far can <u>only</u> be added to a single Admin Group - **Super Users**.  This means that we will have to create a new Admin User and assign them to the **ERS Admin** role.  This task can only be performed via the ISE Web GUI.

>[!NOTE]
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps may reference) using the Windows Jump Host. 


This lab module consists of the following tasks:

1. [***Creating and Assigning an ERS Admin***](#creating-and-assigning-an-ers-admin)
2. [***Validating the ERS Admin via API***](#validating-the-ers-admin-via-api)


## Creating and Assigning an ERS Admin

***Complete the following tasks:***

1. Open a web browser and navigate to ISE using the URL https://198.18.133.27 (or use the bookmark if you're on the Windows Jump Host) and login with ***username: `admin`*** and ***password: `C1sco12345`***

2. From the hamburger menu in the top left:

    1. Select ***Administration*** and then

    2. Under "System" select ***Admin Access***

        ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-1.png?raw=true "Import JSON")

3. On the left menu:

    1. Select ***Administrators*** then

    2. ***Admin Users***

    3. ***Add***

        ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-2.png?raw=true "Import JSON")

4. Choose ***Create an admin user***

5. For the purposes of this lab, the only fields we really care about are as follows:

    1. ***Name*** = `ers_admin`

    2. ***Password*** = `C1sco12345` (input into the Re-Enter field as well)

    3. In the ***Admin Groups*** section, select ***ERS Admin*** from the drop down box.

    4. Select ***Submit***

        ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-3.png?raw=true "Import JSON")

6. The ***ers_admin*** user should now show up on the list of administrators, with Admin Groups "ERS Admin"

    ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-4.png?raw=true "Import JSON")

Let's validate that this user is properly configured by attempting a basic ERS-based API call.

## Validating the ERS Admin via API

>[!NOTE]
>These tasks assume you have already imported and setup the collection and environment from the [***03b-ISE-API***](../ise-automation-1-certificates/03b-ISE-API.md) module.

1. From your Postman app, open ***lab-9-ise-automation-collection > ISE > User Management*** and select ***GET - Admin Users List***

    ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-5.png?raw=true "Import JSON")

2. This "GET - Admin Users List*** - as its name suggests, gets a list of all the Administrator Users in ISE.  This GET request itself utilizes the ERS-based APIs.  Before we run this GET request:

    1. Click on the ***Authorization*** tab, and
    
    2. Note that the variables we're calling from the ***lab-9-ise-automation-environment*** are `{{ers_admin}}` and `{{ers_password}}`.  While the collection/environment in this (and future) labs are prebuilt for you with the correct environment variables input into their proper place, its important to note that any time you want to use an ERS-based API in your own environments, you must use the account that is setup in ISE for the ***ERS Admin*** group.

        ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-6.png?raw=true "Import JSON")

3. From here:

    1. Click ***Send***

    2. Our response should show a list of ISE Administrators, including both the `admin` and `ers_admin` accounts:

        ![json](../../../ASSETS/LABS/ISE/ISE-ERS-Admin-7.png?raw=true "Import JSON")

Congratulations, we are now able to utilize ERS-based API's in our ISE environment!

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**ISE Active Directory Integration**](./02-Active-Directory.md)

> [**Return to ISE Automation Lab Overview**](../README.md)