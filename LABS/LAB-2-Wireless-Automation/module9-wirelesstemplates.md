# Wireless Templates

While most configurations for wireless can be addressed via the Cisco Catalyst (DNA) Center Graphical User Interface (GUI), there are a few items where configuration is required and neither the GUI nor the Model-Based Configuration can accomodate. In this subsection we will design templates to be used with Wireless Controllers to provision things which are not currently scoped by the Cisco Catalyst (DNA) Center Graphical User Interface (GUI).

Templates may be utilized as Composite or Regular Templates, and in either Jinja2 or Velocity. Additionally System and Bind Variables may be utilized in accordance to the previously mentioned topics earlier in this repository.

To refresh on those topics please refer to the following:

#### Templating

* [Onboarding Templates](../../Onboarding.md#onboarding-templates-and-flows) - This section will explain Onboarding Templates in DNAC and their use in bringing various devices under Catalyst Center management
* [DayN Templates](../../DayN.md#day-n-templates-and-flows) - This section will explain how to use templates for ongoing (Day-N) changes to the network
* [Building Templates](../../Templates.md#building-templates) - This section will explain how to build a template on DNAC from scratch

#### Velocity Language

* [Velocity Variables](../../Variables.md#velocity-variables) - This section explains Template Variables in depth, and how and where to use them
* [Velocity Scripting](../../Velocity.md#velocity-scripting) - This section will dive into Velocity Language Template Scripting constructs and use cases
* [Advanced Velocity Scripting](../../AdvancedVelocity.md#advanced-velocity) - This section will dive into Advanced Velocity Language Template examples

#### Jinja2 Language

* [Jinja2 Variables](../../Variables.md#jinja2-variables) - This section explains Template Variables in depth, and how and where to use them
* [Jinja2 Scripting](../../Jinja2.md#jinja2-scripting) - This section will dive into Jinja2 Language Template Scripting constructs and use cases
* [Advanced Jinja2 Scripting](../../AdvancedJinja2.md#advanced-jinja2) - This section will dive into Advanced Jinja2 Language Template examples

#### Variables

* [System Variables](../../SystemVariables.md#dna-center-system-variables) - This section explains Catalyst Centers System Variables

#### Fault-Finding

* [Troubleshooting](../../TroubleShoot.md#Troubleshooting) - This section will dive into Troubleshooting Velocity based Template Constructs

While there may be many use cases for templates in wireless, the use of the GUI negates the complexities involved with maintaining lengthy ones. There are however some examples which have used over the past few years when certain features were not available via the GUI in any form:

1. [⬇︎**SSID with mPSK**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_SSID_mPSK.json) - *(create mPSK keys in SSID)* - *(available in 2.3.5.x)*
2. [⬇︎**CCKM SSID**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_CCKM_templates.json) - *(CCKM setting for SSID)* - *(available in 2.3.5.x)*
3. [⬇︎**Anchor Priority**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_Anchor_Priority_templates.json) - *(Enabling)* - *(available in 2.3.3.x)*
4. [⬇︎**Open Roaming**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_Open_Roaming_project.json) - *(Set up open roaming from a Project)*
5. [⬇︎**RF**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_RF_templates.json) - *(Enabling RF Thresholds)*
6. [⬇︎**Radius Probes**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_AAA_Probes_templates.json) - *(Enabling Probes for AAA)*
7. [⬇︎**9800 Hardening**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_9800_Harden_templates.json) - *(Various Security Settings)*
8. [⬇︎**Onboarding**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_PnP_Onboarding_project.json) - *(Composite Example for PnP from a Project)*

9. [⬇︎**ALL Wireless Examples**⬇︎](https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/Wifi_Templates_Project.json) - *(All Wireless Examples in a Project)*

<details open>
<summary> Click the arrow for details</summary>

## Step 1 - ***Creating Wireless Templates***

While on Cisco Catalyst (DNA) Center you can import templates, we will build one specific for defining CCKM below.

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select `Tools>Template Editor`.

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-menu-tools-templateeditor.png?raw=true "Import JSON")

2. In the Template Editor **create** a new Jinja2 Regular Template in the DCLOUD PrepEnvironment Project. Customize a name that you will remember and select Regular, Jinja2, Wireless Controllers as device type and IOS-XE as software.

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-templateeditor-add.png?raw=true "Import JSON")
   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-templateeditor-parameters.png?raw=true "Import JSON")

3. Within the Editor View **paste** the following:

[//]: # ({% raw %})
```J2
{# This changes the delimiter from hyphen to colon for RADIUS communications to ISE.
#}

radius-server attribute wireless authentication mac-delimiter colon
radius-server attribute wireless accounting mac-delimiter colon

```
[//]: # ({% endraw %})
4. **Save** and **Commit** the Template to the project.

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-templateeditor-save-commit.png?raw=true "Import JSON")

## Step 2 - ***Assigning Wireless Templates***

1. Select the hamburger menu icon to open the menu. Select `Design>Network Profiles`.

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-menu-profiles.png?raw=true "Import JSON")

2. Select the **edit** button beside the Wireless Network Profile

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-profiles-edit.png?raw=true "Import JSON")

3. Scroll down to the **Attach Templates** and click the **⨁ Add Wireless Template** button

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-profile-template-add.png?raw=true "Import JSON")

4. In the Window that appears:
   
   1. Device Types select Wireless Controller
   2. Select **> Templates** to display the list
   3. Select **Wireless CCKM**
   4. Click **Add**

      ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-profile-template-add.png?raw=true "Import JSON")

5. Click Save to add the changes.

   ![json](../../ASSETS/LABS/WIRELESS/module8-wirelesstemplates/dnac-profiles-template-save.png?raw=true "Import JSON")

6. The configuration changes would now need to be provisioned to the Wireless Controller.

</details>

## Summary

Congratulations you have completed the Wireless Templating module of the lab and discovered how and when to utilize wireless templates. Please use the navigatation below to continue your learning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Wireless Controller High Availability Module**](../LAB-2-Wireless-Automation/module10-controllerha.md)

> [**Return to Lab Menu**](./README.md)