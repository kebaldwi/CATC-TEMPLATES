# DayN Provisioning

## Overview

This Module is designed to be a part of a series of labs built to address how to use DayN templates within Catalyst Center to configure network devices at Day 1 through N. This Lab is designed to be used after first completing the previous modules. The purpose of DayN templates is to allow for ongoing configuration of features on devices beyond those deployed on the Claiming process. With Catalyst Center, if devices are not within a fabric, the host onboarding part of the UI will not be available. To that end, templates are an easy way of deploying those types of configuration and much more. Before starting this Lab, please make sure you have finished all the steps in the previous modules.

## General Information

Catalyst Center can be used for Plug and Play and Day N or Ongoing Templates; customers will start by building out an Onboarding Template that typically deploys only enough information to bring the device up initially. While it might include the entire configuration for a traditional network device, this is better served by Day N Templates as they can be used to apply ongoing changes and to allow device modifications after initial deployment. This lab section will focus on Day N templates to be built as regular templates within Catalyst Center.

Another important consideration is that part of a typical configuration would include some lines of code, which are built by the *Design >Network Settings >* application within Catalyst Center. If the Design component is used, you should **not** deploy the same feature from cli code in a template to configure the device. It's a decision you have to make upfront, avoids many lines in the templates, and allows for a more UI-centric configuration that is easier to maintain. 

As guidance, try and use **Design Settings** for as many configurations as you can, leaving Templates light and nimble for configurations that might change ongoing.

### Greenfield

When dealing with net new devices using the Provisioning process we utilize it is better to utilize composite templates with multiple regular templates within. This allows greater flexibility and a method to always add to the structure for compliance reasons. Additionally, Jinja2 and Velocity Scripting languages may be intermingled, allowing for the reuse of existing scripts.

### Brownfield

When dealing with existing infrastructure, initially we want to absorb the device and its configuration into Catalyst Center to allow for monitoring and a gradual shift to automated management, as the device usually is in a running state supporting the network, and the configuration pre-exists.

As time progresses though, we may want to introduce slowly automation from Catalyst Center utilizing DayN Templates. Be aware that with Brownfield device configurations, there is no template learning capability for switching. As such configuration on the device may need modification prior to provisioning in some situations. Should it be a newer device, you may want to Discover and then push a normalization template via REST API to remove settings that would cause ongoing provisioning errors. Should this be a device already in Catalyst Center, then a normalization strategy may need to be adopted, backing out certain configuration, prior to provisioning. This script will involve perhaps the removal of AAA commands and others which cause issues with provisioning.

## Catalyst Center DayN Template Overview

Additionally, while a more extensive set of settings can be built out for deployment, we will limit the configuration to the **minimum** necessary to perform this step, building off the completed tasks in module 2.

You can create Regular Day N Templates using Jinja2 and Velocity scripting languages within the **Template Hub** within **Catalyst Center**. There are two basic types of templates we can utilize. **Regular** templates, as well as **Composite** templates. Use a combiination of these templates to adhere to the **DRY** philosophy.

### Regular Templates

**Regular** templates are templates which are typically designed to address a specific use case. Regular templates are written in either Jinja2 or Velocity scripting languages. Each Language has features which may be leveraged to make the script more reusable, allowing the user to not have to repeat themselves. This modular capability allows us to keep a script written to address a specific need small. At the same time each form of scripting language allows for features like variables, conditional logic, and looping constructs. This allows for a small powerful script to be written making it more light weight and easier to fault find and maintain.

### Composite Templates

**Composite** templates are logical templates used for grouping together multiple **Regular** templates. They allow you to use Jinja2 and Velocity **Regular** templates within the same logical template. This allows us to make templates in mutliple languages and to be able to reuse long standing Velocity scripts with newer Jinja2 templates within the same **Composite** Template. This allows for people to code in the language they are more accustomed too, and to continue to support existing scripts.

### Scripting Languages

**Jinja2** and **Velocity** both have similar capabilities. For additional information please see these tutorials. You may want to open these in another tab to read the content and to allow you to continue the lab:

* [Velocity Scripting](../../TUTORIALS/Velocity.md)
* [Jinja2 Scripting](../../TUTORIALS/Jinja2.md)

Within these logical constructs you have many tools and these are an example but not all of them, please review each section as needed:

#### Velocity Scripting Logic

Velocity's deployment in Catalyst Center is utilizing 1.75 version, and as such has the typical logical capabilities available within that release. Please see the following:

* [If Statements](../../TUTORIALS/Velocity.md#if-statements)
* [Macros](../../TUTORIALS/Velocity.md#macros)
* [Loops](../../TUTORIALS/Velocity.md#foreach-loops)
* [Multiline commands](../../TUTORIALS/Velocity.md#multi-line-commands)

#### Jinja2 Scripting Logic

Jinja2 as deployed in Catalyst Center allows for the following capabilities as well as include and extend capabilities. Please see the following:

* [If Statements](../../TUTORIALS/Jinja2.md#conditional-statements)
* [Macros](../../TUTORIALS/Jinja2.md#macros)
* [Loops](../../TUTORIALS/Jinja2.md#for-loops)
* [Multiline commands](../../TUTORIALS/Jinja2.md#multi-line-commands)

## Catalyst Center DayN Template Provisioning

This section will go through the build and provisioning of **Composite** and **Regular** templates via Catalyst Center to a Catalyst 9k switch. We will deal with **Brownfield** and **Greenfield** scenarios during this module.

### Section 1 - Preparation

We will download and import a template project to include templates for deployment of the Wired Lab environment. Contained in the download will be **Regular** and **Composite** template examples which we will use against both the **Greenfield** and **Brownfield** devices.

#### Step 1 - Import the Day N Templates

We will use the **Template Hub** to write, maintain and test template projects. A Project is a logical folder or grouping of templates. Templates can be imported or exported individually or as a collection in a project. We will be importing a Project into the template editor which will have a combination of **Regular** and **Composite** templates.

**Download**, **Extract** and **import** a set of Day N Templates into the **Template Hub** using the file: <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/DAYN/JSON/Titanium_WiredAutoLab_Jinja2_project.json">**⬇︎Titanium_WiredAutoLab_Jinja2_project.json⬇︎**</a></br></br>

1. Navigate to the **Template Hub**  within Catalyst Center through the menu **`Tools > Template Hub`**.

   ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateTemplate.png?raw=true "Import JSON")

2. Within the **Template Hub**, hover over the import link and select **Import Project** within the menu.  

   ![json](../../ASSETS/LABS/WIRED/DNAC-ProjectImportBegins.png?raw=true "Import JSON")

3. Click **Select a file from your computer**, then in the file explorer search for the file as shown in the image `Titanium_WiredAutoLab_Jinja2_project.json`. This project will be the one that has all our templates. Click **Open** to prepare it for uploading.

   ![json](../../ASSETS/LABS/WIRED/DNAC-ProjectImportSelect.png?raw=true "Import JSON")

4. Click **Import** 

   ![json](../../ASSETS/LABS/WIRED/DNAC-ProjectImportDayN.png?raw=true "Import JSON")

5. Within the **Template Hub** you will notice a new Project appear, click on the **Project Name** link to display the Projects. Notice the following:
   1. Project - **DCLOUD CATC Template Labs DayN Jinja2** 
   2. Composite Template - **CATC Template Labs DayN Composite Jinja2** 
   3. Regular Template - **c9300-2-Setup-Configuratioh**

   ![json](../../ASSETS/LABS/WIRED/DNAC-ProjectImported.png?raw=true "New IMage Required")

6. Select the **AAA-Configuration** template and notice it has configuration within it. Some templates are just that, others make use of logical statements, conditional statements, looping structures and variables. You will see the following commands in the template selected.

```J2
aaa new-model
!
aaa authentication username-prompt "Authorized Username:"
aaa authentication login admin local
aaa authorization console
aaa authorization exec admin local
aaa authentication login admin local-case
aaa authorization exec admin local 
!
mac address-table notification mac-move
mac address-table notification threshold
mac-address-table notification change
!
```

### Section 2 - Configuring Network Profile

In this section we will prepare the Network Profile to allow for provisioning of the Greenfield and Brownfield network devices. In order to accomodate the fact that we have two types of templates to use, one for the distribution and one for access, both of which will be used on 9300, we need to be able to effectively choose between the templates for the specific use cases.

In this situation we will inlist the use of **TAGs** to identify the use case for the template and filter accordingly.

#### Step 1 - Create and Apply the Device TAGs

We will Create and Assign **TAGs** to the **ACCESS** switch and the **DISTRO** switch as follows:

   1. Within Catalyst Center Navigate to **`Provision > Network Devices > Inventory`**      

      ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateInventory.png?raw=true "Import JSON")

   2. We will **TAG** the device **c9300-1** as **ACCESS**, complete the following:

      1. Select **c9300-1** on the left
      2. Click the **Tag** link and in the menu provided
      3. Enter **`ACCESS`** in the search field for the **TAG** 
      4. Click the option **Create new tag (ACCESS)**   

            ![json](../../ASSETS/LABS/WIRED/CATC-Inventory-TAG-9300-1-ACCESS.png?raw=true "Import JSON")

   3. We will **TAG** the device **c9300-2** as **DISTRO**, complete the following:

      1. Select **c9300-2** on the left
      2. Click the **Tag** link and in the menu provided
      2. Enter **`DISTRO`** in the search field for the **TAG** 
      3. Click the option **Create new tag (DISTRO)**   

            ![json](../../ASSETS/LABS/WIRED/CATC-Inventory-TAG-9300-2-DISTRO.png?raw=true "Import JSON")

   4. At this point the two switches **c9300-1** and **c9300-2** should be tagged accordingly as shown:    

      ![json](../../ASSETS/LABS/WIRED/CATC-Inventory-TAG-9300s-RESULT.png?raw=true "Import JSON")

#### Step 2 - Modify the Network Profile for the DayN Templates

Assign the DayN Templates for both the Greenfield and Brownfield 9300's to a site using the Network Profile. As there is an existing network profile for the site, we **must** reuse that one as you can only have one switching profile associated to a specific site. **(required)** 

We will Modify and Assign **DayN Templates** to the switches using **ACCESS** and **DISTRO** **TAGs** as follows:

   1. Navigate to Network Profiles by selecting **`Design > Network Profiles`**.

      ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateProfile.png?raw=true "Import JSON")


   2. Click the **Edit** link next to the **CATC Template Lab Floor 1** switching profile created earlier.  

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileEdit.png?raw=true "Import JSON")

   3. Within the Profile Editor, select the **Day-N Template(s)** tab click **⨁ Add Template** 

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileDayNAdd.png?raw=true "Import JSON")   

   4. Within the **Add Template** side tile complete the following:

      For the **`CATC Template Labs DayN Composite Jinja2`** Template do the following:

      1. Select the **`CATC Template Labs DayN Composite Jinja2`** Template from the list as shown
      2. Click the **APPLICABLE DEVICE TAGS** search window 
      3. Select the **ACCESS** tag
      4. The **ACCESS** tag should now appear as shown in the **APPLICABLE DEVICE TAGS** section
      5. Click **Add**

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileDayN-ACCESS.png?raw=true "Import JSON")   

      For the **`c9300-2-Setup-Configuration`** Template do the following:

      1. Select the **`c9300-2-Setup-Configuration`** Template from the list as shown
      2. Click the **APPLICABLE DEVICE TAGS** search window and type **DISTRO**
      3. Select the **DISTRO** tag
      4. The **DISTRO** tag should now appear as shown in the **APPLICABLE DEVICE TAGS** section
      5. Click **Add**

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileDayN-DISTRO.png?raw=true "Import JSON")   

   5. Click **X** to close the **Add Template** window.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileCloseAddTemplate.png?raw=true "Import JSON")   

   6. You will notice both templates as shown click the **view Device Tag** link on the **`c9300-2-Setup-Configuration`** Template and verify the **DISTRO** tag appears as shown.

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileSuccess-1.png?raw=true "Import JSON")   

   7. You will notice both templates as shown click the **view Device Tag** link on the **`c9300-2-Setup-Configuration`** Template and verify the **DISTRO** tag appears as shown.

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileSuccess-2.png?raw=true "Import JSON")   

   8. Click **Save** to save the modifications to the Network Profile.

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProfileSuccess.png?raw=true "Import JSON")   

### Section 3 - Greenfield DayN Provisioning Sequence

In this section we will apply a DayN template to the device **c9300-1** which we onboarded through the use of Plug and Play (PnP). This device had no configuration on it and as such we will now expand on the configuration.

#### Step 1 - Provisioning the Device

At this point, Catalyst Center is set up and ready to provision composite template to the device. This next set of sequences will push the various Network Settings, Services, and DayN Template to the **Greenfield** device.

We will now provision the switch using DayN Templates. To do this, do the following:

   1. Within Catalyst Center Navigate to **`Provision > Network Devices > Inventory`**.      

      ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateInventory.png?raw=true "Import JSON")

   2. Put a checkmark next to the device **c9300-1** to be provisioned.
   3. Click the **Actions > Provision > Provision Device** link and walk through the workflow presented:    

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionBegin.png?raw=true "Import JSON")

      1. The floor was already selected as part of the claim so click **next**    

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionSite.png?raw=true "Import JSON")

      2. Select **c9300-1** on the left and ensure the two tick boxes at the top of the page are ticked, then click the **SystemManagement-Configuration** tab. Enter `Building10` as the location  

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionAdvConfig-1.png?raw=true "Import JSON")
      
      3. Click the **Interfaces-Configuration** tab. Select the following as shown:

         1. Vlan Schema: **`A`**  
         1. Access Point Interfaces: **`GigabitEnthernet1/0/2`**  
         1. Then click **Next** to continue

            ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionAdvConfig-2.png?raw=true "Import JSON")
      
      4. Review the information to be deployed and click **Deploy**.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionDeploy.png?raw=true "Import JSON")

      5. Select **`Generate Configuration Preview`** and then click **Apply** on the Provision Device pop-up screen.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionApply.png?raw=true "Import JSON")

   4. The task will be submitted, and the deployment will run. Click on **Work Items** to display the configuration rendered prior to provisioning.

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionTask.png?raw=true "Import JSON")

   5. The configuration will be rendered, and you can click the preview to show it, and continue the deployment. Within the preview page click **Deploy** and the deployment will run. 

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionTasking.png?raw=true "Import JSON")

   6. You will be presented with a screen to schedule the deployment, select **Now** and click **Apply**. A screen will pop up after this asking whether you wish to delete the task, click **No** to keep a history.

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionScheduled.png?raw=true "Import JSON")

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionScheduled-2.png?raw=true "Import JSON")

   7. You can monitor the deployment on the Inventory page. Return to the Inventory via the menu, and change to the **Provisioning** Focus as shown.

      ![json](../../ASSETS/LABS/WIRED/DNAC-InventoryProvision.png?raw=true "Import JSON")
       
At this point, we have onboarded a device and successfully pushed configuration via Onboarding and DayN Templates. Our DayN automation for the Greenfield device used a **Composite** template composed of **Regular** templates. Take some time and review the templates and logic used.

> [!CAUTION]
> If you populate the UI with settings, those parameters should **NOT** be in your templates as they will **conflict**, and the deployment through provisioning will fail. While it is easy to populate these settings, it is best to test with a switch to see what configuration is pushed.

### Section 4 - Brownfield DayN Provisioning Sequence

In this section we will apply a DayN template to the device c9300-2 which we onboarded through the use of the Discovery Tool. This device had configuration on it and as such we will now expand on the configuration and augment the configuration.

#### Step 1 - Provisioning the Device

At this point, Catalyst Center is set up and ready to provision composite template to the device. This next set of sequences will push the various Network Settings, Services, and DayN Template to the **Brownfield** device.

We will now provision the switch using DayN Templates. To do this, do the following:

   1. Within Catalyst Center Navigate to **`Provision > Inventory`**.      

      ![json](../../ASSETS/LABS/WIRED/DNAC-NavigateInventory.png?raw=true "Import JSON")

   2. Put a checkmark next to the device **c9300-2** to be provisioned.
   3. Click the **Actions > Provision > Provision Device** link and walk through the workflow presented:    

      ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionBegin-c9300-2.png?raw=true "Import JSON")

      1. The floor was already selected as part of the claim so click **next**    

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionSite-c9300-2.png?raw=true "Import JSON")

      2. Select **c9300-2** on the left and ensure the two tick boxes at the top of the page are ticked, then complete the following:
      
         1. Enter **`Building10`** for the SNMP Location 
         2. Click the down arrow beside **Routed Interfaces** to allow you to search and select interface **`GigabitEthernet1/0/48`**  

            ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionAdvConfig-1-c9300-2.png?raw=true "Import JSON")
      
      3. Click the **Access Point Interfaces** dropdown and then search and select interface **`GigabitEthernet1/0/2`** which has an Access Point attached to it.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionAdvConfig-2-c9300-2.png?raw=true "Import JSON")

      4. Review the information and click **Next**.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionAdvConfig-3-c9300-2.png?raw=true "Import JSON")

      5. Review the information and click **Deploy**.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionSummary-c9300-2.png?raw=true "Import JSON")

      6. Select **`Now`** and then click **Apply** on the Provision Device pop-up screen to deploy the template immediately.

         ![json](../../ASSETS/LABS/WIRED/DNAC-ProvisionDeploy-c9300-2.png?raw=true "Import JSON")

   5. The task will be submitted, and the deployment will run. You can monitor the deployment on the Inventory page. Change to the **Provisioning** Focus as shown.

      ![json](../../ASSETS/LABS/WIRED/DNAC-InventoryProvision.png?raw=true "Import JSON")
       
At this point, we have onboarded a device and successfully pushed configuration via Discovery and DayN Templates. Our DayN automation for the Brownfield Device used a **Regular** template and within it multiple **Included** templates. Take some time and review the templates and logic used.

> [!CAUTION]
> If you populate the UI with settings, those parameters should **NOT** be in your templates as they will **conflict**, and the deployment through provisioning will fail. While it is easy to populate these settings, it is best to test with a switch to see what configuration is pushed.

### Automating Provisioning

While it is possible to click through the claiming and provisioning processes manually, which can be time-consuming, we can handle bulk deployments differently. For Bulk deployments, after the templates are built and assigned to the network profile and a site, we may automate them further by uploading a CSV file to Catalyst Center via REST API.

## Summary

The next step will be to build Composite Template to include the Day N regular templates created in this lab for the switches to be pushed out to the various devices in the network infrastructure. 

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Application QoS Lab**](./module4-applicationqos.md)

> [**Return to LAB Menu**](./README.md)
