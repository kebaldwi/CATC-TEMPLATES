# Configuring ISE Policies (via API)

## Overview

Congratulations on making it to this lab module!  This is the culmination of all of our efforts thus far.  Now we get to configure our policies so that ISE can actually <b><i><u>do</u></i></b> what its mean to do in our environment.  ISE policies enable network access control by defining rules that authenticate and authorize users and devices attempting to connect to the network. These policies dynamically assign access permissions based on attributes such as user identity, device type, location, and security posture, allowing for scalable and consistent enforcement of security across wired, wireless, and guest networks. ISE policies also facilitate segmentation and adaptive access by integrating with technologies like Security Group Tags (SGTs) to simplify and automate network security management.


## General Information

While ISE does have many, many advanced capabilities (posturing, profiling, SGT assignment, etc.) this lab will focus on fairly basic policies correlated to the various WLAN configurations found in [**Lab 2 - Wireless Automation**](../../LAB-2-Wireless-Automation/module2-wlans.md).

>[!WARNING]
>You must have completed ***ALL*** Lab 9 Modules up to this point prior to attempting this lab

>[!NOTE]
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host. <br><br>

This lab module consists of the following tasks:

1. [***Collection Run #1 - Prerequisites and Standalone Requests***](#collection-run-1---prerequisites-and-standalone-requests)
2. [***Collection Run #2 - Creation of Authentication Rules***](#collection-run-2---creation-of-authentication-rules)
3. [***Collection Run #3 - Creation of EAP Authorization Rules***](#collection-run-3---creation-of-eap-authorization-rules)
4. [***Validating Policy Creation***](#validating-policy-creation)

## Collection Run #1 - Prerequisites and Standalone Requests

As we demonstrated in the [***Catalyst Center Integration via API Module***](../ise-automation-2-integrations/03b-Catalyst-Center-API.md), we can use Postman "Collections" to run multiple Postman Requests in sequence, often taking JSON output from one request and using it as variable input into another.  We will be doing the same for this task.

1. From your Postman app, navigate to ***Collections > lab-9-ise-automation-collection > ISE*** and expand the "POLICY" folder:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-03.png?raw=true "Import JSON")

    For this Collection Run #1, we are only going to run requests 1 thru 8.  Feel free to poke around in each of the requests to get an idea of what each of them is doing, but from a high level here is what requests 1 thru 8 accomplish:

    1. (Requests 1-3) Pull down the Active Directory groups and add "Domain Users" and "Domain Computers" as usable objects in our Authentication (AuthN) and Authorization (AuthZ) rules - for EAP-TTLS/EAP-PEAP and EAP-TLS, respectively.

    2. (Request 4) - Creates an endpoint record in the "Internal Endpoints" database based on the MAC address of the LAB PC you provided in the [***Lab Client Orientation***](01-Lab-Client-Orientation.md) module earlier.  It also configures it with an iPSK password of "Cisco6789"

    3. (Request 5) - Creates the iPSK Authorization Profile that the iPSK Authorization Rule will use to lookup the Lab PC by MAC address and validate that it sent the correct iPSK key

    4. (Request 6) - Creates the Certificate Authentication Profile we'll need for our EAP-TLS rule

    5. (Request 7-8) - Creates a "parent policy" called "DCLOUD-LAB-POLICY", and because our iPSK Authorization policy only has one condition (as opposed to our EAP policies which will have two) -- we just included its configuration as part of this first run.

2. Hover your mouse over the "POLICY" folder, select the three dots and click "Run"

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-04.png?raw=true "Import JSON")

3. From the Run Sequence Screen

    1. <b><i><u>DESELECT</u></i></b> items #9 and #10

    2. Set the run Delay to 10000 ms

    3. Click the orange Run button

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-05.png?raw=true "Import JSON")

4. Once the Runner completes, you should see each item with a ***Green*** status code.  If not, please consult your lab proctor before continuing on to the next task!

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-06.png?raw=true "Import JSON")


## Collection Run #2 - Creation of Authentication Rules

In this collection run, we are going to introduce a Postman functionality you may or may not be familiar with - which is to use the Run Sequence to iterate through a request multiple times, using data from a .CSV file to populate variables differently for different iterations.

For this task, you will need to download the following file:

<p><a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/DOCS/Lab9-Authentication-Rules.csv">⬇︎Lab 9 Authentication Rules⬇︎</a></p>

Once you have that saved to your PC running Postman, complete the following tasks:

1. From your Postman app, navigate to ***Collections > lab-9-ise-automation-collection > ISE*** and expand the "POLICY" folder:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-03.png?raw=true "Import JSON")

2. Hover your mouse over the "POLICY" folder, select the three dots and click "Run"

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-04.png?raw=true "Import JSON")

3. This time, DESELECT all requests except for #9:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-07.png?raw=true "Import JSON")

4. On the right hand side of the Runner, under the "Run configuration" section, there is a "Test data file", choose ***Select File***

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-08.png?raw=true "Import JSON")

5. From the Open window, navigate to where you saved the ***Lab9-Authentication-Rules.csv*** file and open it.

6. At this window, since we are in a lab environment, choose "Use locally"

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-09.png?raw=true "Import JSON")

7. Back to the Runner screen:

    1. Note that the iterations has change from 1 to 3, correlating to the 3 rows of data in our CSV file for the 3 authentication rules we're about to setup

    2. For this Collection Run, set the delay to 20000 (again, this is just because we're running on lab gear - but also we're using the same API call 3 times here, with 3 different inputs, so best to give it time between runs to process)

    3. You should see your "Lab9-Authentication-Rules" file noted here

    4. Click the orange Run button

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-10.png?raw=true "Import JSON")

8.  As before, once the run completes all items should have a Green response.  If you note anything different, please consult your lab proctor.


## Collection Run #3 - Creation of EAP Authorization Rules

Now that we have our Authentication rules setup, its time to configure our Authorization rules.  We'll be doing very similar steps to the last task.

First, download the following file:

<p><a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/DOCS/Lab9-Authorization-Rules.csv">⬇︎Lab 9 Authorization Rules⬇︎</a></p>

1. From your Postman app, navigate to ***Collections > lab-9-ise-automation-collection > ISE*** and expand the "POLICY" folder:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-03.png?raw=true "Import JSON")

2. Hover your mouse over the "POLICY" folder, select the three dots and click "Run"

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-04.png?raw=true "Import JSON")

3. This time, DESELECT all requests except for #10:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-11.png?raw=true "Import JSON")

4. On the right hand side of the Runner, under the "Run configuration" section, there is a "Test data file", choose ***Select File***

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-08.png?raw=true "Import JSON")

5. From the Open window, navigate to where you saved the ***Lab9-Authorization-Rules.csv*** file and open it.

6. At this window, since we are in a lab environment, choose "Use locally"

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-09.png?raw=true "Import JSON")

7. Back on the Runner screen, as before, set Delay to 20000 and click the orange "Run" button

    >[!NOTE]
    >Because we already created our iPSK Authorization rule as part of the Collection Run #1 task above, the iteration count here will be 2, not 3.

8. As before, once the run completes all items should have a Green response.  If you note anything different, please consult your lab proctor.

## Validating Policy Creation

Assuming all of your API Collection Runs returned Green statuses, (and/or you worked with the proctor to troubleshoot any issues), we can now hop into the ISE GUI to ensure that our policies got configured correctly.

1. From your workstation/jumpbox, open Chrome browser and navigate ISE via http://198.18.133.27 and login with ***username: `admin`*** and ***password: `C1sco12345`*** if prompted

2. From the hamburger menu in the top left:

    1. Select ***Policy***, then

    2. ***Policy Sets***

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-12.png?raw=true "Import JSON")

3. On this screen we should see:

    1. Our "DCLOUD-LAB-POLICY", with Conditions of `DEVICE-Device Type EQUALS All Device Types` and under "Allowed Protocols" `Default Network Access`

    2. Click the blue arrow to expand the policy

        ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-13.png?raw=true "Import JSON")

4. Click on ***Authentication Policy (4)*** to expand it

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-14.png?raw=true "Import JSON")

5. Here, we see the three Authentication Policies we created along with the default policy.

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-15.png?raw=true "Import JSON")

    >[!NOTE]
    >Our custom policies were created in a "disabled" state by default so that you can selectively enable which policies you want during your testing, since we can really only test with 1 Lab PC at a time due to having a single USB Wireless Adapter.

    Please ensure your policies match the above image.

6. Similarly, if we scroll down and expand the ***Authorization Policy (4)*** section, we should see as below:

    ![json](../../../ASSETS/LABS/ISE/ISE-POLICY-16.png?raw=true "Import JSON")

Congrats, now we're ready to start testing!

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to iPSK Testing**](../ise-automation-4-testing/01-iPSK-Testing.md)

> [**Return to ISE Automation Lab Overview**](../README.md)