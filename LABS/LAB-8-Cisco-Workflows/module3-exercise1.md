 
# Exercise 1 - Cisco Workflows Introduction

## Overview

Today, we’re going to walk you through the tool. No programming experience required. If you can use Microsoft Visio, you can use Workflows. We are going to start with the absolute basics and build layer upon layer until we get into some more complex concepts in the tooling. In this lab we are going to play with a simple sequence of events to build your confidence with Cisco Workflows.

> [!IMPORTANT] 
> **Preparation:** To use this lab, you should enable your Meraki org with Workflows Automation. If you have not had automation enabled for your Meraki account, please utilize the preparation steps in [module 1](./module1-preparation.md).

## General Information

* **[Overview](#overview)**
* **[Lab Exercise 1A](#lab-exercise-1a---i-need-some-sleep)** - I Need Some Sleep
* **[Lab Exercise 1B](#lab-exercise-1b---i-need-some-sleep-with-user-input)** - I Need Some Sleep (with user Input)
* **[Lab Exercise 1C](#lab-exercise-1c---need-some-sleep-and-im-bored)** - I Need Some Sleep and I’m Bored
* **[Lab Exercise 1D](#lab-exercise-1d---i-need-some-sleep-im-bored-and-how-many-people)** - I Need Some Sleep, I’m Bored, and How Many People?
* **[Lab Exercise 1E](#lab-exercise-1e---i-need-some-sleep-im-bored-and-im-taking-a-nap-based-on-the-crowd-size)** - I Need Some Sleep, I’m Bored, and I’m Taking a Nap Based on the Crowd Size
* **[Lab Exercise 1F](#lab-exercise-1f----http-post-example)** - HTTP POST Example
* **[Lab Exercise 1G](#lab-exercise-1g-bonus---cleanup-on-aisle-5)** - (Bonus): Cleanup on Aisle
* **[Appendix](./module6-advanced.md#advanced-information-and-resources)** - Useful Workflows Resources

## Lab Exercise 1A - I Need Some Sleep

I don’t know about you, but I’m allergic to “Hello World” (it makes my knees hurt). So, we’re going to start with something much more relaxing to gain an understanding of the most basic flow of the tool: Sleep.

1. Log into your Meraki account and navigate to Automation Workspace.

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE]
> If you do not see automation in the side menu, please utilize the preparation steps in [module 1](./module1-preparation.md).

</td></tr>
</table>
</div>

2. Click Create workflow.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow1.png" alt="Workflow Properties" style="width:100%; height:auto;">

3. Select Blank Custom Workflow. 

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow2.png" alt="Workflow Properties" style="width:60%; height:auto;">
 
4. Click Continue and enter a name of your choosing

   For example: Lab1a – Sleep 

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow3.png" alt="Workflow Properties" style="width:60%; height:auto;">

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE] 
> The Workflow with Automation Rule option (in the above screenshot) is for workflows triggered by Webhooks and other alternatives.

</td></tr>
</table>
</div>

5. Now, you will see a blank canvas ready for any automation you can think of. But before we get too crazy, let’s walk through the basics of the workflows editor.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow4.png" alt="Workflow Properties" style="width:100%; height:auto;">

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE]
> To Refresh your memory:
>
>### Adapters
>
>This panel contains the building blocks and individual functions you can add to a workflow. They are grouped under adapters representing the different controllers with which Workflows integrates, and the individual actions called “activities” are based on API calls to the integrated products, logic components, and other workflows. Think of an activity as an API call or function. Feel free to explore some of them by expanding and examining the activities that are provided “out of the box”. 
>
>Notice how many non-Meraki activities are supported right now, and this list isn’t even the exhaustive collection of activities Cisco has (Catalyst Center, Catalyst SD-WAN, Cisco FMC, ISE). There are also non-networking activities, such as Ansible and Terraform and Python. Scroll all the way to the bottom and note the Web Service activity that provides a generic REST API activity. If you need to automate something with a REST API – that is your catch-all for all things REST. I won’t list them all here, however, the main takeaway is that Cisco Workflows is a very powerful multi-domain automation and orchestration tool that your customers will already have.
>
>### Properties
>
>This panel includes the properties of the workflow itself as well as those for each activity on the workflow canvas. With a blank palette, the properties panel is where all the details and specifics of your automation are entered. Right now, with a blank canvas, the Properties space is for the overall workflow general configuration.  You can define variables for the workflow, and various other details we will get to soon.
>
>### Canvas
>
>This panel is where you build the structure and set the actions, order, and logic for a workflow. Drag-and-drop items from the Activities panel, including other workflows, here to add them to a workflow. You can drag and drop items on the canvas to change their location and order in the workflow. This is your space to build anything you wish.  
>
>### Validate and Run
>
>These are important concepts to pick up at the beginning of your Cisco Workflows journey.  Run executes your workflow, however, notice how it’s greyed out.  Cisco Workflows has a built in “gut check” that is required before a workflow is allowed to run. For example, what if the workflow designer forgot to configure a required part of a function or the larger workflow itself – rather than attempt and fail, this screen requires the designer to validate the workflow.  When the gut check is complete the workflow is allowed to run.  
>
>### More Actions
>
>This drop-down menu in the upper left corner contains the following options:
></br>*	View runs option allows the workflow designer to see the previous runs of the workflow and examine the input and output details of every activity
></br>*	Duplicate option creates a copy and is useful when you have a working workflow that you would like to modify while also keeping the original workflow intact
></br>*	Share option will allow you to export your workflow as a JSON file

</td></tr>
</table>
</div>

Labs can be exhausting, so let’s get some sleep.  

We have a few options to find the activity we are interested in:
*	Search for all adapters via the Search Activities field
*	Navigate directly to the activity (the Sleep activity is under the Core adapter)

6. Select your approach and drag sleep onto the canvas

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow5.png" alt="Workflow Properties" style="width:100%; height:auto;">

**NICE!**  You’re already designing automation – no coding required.

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE] 
> You may have noticed that the Properties space on the right has changed. This is because the sleep activity is highlighted.
> 
>If the workflow designer:
></br>
> * Clicks an activity, the Properties space is for that activity.
> * Clicks outside of an activity (anywhere in the **canvas** grey space), it will be the **workflow properties** space for the whole workflow.
>
>Expand Sleep configuration and you will be able to see which activity field requires a setting. Cisco is feeling generous right now (after all – this is the sales meeting and let’s celebrate) and is going to give us all a 3-second nap. Thank you, Cisco. 

</td></tr>
</table>
</div>

7. Enter 3 in the Sleep Interval field.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow6.png" alt="Workflow Properties" style="width:70%; height:auto;">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow7.png" alt="Workflow Properties" style="width:50%; height:auto;">

> [!IMPORTANT]
> While in canvas, click anywhere outside of the sleep activity. Note how the Properties space changed back to the general workflow parameters. Now validate the workflow so we can try to run it.

8. Click Validate. The Validate button should now be greyed out and the Run button will become available for the first time.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow8.png" alt="Workflow Properties" style="width:60%; height:auto;">

9. Click Run. 
   </br>How refreshing.  Nothing like a power nap!

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="33%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow9.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
<td valign="center" align="center" width="33%">

*…and then*	 

</td>
<td valign="top" align="center" width="33%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow10.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE]
> When an activity is running, it is blue. If it completes successfully, it turns green.  If it fails, it turns red.
>
> An important feature that customers will often look for is an audit log of every action and activity that was performed against the network (or beyond the network), so let’s check out the workflow’s run history.

</td></tr>
</table>
</div>

10. Navigate to Automation and then Run Monitoring

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow11.png" alt="Workflow Properties" style="width:100%; height:auto;">

You won’t see your workflow run until you enter your details.
 
11. In the Workflow Name field, type the first few characters of the name you gave your workflow earlier.

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow12.png" alt="Workflow Properties" style="width:100%; height:auto;">

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow13.png" alt="Workflow Properties" style="width:60%; height:auto;">
 
12. Click your workflow’s display name.</br> 
    The Run drawer opens on the right, which displays a summary of the workflow execution to help you quickly understand it at a high level. The summary includes information such as description, started by, started on, ended on, status, variables, and any error messages.
 
    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/CreateWorkflow14.png" alt="Workflow Properties" style="width:100%; height:auto;">

13. Click View run details in the bottom right.

Here you can inspect every detail about your workflow’s performance.  This view displays the detailed run data in a workflow editor environment. You can view what the workflow and its activities did, including which parts succeeded or failed (highlighted in red).  

The workflow properties section provides a summary of general information, response options, prompt response, variables, automation rules, targets, and output values from the workflow execution.  You can click each activity to show its properties, including output values such as JSON output which you may copy for further use.
Note that you can click the sleep activity and drill down into the details of that specific activity.  Click anywhere in the grey space to return to the general workflow run details (which will be more interesting shortly).

Congratulations!  You’re now officially a workflow automation and orchestration designer, and much more rested due to the generous nap Cisco just gave you.
 
## Lab Exercise 1B - I Need Some Sleep (with user Input)

While that was restful and awesome, it wasn’t very flexible.  Let’s create a workflow input for our sleep activity because you might want to abuse the system and take a 5 second nap next time or if you’re late for a customer call, reduce it to 2 seconds.

1. Click Modify in the top right to return to the workflow editor for this workflow.
   </br>The Properties space should show properties for the general workflow and not the sleep activity

2. Scroll down on the right side to the Variables section and click + Add Variable.
   
   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow1.png" alt="Workflow Properties" style="width:60%; height:auto;">

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="50%">

> [!NOTE] 
> ### Key Concepts
> 
> Data Type contains a few options, such as Secure String. Secure refers to things like passwords that you don’t want people looking over your shoulder to be able to see.
>
> Display Name is how you will reference this variable in the rest of your workflow. So, in this instance, we’ll call this “length of nap”. Display names should be in human-readable and capitalized form (no snake or camel case).
>
> Description is an optional field that can include information about the variable’s purpose.
>
> Scope is an important field. Click the drop-down menu to view various options. The options for Scope are:
>*	Input: Ask the workflow runner for information at the start
>*	Output: The desired outcome for the workflow
>*	Local: A variable used in the workflow and its value can change.  Example – You want to check how an IOS upgrade is progressing, but if there’s an issue you don’t want it to run infinitely. A local variable can bethe  number of times    you check on something before timing out of the workflow.
>*	Static: A value you want to hard code in your workflow but still have the freedom to change long term without having to tear apart your workflow.	 

</td>
<td valign="center" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow2.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

3. Select Input in the Scope field and click Save
4. Create another variable with the Scope set as Output and click Save.
   </br></br>At this point, you should have two new variables and your original sleep activity.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow3.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow4.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE] 
> Mapping variables is a very handy feature of Cisco Workflows. The basic concept is the use of the output of a step as the input for a future step.
>
>For example: 
>    1. Get a list of all your Meraki orgs and select the one you are interested in.
>    2. Get a list of networks in that org. Select the one you are interested in.
>    3. Get a list of devices in that network. Select the one you are interested in.
>    4. Get a list of ports on that device. Select the one you are interested in.

</td></tr>
</table>
</div>

5. Click the Sleep activity.
   </br>Watch how the Properties space changes to that activity.

   1. Keeping it simple for now, delete the 3 from the Sleep interval field, and then click the code icon on the right side of the field that looks like this (x).	 

      <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow5.png" alt="Workflow Properties" style="width:80%; height:auto;">

   2. Select Workflow, Input (variables), Length of Nap, and then click Save.	 

      <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow6.png" alt="Workflow Properties" style="width:65%; height:auto;">

   3. Your properties view should look like this.	 

      <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow7.png" alt="Workflow Properties" style="width:60%; height:auto;">

      How easy was that? A few clicks and you’ve replaced a hard coded value with a dynamic one. **NICE!**
      Let’s test it out. What’s the process to run a new or changed workflow?
      * The gut check: Validate it
      * If everything appears good: Run it
      
      I work hard for Cisco, so I’m going to abuse the system and sleep for a full six seconds. That’s how I roll. 

6. Enter the number 6 in the Input Variables field and click Run.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow8.png" alt="Workflow Properties" style="width:60%; height:auto;">
 
7. Click the Sleep activity when it turns green to verify the settings.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow9.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow10.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
</tr>
</table>
</div>

There it is: 6 seconds. Maybe it was a mistake for me to abuse the system in an environment that keeps detailed logs of every single action!

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="50%">

At this point, we’ve covered the concepts and the flow of how workflows are built.
*	Adapters and Activities
*	Drag and Drop
*	Configuring activities with variables and mappings
*	Validate the workflow
*	And, finally, run it

Now that we’ve had a few naps and are well rested, let’s do something more interesting.

</td>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/ModifyWorkflow11.png" alt="HTTP Request" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

## Lab Exercise 1C - Need Some Sleep and I’m Bored

There is a public and free API called bored-api. It simply returns JSON formatted suggestions of something to do if one is bored. We’re going to query this API for some activity suggestions, and in the process review what you’ve already learned and add a few more pieces.

1. Navigate to your Lab1a – Sleep workflow.
2. In the activities section, on the left of the screen, find the HTTP Request activity under the Web Service category. Drag it onto your workflow canvas ABOVE your sleep activity.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow1.png" alt="HTTP Request" style="width:100%; height:auto;">

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="50%">

> [!NOTE] 
> ### Key Concepts
> HTTP Request is the activity for all REST APIs. This is how you can add anything to workflows that have a REST API. Workflows isn’t just for Meraki or just for Cisco. The Workflows tool can be used to manage anything with a REST API (or other protocols, such as ssh).
> 
> The right side highlights the configuration details for this HTTP request. Click Target to expand and view the error.
> 
>   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow2.png" alt="HTTP Request" style="width:70%; height:auto;">
>
> Let’s discuss the flow of how we interact with any system from within Cisco Workflows. What is required to communicate with a REST API?
>
>*	Access: Most APIs require an authentication mechanism. This could be a user / password, a token, or an API key.
>*	Address: A REST API can be accessed via a URL or an IP address. You can also validate certification on the endpoint URL.
>*	Base URL (optional): Using Workflows you can add the base URL to the address once instead of having to type it during every interaction with Meraki. In this example the base URL is bold: api.meraki.com/api/v1.
>
> Even though we’re trying to find a solution to our boredom, we don’t have any of this set up yet the way Workflows is designed.  Bored-api doesn’t require authentication so we can skip that for now.  

</td>
</tr>
</table>
</div>

3. Navigate to Targets.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="50%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow3.png" alt="HTTP Request" style="width:60%; height:auto;">

</td>
<td valign="top" align="center" width="50%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow4.png" alt="HTTP Request" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

4. Click **+** New target (note that your screen may look different from this screenshot)
   </br></br>Let’s explore the Target types and how our friends in Meraki engineering have made it as easy as possible to onboard Cisco controllers (Catalyst Center, Catalyst SD-WAN, ISE, FMC, Meraki). However, they didn’t stop there. Service Now, Terraform, and Ansible are also accounted for.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow5.png" alt="HTTP Request" style="width:100%; height:auto;">

5. Select HTTP Endpoint.
   </br>Give this endpoint a name you’ll recognize adding a description is optional.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="100%">

> [!NOTE] 
> The bored-api falls under the generic REST endpoint that works for anything.

</td>
</tr>
</table>
</div>

6. Select True in the No Account Keys field

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="55%">

The No Account Keys field can be confusing. 
* If you want account keys select False.
* If you do NOT want account keys select True.

> [!NOTE]
> Ignore the Remote Keys field. That is for advanced use cases where you need to get behind a firewall with a TLS gateway.	 

</td>
<td valign="top" align="center" width="45%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow7.png" alt="HTTP Request" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

<div style="padding-left:0px;">
<table>
<tr>
<td valign="top" width="57%">

7. Select HTTP in the Protocol field.

8. Enter **`18.188.19.30`** in the Host/IP Address field.

9. Select **`8502`** in the Port field.

10. Enter **`/api`** in the Path field.

    This is the base path for all APIs.

    You do not need to check the **Disable server certificate validation** box for this activity. However, take note of this because SEs are often doing automation work against test servers or IPs that don’t have valid public certs.

</td>
<td valign="top" align="center" width="43%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow8.png" alt="HTTP Request" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>
 
11. Click Save.
    </br>Cisco Workflows verifies that the details you entered were correct. You should see Bored API as a valid target in your list of targets.

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow9.png" alt="HTTP Request" style="width:100%; height:auto;">

12. Navigate back to your Lab1 workflow canvas. 

    You should be able to select a target.  But before you do that, let’s understand that there are multiple places where a target can be configured. When possible, save yourself a few clicks and define a default target for the entire workflow.  

    * Option 1: Define it as the default target for the entire workflow.  This is a valid action for this lab.
    * Option 2: Override the default target for the workflow in an individual activity.  This is also a valid action for this lab.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="100%">

> [!TIP]
> You may be thinking that one probably wants to start the design process by defining authentication and targets before you even start on your workflow, and you’d be right to think this.  Since this is an introduction workshop, we’re adding the topics as they come up. Consequently, things might be slightly out of order for a seasoned workflow designer.

</td>
</tr>
</table>
</div>

13. Make sure you’re in the Properties space for the general workflow, scroll down, and define your default target.

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow10.png" alt="Workflow Properties" style="width:50%; height:auto;">

14. Click the HTTP Request so we can configure that activity. 

15. Select Use workflow target.

16. Expand HTTP Request and enter /random in the Relative URL field.

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow11.png" alt="Workflow Properties" style="width:50%; height:auto;">

    We’re ready to run our new and improved workflow.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" width="100%">

> [!TIP]
> Is the Run button greyed out?  Do you remember the step you have to do when you create or edit a workflow?  A “gutcheck” perhaps?

</td>
</tr>
</table>
</div>

17. If all went well, you should see something like this. By default, the run details are displayed in the panel on the right for the general workflow.

    <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow12.png" alt="HTTP Request" style="width:100%; height:auto;">

18. Click the HTTP Request to get the details of that activity.

    You might have to scroll down in the panel on the right to see the JSON result of our request for an activity.  Yours will likely be different from what is shown here.
 
     <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify2Workflow13.png" alt="Workflow Properties" style="width:60%; height:auto;">

    You know it’s a party when someone suggests that we: “activity”: “Learn about a distributed version control system such as Git”

    Congratulations! You just added a drag-and-drop solution for automating boredom! SCORE!
    
    Before we move on, note that the suggestions also include the number of participants. Quite often, these activity suggestions are for one person, but they can include many more. In the next section of this lab, we’re going to parse through the JSON and pull out that specific field.
 
## Lab Exercise 1D - I Need Some Sleep, I’m Bored, and How Many People?

Time to parse some JSON.

1. Click the **Modify** button to navigate back to the workflow editor canvas and find a core activity called JSONPath Query.

   Drag the activity onto your canvas below the HTTP Request (see screenshot). The JSONPath Query is a handy activity for parsing JSON and pulling out the exact field you need.  

   If it’s not already highlighted in the Properties and Configuration space, click your new JSONPath Query. Notice it wants two pieces of information: the source to run the query on and the JSONPath to query. First – let’s set the source JSON to the output of the HTTP Request we just created. Remember the puzzle piece for easy and fast mapping?

2. Click the code icon in the right corner of the Format box.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="38%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow1.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
<td valign="top" align="center" width="72%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow2.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
</tr>
</table>
</div>

3. In the Browse Variables window, select Activities, HTTP Request, and then Body.

   In REST terms, we want the body that was returned from that HTTP Request.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow3.png" alt="Workflow Properties" style="width:70%; height:auto;">

4. Click Save.
   </br>You’ve taken the output from step 1 and passed it as the input for step 2.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow4.png" alt="Workflow Properties" style="width:70%; height:auto;">

   Now we need to tell the system what field we are interested in extracting and using as a variable in a future workflow step.

5. Click + Add under JSONPath Queries.

<div style="padding-left:30px;">
<table>
<tr>
<td valign="top" width="38%">

> [!NOTE] 
> The title is plural. We can easily extract 2, 3, 5, or 22 variables vs just 1.

Review the output from the previous step.

</td>
<td valign="top" align="center" width="72%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow5.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

> [!NOTE]
> ## IMPORTANT CONCEPT: 
>If you have not done a lot of coding, this may not be intuitive. If you have done a little python coding and extracted entries from lists or dictionaries, this will become clear.
>
>**Quick dictionary example:**
>
>```
>>>> my_dictionary = {“color”:”red”,”size”:”large”,”cost”:”20 quid”}
>>>> print(my_dictionary[“size”])
>>>> large
>```
>
>The JSONPath query example was in the format of **[“size”]**.  That means you want to go through the dictionary and return the entry called “**size**”. In this example, we want to query **[“participants”]**.

6. Enter ["participants"] as the JSONPath Query.

7. Enter Participant Number as the Property Name.

8. Select Integer as the Property Type

   The Property Name field is what this item will be called in the Browse Variables window when mapping the output of this JSONPath Query activity.  

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow6.png" alt="Workflow Properties" style="width:50%; height:auto;"> 

> [!TIP]
> ## SAFETY TIP 
> This is simple JSON code. Things might be more complicated in the real world. It might be worth looking into some JSON 101 material **[here](../../TUTORIALS/JsonYamlXml.md)** if you want to get into more advanced workflow design.
>
>## Workflows Best Practice 
>For activity output variables, like Python activity or JSONPath, the names of the variables should be written in camel case, as they're considered code-related. That practice helps distinguish them from the workflow names. For example, deviceID vs. Device ID, and sortByDate vs. sort_by_date.

9. Let’s run it.  You remember all the steps.

   * Click the JSONPath Query activity to get the details of that activity on the right-hand side.
   * If you scroll down, you’ll see the source JSON and the resulting Path Query

     <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify3Workflow7.png" alt="Workflow Properties" style="width:60%; height:auto;">

**NICE!**  You’re hitting APIs and pulling out the exact data you want.  How many lines of code have you written?
</br>Now – Let’s get a little wacky in the last part of this lab. 

## Lab Exercise 1E - I Need Some Sleep, I’m Bored, and I’m Taking a Nap Based on the Crowd Size

Buckle up for this step. We’re going to illustrate a key concept, but in a wacky way.  We’re going to remove the user input for the length of our nap. Instead, we will sleep the same number of seconds as there are people suggested to take part in the activity.

Example: If there are five participants for the activity, we’re going to sleep for five seconds. If there are two participants, we’re going to sleep for two seconds.

This is intended to illustrate the nature of workflows.

**Use** the **output** of **`Step 1`**, **to drive** the **input** of **`Step 3`**. How, you ask? Through the awesome **mapping button**.  Let’s go!

1. Navigate back to your workflow editing canvas and delete the input variable from the general workflow configuration space and properties space.

   <img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify4Workflow1.png" alt="Workflow Properties" style="width:60%; height:auto;">

   When you delete that variable, the sleep activity went into an error state.  Why?  Because we just deleted the value of the length of our nap.

2. Fix it by clicking the sleep activity and map in the participants from the output of the JSONPath query.

<div style="padding-left:30px;">
<table>
<tr>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify4Workflow2.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
<td valign="top" align="center" width="50%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify4Workflow3.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
</tr>
</table>
</div>

## Lab Exercise 1F -  HTTP POST Example

Let’s do one more REST example before we move on.  HTTP Gets are great, but let’s submit some information.  In the presentation portion of this session, we talked about “The Prime Directive”, and we’re here to help you with customer engagements if you need it.  So, let’s do an HTTP POST and pull it all together.

<div style="padding-left:30px;">
<table>
<tr>
<td valign="top" width="38%">

1. Add another HTTP Request activity to the end of the workflow and configure it as follows.

</td>
<td valign="top" align="center" width="38%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify5Workflow1.png" alt="Workflow Properties" style="width:60%; height:auto;">

</td>
</tr>
</table>
</div>

<div style="padding-left:30px;">
<table>
<tr>
<td valign="top" width="38%">

> [!NOTE] 
> All fields must have a value in the Request Body field of your POST

```
Relative URL: /workflows-feedback
Method: Select POST
Request Body:
{
  "SE_Name": "…",
  "Customer_Name": "…",
  "Workflows_Use_Case": "…",
  "Interested_in_Workflows": "YES",
  "Prime_Directive": "YES",
  "Lab_Rating": "5 stars",
  "Feedback": "…"
}	 
```

</td>
<td valign="top" align="center" width="38%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify5Workflow2.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
</tr>
</table>
</div>

**EXCELLENT!**  We worked hard on these labs and appreciate any feedback you have that will make them even better.
 
## Lab Exercise 1G (Bonus) - Cleanup on Aisle 5

There are times when it helps other users of your workflows to more easily understand what the “flow” of the workflow is.  Do all your users understand what a JSONPath Query is?  Let’s do a few cleanup tasks just to make sure everything is nice and clean.

<div style="padding-left:30px;">
<table>
<tr>
<td valign="top" width="38%">

1. Navigate to your workflow canvas in the workflow editor and go through each step.

   Give it a more descriptive name.

</td>
<td valign="top" align="center" width="38%">

<img src="../../ASSETS/LABS/WORKFLOWS/EXERCISE1/Modify6Workflow1.png" alt="Workflow Properties" style="width:70%; height:auto;">

</td>
</tr>
</table>
</div>
     
**NICE!** Believe it or not, you’ve just covered nearly all the basic concepts of Cisco Workflows. You’re requesting JSON data from APIs, and parsing it for the specific items you’re interested in. You’re then using that data in future actions.

## Summary

Consider what you can already do.  Run a detailed report against Catalyst Center and Meraki.  Parse out the specifics of what you’re interested in.

What could this mean for your company, your team, your users, or you specifically?

Complete this sentence: “I could wait for Cisco to develop it or I could just… <your answer here>.”  

*	What if you could write a workflow to do that thing? That one missing feature you need to close the job?
*	Could the Workflows tool do that one missing feature, or that one tweak to a product outcome?
*	Can workflows buy you and Cisco time to fully develop and deliver a function or outcome?

We hope you enjoyed this workshop, and we look forward to seeing what you can do with Workflows. 

Now continue to the next exercise below for further training.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Exercise 2**](./module4-exercise2.md)

> [**Return to LAB Menu**](./README.md)