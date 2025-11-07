# ISE Integration with Catalyst Center (via API)

## Overview

Up to this point in our ISE Automation journey, we've generally performed API calls one at a time.  However, if you're a seasoned Postman professional - you may know that you can run a group of API calls as a "Collection", which allow us to:

1. Make an API call, and capture the resulting output
2. Script Postman to take some of the captured output and set it as an environment variable for future use, then
3. Move on to another API call, using the environment variable from that previous API output as the INPUT for this call

That is what we're going to do in this lab!  We simply have to run a collection once, and it should configure our Catalyst Center <--> ISE integration for us in one fell swoop.

## General Information

>[!WARNING]
>You must have completed the following modules prior to continuing:

1. [**PKI Infrastructure**](../ise-automation-1-certificates/01-PKI-Infrastructure.md) from Lab 9 - Section 1 "Certificates"
2. [**Catalyst Center Certificate**](../ise-automation-1-certificates/02-Catatlyst-Center.md) from Lab 9 - Section 1 "Certificates"
3. [**ISE Certificates**](../ise-automation-1-certificates/03-ISE-Certificates.md) from Lab 9 - Section 1 "Certificates" (either via GUI or API)


>[!NOTE]
>:mega: If you have already completed the integration between Catalyst Center and ISE as part of the [Module 1 - PnP Prep](../../LAB-1-Wired-Automation/module1-pnpprep.md) from Lab 1, you may skip this module.<br><br>
>:mega: While many of these tasks can be completed with your own device, the screenshots taken (and many of the steps reference) using the Windows Jump Host. <br><br>

This module consists of the following tasks:

1. [**Running the CATCENTER INTEGRATION as a Collection**](#running-the-catcenter-integration-as-a-collection)
2. [**What is Happening Behind the Scenes**](#what-is-happening-behind-the-scenes)
3. [**Validate Catalyst Center and ISE Integration**](#validate-catalyst-center-and-ise-integration)

## Running the CATCENTER INTEGRATION as a Collection

***Complete the following tasks:***

1. From your Postman app, open ***lab-9-ise-automation-collection > ISE > CATCENTER INTEGRATION***

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-01.png?raw=true "Import JSON")

   Here, you'll notice that we've prefaced each API call with a number (1, 2, 3, etc.) corresponding to the order in which we want these APIs to be run.

   >[!TIP]
   >Postman does not, by default, automatically arrange the order of APIs in a collection based on numerical order (or alphabetical, for that matter).  You can arrange them any way you want just by dragging and dropping them.  But the numbers do serve as a good way to highlight the order in a collection and is considered best practice when working on a collection with a larger team.

2. Hover your mouse over the **CATCENTER INTEGRATION** folder name and

   1. Select the three dots

   2. Choose "Run Folder"

   >[!NOTE]
   >Depending on what version of Postman you are running, this may just say "Run"

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-02.png?raw=true "Import JSON")

3. From here:

   1. Leave all of the APIs selected, since we're going to run all of them

   2. Set the **Delay** to 10000 ms (ie: 10 seconds)

      >[!TIP]
      >In a production environment you probably wouldn't need to set a delay of this magnitude.  But as this is a lab environment, the hardware resources we've allocated to these devices wouldn't normally be considered production-ready - so, much like your aging relatives at a family reunion, giving them a bit of time to process a task before moving on to the next makes things go more smoothly. 

   3. Click the orange **Run lab-9-ise etc...etc..** button

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-03.png?raw=true "Import JSON")

4. Once all of the APIs ran, we should see them in a list with green 20x codes next to them as per the screenshot below:

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-04.png?raw=true "Import JSON")

## What is Happening Behind the Scenes

So what is <i>actually</i> happening here?  Well, we could just let you appreciate the magic that is Postman collection runs and proceed on to the next part of the lab -- but we also plan on using this same mechanism to deploy some of our other labs going forward.  So if you're someone who already knows how this works, by all means, skip ahead - otherwise, let's take a deeper look at this API call by API call.  

### 1. PUT - Set ISE pxGrid AutoApprove

This step directly coordinates to the "Prepare ISE for Catalyst Center Integration" step from the [**03a-Catalyst-Center-GUI**](./03a-Catalyst-Center-GUI.md) module.  Essentially, it configures the ISE pxGrid settings to automatically approve/accept pxGrid integration requests based on a password.

### 2. POST - Get CatC Auth Token

As you go through your automation journey, you'll quickly realize that different systems authenticate their API requests in different ways.  ISE, for example, will authenticate all calls based solely on the username/password information sent to it in the header of the API call itself.  Cisco SD-WAN, meanwhile, requires both username/password <b>AND</b> a session ID (essentially a Cookie).  Catalyst Center requires username/password, a session ID, <b><u><i>AND</i></u></b> a "token" before making any other API calls.  This step is essentially us using an API to get the token we need to submit further API calls to Catalyst Center.  Its an empty Body API "POST" request against https://{{catalyst center IP address}}/api/system/v1/auth/token endpoint.  If we run this POST request by itself, you see we get a JSON response with a key of "Token" and a big long line of jibberish that is the Token value itself: 

![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-05.png?raw=true "Import JSON")

Where things get interesting is if you click on:

   1. ***Scripts*** section

      >[!NOTE]
      >Depending on what version of Postman you're running, this section might be called "Tests" for some reason

   2. ***Post Response***

   3. Here we see some basic JavaScript:

      ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-06.png?raw=true "Import JSON")

Essentially, we're telling Postman to run the API POST request, but once it receives a response (hence the "Post-response" section), run this section of code:

```
var data = pm.response.json();
```

...which means we're creating a variable called "data" and inside of it we're putting in the entire JSON response we get from the API call.  Then...

```
pm.environment.set("catc-token", data.Token);
```

...which means that we're setting an environment variable called "catc-token" and the value we're giving it is from the variable "data", specifically, the value associated with the key called "Token".

Sure enough, if you open your ***Environments > lab-9-ise-automation-environment***, you'll see a variable called "catc-token" and the long string value that matches what we saw earlier.

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-07.png?raw=true "Import JSON")

Now we can use this token in our next API call on the list!

### 3. POST - Add ISE Policy Server to CatC

From your Postman app:

1. Go back to ***Collections > lab-9-ise-automation-collection > ISE > CATCENTER INTEGRATION*** and open the **POST - 3. Add ISE Policy Server to CatC** API call

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-08.png?raw=true "Import JSON")

2. Click on the **Headers** tab, and note that we've setup a header item called `x-auth-token` with which we've assigned the variable value from `catc-token`

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-09.png?raw=true "Import JSON")

   >[!IMPORTANT]
   >While "catc-token" is a variable name that we just came up with for the purposes of using within this Postman lab (<i>and we challenge you to come up with a better name, we'll wait</i> :sunglasses:), the Header name of "x-auth-token" is very much something that is set in stone from the developers and standards bodies that set the rules for API header formatting.  This applies to all Header key names.  Naming these something else other than what the developer intended will <u>not</u> work.  Always consult the documentation for your application to determine what headers are needed, and how to name them.

Alright so now that we know how we took the "catc-token" from Step 2. and put it as a variable into the "x-auth-token" in our Step 3 API call, what does this API actually DO?  If you reference the [**03a-Catalyst-Center-GUI**](./03a-Catalyst-Center-GUI.md) module, this step directly correlates to **Integrate ISE and Catalyst Center** Section, Steps 1 through 4. While you're there, note Step 5 - which is to accept the certificate that ISE presents to Catalyst Center.  Our next two API calls tackle this.

### 4. GET - Get ISE instanceUuid from CatC

Now that we've added the ISE configuration to Catalyst Center, it sits in kind of a "limbo" state until we accept the certificate that ISE presents to Catalyst Center.  Since Catalyst Center supports more than one ISE instance at a time, we need to obtain the Universal Unique IDentifier (UUID) of the ISE instance we want to accept the certificate from - which is what we're doing with this API call.  If you open the Scripts (or "Tests") section of the API, you'll see we're doing something very similar to what we did with the Catalyst Center authentication token.  We capture the JSON response and put it into a temporary variable called "data", and then set an environment variable (in this case, one named `ise-uuid-catc`) with the value of the "instanceUuid" in the JSON response.

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-10.png?raw=true "Import JSON")

By now you probably know where we're going with this - that `ise-uuid-catc` variable is going to be used in our next API call!

### 5. PUT - Accept ISE Cert on CatC

For this API call, the variable from the last step is actually inserted as part of the API endpoint URL.  The body of the API simply setting the `isCertAcceptedByUser` value to `true`:

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-11.png?raw=true "Import JSON")


## Validate Catalyst Center and ISE Integration

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon and navigate to the System > Settings menu item.

   ![json](../../../ASSETS/LABS/CATC/catc-menu-systemsettings.png?raw=true "Import JSON")

2. Within the System Settings page navigate down the list on the left and select the Authentication and Policy Server section.

   ![json](../../../ASSETS/LABS/CATC/catc-systemsettings-aaa.png?raw=true "Import JSON")

3. Here we should see that our ISE server is added and has a state of "ACTIVE"

   ![json](../../../ASSETS/LABS/ISE/ISE-CATC-INT-12.png?raw=true "Import JSON")


Congrats!  Our ISE node is integrated with Catalyst Center, and ready to apply policy!

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

Continue to:

[**Next Section**](../ise-automation-3-policy/01-Lab-Client-Orientation.md)

[**Return to ISE Automation Lab Overview**](../README.md)