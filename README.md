# DNAC-TEMPLATES [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

> [!NOTE] 
> Thank you for continuing your **support** of the **DNAC-Template Repository** by your continued visits to the site. Over the past few months we have updated and redeveloped a lot of content and it is **reorganized** to be more consise, and to aide users in finding the relevant content easily. Over the next few months you will **notice more lab updates** to the repository, as we **add** additional content. The **folder structure** and **resources** have been **reorganized** for ease of use, and so that **[CODE](./CODE/README.md)** examples and **[TUTORIALS](TUTORIALS.md)** will be grouped together for ease of use. We hope this will help users to find the content they need in an easier manner.

> [!IMPORTANT]
>**[Discussions](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions):** is now now open, so please do use that for feedback suggestions on improvements or other ideas, please use this link: **[Discussions](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions)**</br></br>**[Issues](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new):** will now be used to track problems with documentation or the labs and code, please use this link: **[Issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new)**

## Cisco Catalyst Center

![Cisco Catalyst Center Overview](./ASSETS/cisco_dnac.png)

Cisco Catalyst Center is an intelligent Automation and Assurance platform for the campus. Cisco Catalyst Center enables, simplified Day-0 through Day-N management of switching, routing, and wireless infrastructure. It also improves operations with AI/ML-enhanced analytics to streamline troubleshooting and provide actionable insights into the health of the network and the quality of experience for users and applications. Here are some of the capabilities of Cisco Catalyst Center in their respective domains:

* NetOps: Network Plug and Play for Zero Touch Deployment, Software Image Management, Compliance, Configuration Templates and Network Profiles, Model-Driven Configuration, and RMA Support.
* AIOps: AI/ML-enhanced monitoring and troubleshooting support. Predictive Insights, Network Baselines, Network Reasoner, Device/Client/Application 360, Intelligent Capture.
* SecOps: AI Endpoint Analytics, Group-Based Policy and Analytics, Software-Defined Access
* DevOps: ITSM Integrations, APIs, SDK & Ansible Module 

## Overview

This Repository will give examples of templates used in Cisco Catalyst Center that can be modified. Additional information will be included to hopefully give a well rounded explanation of Automation methods with Templates using Cisco Catalyst Center and flows with both Onboarding and DayN Templates and concepts.

The repository will include scripts and examples with the following:

1. Template Scripting for both Jinja and Velocity
2. Variable notation and usage
3. Binding Variables
4. System Variables
5. Regular Templates
6. Composite Templates

The goal of this repository is a practical guide to allow engineers to rapidly begin using Cisco Catalyst Center automation and begin conversion of IOS CLI Templates. The Templates have been developed over the years and with various use cases in mind, and so the intent of sharing this collection is to reduce the lift to begin automating.

## Intent Based Networking

Either one or multiple Templates may be used to deploy Intent in combination with the Design Settings and Policies deployed within the UI. One or Multiple templates may be used in Onboarding (PnP) or Day N methods. Day N methods are designed for making ongoing changes and may require 'no' statements depending on the configuration construct being modified. 

Additionally:

1.	Intent can be defined as the set of code along with the configuration constructs deployed via a template.
2.	Variables can be used to modify or choose between constructs deployed via decision (‘IF’) statements
3.	Repetition of any construct may be introduced through the use of Looping structures on any device.
4.	Variables may be used when the device is being onboarded or provisioned

## Tutorial Sections

Various sections will be covered within this github repository. Please use this menu as the main index for navigating content. 
You will find various examples within the various folders of this repository, with supplied explanation readme files for reference.

### Workflows

* [PnP Workflow](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/PnP-Workflow.md#pnp-workflow) - This section explains the overall Plug and Play Methodology
* [Onboarding Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Onboarding.md#onboarding-templates-and-flows) - This section will explain Onboarding Templates in Cisco Catalyst Center and their use in bringing various devices under Cisco Catalyst Center management
* [DayN Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/DayN.md#day-n-templates-and-flows) - This section will explain how to use templates for ongoing (Day-N) changes to the network

### Templating

* [Building Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Templates.md#building-templates) - This section will explain how to build a template on Cisco Catalyst Center from scratch

#### Velocity Language

* [Velocity Variables](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Variables.md#velocity-variables) - This section explains Template Variables in depth, and how and where to use them
* [Velocity Scripting](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Velocity.md#velocity-scripting) - This section will dive into Velocity Language Template Scripting constructs and use cases
* [Advanced Velocity Scripting](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/AdvancedVelocity.md#advanced-velocity) - This section will dive into Advanced Velocity Language Template examples

#### Jinja2 Language

* [Jinja2 Variables](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Variables.md#jinja2-variables) - This section explains Template Variables in depth, and how and where to use them
* [Jinja2 Scripting](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Jinja2.md#jinja2-scripting) - This section will dive into Jinja2 Language Template Scripting constructs and use cases
* [Advanced Jinja2 Scripting](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/AdvancedJinja2.md#advanced-jinja2) - This section will dive into Advanced Jinja2 Language Template examples

### Advanced Use Cases

* [Embedded Event Manager](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/EEM.md#EEM) - This section will dive into EEM (Embedded Event Manager) Scripting and various use cases 
* [System Variables](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/SystemVariables.md#dna-center-system-variables) - This section explains Cisco Catalyst Centers System Variables
* [JSON YAML XML Explained](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/JsonYamlXml.md#json-yaml-xml-explained) - This section explains various DATA Structures and Formats

### Orchestration of Cisco Catalyst Center

* [REST API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/RestAPI.md) - This section is a high level discussion of utlilizing REST API with Cisco Catalyst Center
* [Python Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Python.md) - This section is a high level discussion of utilizing Python with Cisco Catalyst Center
* [Ansible Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Ansible.md) - This section is a high level discussion of Ansible orchestration of Cisco Catalyst Center
* [CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/CICD.md) - This section is a high level discussion of CICD orchestration of Cisco Catalyst Center

### Fault-Finding

* [Troubleshooting](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/TroubleShoot.md#Troubleshooting) - This section will dive into Troubleshooting Velocity based Template Constructs

## [DNAC Template LABS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS#dnac-template-labs-)

This section built out in a lab format to guide you through the typical steps to complete various automation tasks delivered by Cisco Catalyst Center. It allows for customers to practice Cisco Catalyst Center workflows with Onboarding, DayN Templates, and Application Policy automation on both Wired and Wireless Platforms, while reducing the time and effort needed to instantiate the network The lab will also introduce advanced velocity templating topics and troubleshooting tools, which may help determine common failure scenarios in a deployment.

**IMPORTANT:** Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Parter**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

## New Catalyst Center Lab Content

This newer and more modular lab approach is designed to deal with and includes concepts from the legacy labs in a newer more modular format.

1. [Lab 1 Wired Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation) - Covers green and brown field use cases **(allow 4.0 hrs)**
2. [Lab 2 Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation) - Covers traditional wireless automation  **(allow 4.0 hrs)**
4. [Lab 4 Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - Covers [Postman](https://www.postman.com) automation of Cisco Catalyst Center **(allow 2.0 hrs)**
7. [Lab 7 CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) - Covers [Python](https://www.python.org) with [JENKINS](https://www.jenkins.io) orchestration via REST-API **(allow 4.0 hrs)**

## Legacy Lab Content

In this legacy lab section you will continue to find all the existing labs which deal with specifics in separate easy to do labs. This set of labs is being depricated due to new content above.

<details closed>
<summary> Expand section for Legacy Lab Content if required </summary></br>

* [PnP Preparation](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module1-pnpprep.md) - The lab covers setup for Plug and Play **(allow 1.5 hrs)**
* [Onboarding Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module2-pnp.md) - The lab covers in depth topics in deploying Day 0 templates **(allow 1.5 hrs)**
* [Day N Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - The lab covers Day N template constructs and use cases **(allow 0.5 hrs)**
* [Composite Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - This lab covers building a composite template on Cisco Catalyst Center **(allow 0.5 hrs)**
* [Application Policys](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automationy/module4-applicationqos.md) - This lab covers Application Policy & SDAVC in Cisco Catalyst Center **(allow 1.0 hrs)**
* [Telemetry](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module5-telemetry.md) - This lab explains how to deploy Streaming Telemetry for Cisco Catalyst Center Assurance **(allow 0.5 hrs)**
* [Advanced Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module6-advanced.md) - This lab will explore Advanced Automation examples **(allow 1.5 hrs)**
* [Dynamic Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-3-Advanced-Automation/) - This lab will explore additional Advanced Automation examples **(allow 2.0 hrs)**
* [Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - This lab uses [Postman](https://www.postman.com) Collections to automate Cisco Catalyst Center **(allow 2.0 hrs)**
* [Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation/) - This lab covers Traditional Wireless Automation  **(allow 6.0 hrs)**
* [Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-K-Orchestration/) - This lab covers [Postman](https://www.postman.com) and [Ansible](https://www.ansible.com) orchestration **(allow 4.0 hrs)**
* [CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) This lab covers [Python](https://www.python.org), [Ansible](https://www.ansible.com) and [JENKINS](https://www.jenkins.io) to orchestrate via REST-API **(allow 4.0 hrs)**

</details>

## [Practical Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/TUTORIALS/ExamplesAndConcepts.md)

In this section I have compiled a number of template examples built with Jinja2 Language. These samples include a wide ranging set of configurations which may be used in your labs to solve specific configuration requirements. This collection summarizes aspects covered previously in this templating repository, and are aimed at providing quick practical references to help engineers solve automation tasks with the help of Cisco Catalyst Center. Additionally these examples may be used in testing in [dCloud](https://dcloud.cisco.com) with any of the labs on this repository.

* [Practical Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/TUTORIALS/ExamplesAndConcepts.md)

## [DNAC Templates Store](https://github.com/kebaldwi/DNAC-Templates-Store)

This repository is built out to share Cisco Catalyst Center Templates and allow for ongoing submissions from those inclined to share their work with the community. Initially the repository includes all the examples that we have used in this repository in RAW TEXT and JSON format. After your first submission you will be able to continually add your templates as you develop new and interesting approaches to device management. 

Please maintain the directory structure with submissions. If you have a suggestion please reach out and contact me.

Please use this menu to navigate the various sections of this separate [DNAC Templates Store](https://github.com/kebaldwi/DNAC-Templates-Store) Github repository. Within the multiple folders are examples, explanation readme files for reference.

* [RAW TEXT Examples](https://github.com/kebaldwi/DNAC-Templates-Store/tree/main/RAW-TEXT-EXAMPLES) - Templates in raw text for editing
* [DAY ZERO JSON](https://github.com/kebaldwi/DNAC-Templates-Store/tree/main/DAY-ZERO-JSON) - JSON files for easy import to Cisco Catalyst Center for Day Zero
* [DAY N JSON](https://github.com/kebaldwi/DNAC-Templates-Store/tree/main/DAY-N-JSON) - JSON files for easy import to Cisco Catalyst Center for Day N
* [REGULAR JSON](https://github.com/kebaldwi/DNAC-Templates-Store/tree/main/DAY-N-JSON/REGULAR-JSON) - JSON files for easy import to Cisco Catalyst Center for Day N
* [COMPOSITE JSON](https://github.com/kebaldwi/DNAC-Templates-Store/tree/main/DAY-N-JSON/COMPOSITE-JSON) - JSON files for easy import to Cisco Catalyst Center for Day N

## DCLOUD as a LAB

### Overview

As a quick start with Cisco Catalyst Center Automation, you may utilize the above labs in conjuction with DCLOUD's sandbox:

1. [Cisco Enterprise Networks Hardware Sandbox West DC](https://dcloud2-sjc.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)
2. [Cisco Enterprise Networks Hardware Sandbox East DC](https://dcloud2-rtp.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)

This allows you to run these labs and gives not only an environment to try the various code samples, but also to develop and export your own code for use in your production environment. DCLOUD  provides for rapid and safe POC/POV on-demand environment without impacting production environments. DCLOUD also negates the need for shipping equipment, associated lead times, and licensing issues associated with setting up your own private testing environment. Please do adhere to the best practices for the DCLOUD environment when using it.

DCLOUD allows for use with a web-based browser client for VPN-less connectivity, as well as AnyConnect VPN client connectivity for those who prefer it. The labs are hosted in Cisco San Jose Facility (Select US East or US West Region when scheduling in DCLOUD). Choose the Cisco Enterprise Network Sandbox version you prefer. 

>**Note:** To access this or any other content, including demonstrations, labs, and training in DCLOUD please work with your Cisco Account team or Cisco Partner Account Team directly. Your Account teams will make sure the session is scheduled and shared for you to use. Once booked follow the guide within Github to complete the tasks adhering to the best practices of the DCLOUD environment.

## Examples

These examples must be used with two conditions:

* Deployed a PnP Discovery method and DHCP scope - see [PnP Workflow](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/PnP-Workflow.md#pnp-workflow)
* Build the template with methods detailed - see [Creating Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Templates.md#template-creation)

When building the template you will need to select a scripting language. Specific examples of Templates in the two scripting languages supported are available in the following folders:

* [Velocity Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/VELOCITY/)
* [Jinja2 Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2) 

The conditions that they are used are documented and are explained in [Onboarding Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/Onboarding.md) and examples of DayN Templates are explained in [DayN Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/TUTORIALS/DayN.md)

> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

