# Custom Endpoint Attribute Creation

## Overview

Cisco ISE uses Custom Endpoint Attributes to enable iPSK (Individual Pre-Shared Key) policies by allowing administrators to create and assign specific attributes to endpoints, which can then be used in authorization and profiling policies. Here is a brief summary of the process:

- Creation of Custom Attributes: Administrators create custom endpoint attributes in Cisco ISE under Administration > Identity Management > Settings > Endpoint Custom Attributes. These attributes can be of various data types such as String, Int, Boolean, etc.

- Assigning Attribute Values: Values for these custom attributes are assigned to endpoints via the Context Visibility > Endpoints page, where specific endpoints can be edited to include the custom attribute values.

- Using Attributes in Policies: These custom attributes are then used in authorization policies to enforce iPSK policies. For example, policies can be created to allow or restrict network access based on the custom attribute values assigned to endpoints.

- Profiling and Enforcement: Custom attributes can also be integrated into profiling policies to better identify and classify endpoints, enabling more granular control and enforcement of iPSK policies.


## General Information

Unfortunately, on the version of ISE we're running in this lab, the creation of Custom Endpoint Attributes via API is not supported, so we need to do this part via the GUI.

>[!NOTE]
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host. <br><br>

## Configuring a Custom Endpoint Attribute

Complete the following tasks:

1. From a web browser, navigate to Cisco ISE via https://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`***

2. From the hamburger menu, in the top left:

    1. Select ***Administrator*** then

    2. Under ***Identity Management*** select ***Settings***

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-01.png?raw=true "Import JSON")

3. On the left hand side:

    1. Select ***Endpoint Custom Attributes*** then

    2. Under the "Endpoint Custom Attributes" section, in the Attribute Name field type `iPSK` and set type to `String`

    3. Click ***Save***

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-02.png?raw=true "Import JSON")


Now our Custom Endpoint Attribute is ready to be used!  We will reference this attribute as part of our Policy Postman Collection Run!

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Next Section**](./03-Policy-Configurations-API.md)

> [**Return to ISE Automation Lab Overview**](../README.md)