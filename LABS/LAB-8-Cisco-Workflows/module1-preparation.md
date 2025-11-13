# Preparation - Getting Started Guide

## Module Overview

You must have a Meraki Account that has full Organizational Administrator permissions for an Organization that is hosted in NORTH AMERICA to be able to complete this lab. 

If you already have an account with full Organizational Administrator permissions on an account in North America, you will only need to complete [Step 3](#step-3---enable-automate-workflows) and Enable Automate Workflows.

If you do not, complete all of the following steps.

### Step 1 - Create a Meraki Organization

1. If you do not have a Meraki account with these permissions hosted in North America,  create one here: [account.meraki.com](https://account.meraki.com/login/new_account)

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE]
> You MUST select North America as your region!

</td></tr>
</table>
</div>

<img src="../../ASSETS/LABS/WORKFLOWS/CreateAccount1.png" alt="Workflow Properties" style="width:50%; height:auto; padding-left:40px;">

2. If you already have a Meraki account, you can use that. If you are a Cisco Employee **DO NOT USE** the Cisco SSO as that only has access to the Cisco demo account.

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="50%">

   <img src="../../ASSETS/LABS/WORKFLOWS/CreateAccount2.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
<td valign="top" width="50%">

3. When you sign in, choose Sign in to personal account. Do
not select Sign in with Cisco SSO.

   <img src="../../ASSETS/LABS/WORKFLOWS/CreateAccount3.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td></tr>
</table>
</div>

### Step 2 - Create a Meraki Network

If you have created a new Meraki Organization, you will need to create a placeholder network.

> [!NOTE]
> This step is not required if you already have a Meraki Organization with at least one network.

1. On the left hand menu, select Network and Create a network

   <img src="../../ASSETS/LABS/WORKFLOWS/CreateNetwork1.png" alt="Workflow Properties" style="width:60%; height:auto;">

2. Enter a Network name and click Create network. **Note:** This network will not be used in the lab.

   <img src="../../ASSETS/LABS/WORKFLOWS/CreateNetwork2.png" alt="Workflow Properties" style="width:80%; height:auto;">

### Step 3 - Enable Automate Workflows

Once you are logged in to your new Meraki account:

1. Select **`Organization > Early Access`**

   <img src="../../ASSETS/LABS/WORKFLOWS/EnableWorkflows1.png" alt="Workflow Properties" style="width:60%; height:auto;">

2. In the Early Access window, enable AI Assistant and Automate Workflows.

<div style="padding-left:40px;">
<table>
<tr><td valign="top" width="100%">

> [!NOTE]
> You will get a Opt in settings pop up, just click on Save.

</td></tr>
</table>
</div>

<div style="padding-left:40px;">
<table>
<tr>
<td valign="top" align="center" width="60%">

<img src="../../ASSETS/LABS/WORKFLOWS/EnableWorkflows2.png" alt="Workflow Properties" style="width:100%; height:auto;">

</td>
<td valign="bottom" align="center" width="40%">

   <img src="../../ASSETS/LABS/WORKFLOWS/EnableWorkflows3.png" alt="Workflow Properties" style="width:80%; height:auto;">

</td></tr>
</table>
</div>

## Summary

Congratulations, you are now ready to make use of Cisco Workflows, in the next section we will take a look at UI and the general functionality of the platform.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Cisco Workflows Orientation**](./module2-orientation.md)

> [**Return to LAB Menu**](./README.md)