# [LABS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS#dnac-template-labs-)

This section built out in a lab format to guide you through the typical steps to complete various automation tasks delivered by Catalyst Center. It allows for customers to practice Catalyst Center workflows with Onboarding, DayN Templates, and Application Policy automation on both Wired and Wireless Platforms, while reducing the time and effort needed to instantiate the network The lab will also introduce advanced velocity templating topics and troubleshooting tools, which may help determine common failure scenarios in a deployment.

> [!IMPORTANT]
> Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Parter**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

> [!NOTE] 
> Thank you for continuing your **support** of the **DNAC-Template Repository** by your continued visits to the site. Over the past few years we have developed a lot of content as a result, it is **time to reorganize** it to help be more consise, and to aide users in finding the relevant content easily. Over the next few months you will **notice changes and updates** to the repository, as we **add** additional content, **revise** existing dated content and nomenclature. The **folder structure** and **resources** will be **reorganized** for ease of use, and so that CODE examples and TUTORIALS will be grouped together for ease of use. We hope this will help users to find the content they need in an easier manner.

## New Catalyst Center Lab Content

This newer and more modular lab approach is designed to deal with and includes concepts from the legacy labs in a newer more modular format.

1. [Lab 1 Wired Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation) - Covers green and brown field use cases **(allow 4.0 hrs)**
2. [Lab 2 Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation) - Covers traditional wireless automation  **(allow 4.0 hrs)**
2. [Lab 3 Advanced Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-3-Advanced-Automation) - Covers how to build templates and logic  **(allow 4.0 hrs)**
4. [Lab 4 Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - Covers [Postman](https://www.postman.com) automation and orchestration of Catalyst Center **(allow 2.0 hrs)**
5. Lab 5 Python Orchestration - In Development - Covers Python automation and orchestration of Catalyst Center **(allow 3.0 hrs)**
6. Lab 6 Ansible Orchestration - In Development - Covers Ansible automation and orchestration Catalyst Center **(allow 3.0 hrs)**
7. [Lab 7 CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) - Covers [Python](https://www.python.org) with [JENKINS](https://www.jenkins.io) orchestration via REST-API **(allow 4.0 hrs)**
8. [Lab 8 Cisco Workflows](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-8-Cisco-Workflows/) - Covers orchestration via REST-API **(allow TBD hrs)**

## Specific Lab Content

In this legacy lab section you will continue to find all the existing labs which deal with specifics in separate easy to do labs. This set of labs is being depricated due to new content above.

<details closed>
<summary> Expand section for Specific Lab Content if required </summary></br>

* [PnP Preparation](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module1-pnpprep.md) - The lab covers setup for Plug and Play **(allow 1.5 hrs)**
* [Onboarding Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module2-pnp.md) - The lab covers in depth topics in deploying Day 0 templates **(allow 1.5 hrs)**
* [Day N Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - The lab covers Day N template constructs and use cases **(allow 0.5 hrs)**
* [Composite Templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/LABS/LAB-1-Wired-Automation/module3-dayn.md) - This lab covers building a composite template on Catalyst Center **(allow 0.5 hrs)**
* [Application Policys](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automationy/module4-applicationqos.md) - This lab covers Application Policy & SDAVC in Catalyst Center **(allow 1.0 hrs)**
* [Telemetry](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module5-telemetry.md) - This lab explains how to deploy Streaming Telemetry for Catalyst Center Assurance **(allow 0.5 hrs)**
* [Advanced Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-1-Wired-Automation/module6-advanced.md) - This lab will explore Advanced Automation examples **(allow 1.5 hrs)**
* [Dynamic Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-3-Advanced-Automation/) - This lab will explore additional Advanced Automation examples **(allow 2.0 hrs)**
* [Rest-API Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-4-Rest-API-Orchestration/) - This lab uses [Postman](https://www.postman.com) Collections to automate Catalyst Center **(allow 2.0 hrs)**
* [Wireless Automation](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-2-Wireless-Automation/) - This lab covers Traditional Wireless Automation  **(allow 6.0 hrs)**
* [Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-K-Orchestration/) - This lab covers [Postman](https://www.postman.com) and [Ansible](https://www.ansible.com) orchestration **(allow 4.0 hrs)**
* [CICD Orchestration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/LABS/LAB-7-CICD-Orchestration/) This lab covers [Python](https://www.python.org), [Ansible](https://www.ansible.com) and [JENKINS](https://www.jenkins.io) to orchestrate via REST-API **(allow 4.0 hrs)**

</details>

## [Practical Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/TUTORIALS/ExamplesAndConcepts.md)

In this section I have compiled a number of template examples built with Jinja2 Language. These samples include a wide ranging set of configurations which may be used in your labs to solve specific configuration requirements. This collection summarizes aspects covered previously in this templating repository, and are aimed at providing quick practical references to help engineers solve automation tasks with the help of Catalyst Center. Additionally these examples may be used in testing in [dCloud](https://dcloud.cisco.com) with any of the labs on this repository.

* [Practical Template Examples](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/TUTORIALS/ExamplesAndConcepts.md)

## DCLOUD as a LAB

### Overview

As a quick start with Catalyst Center Automation, you may utilize the above labs in conjuction with DCLOUD's sandbox:

1. [Cisco Enterprise Networks Hardware Sandbox West DC](https://dcloud2-sjc.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)
2. [Cisco Enterprise Networks Hardware Sandbox East DC](https://dcloud2-rtp.cisco.com/content/catalogue?search=Enterprise%20Networks%20Hardware%20Sandbox&screenCommand=openFilterScreen)

This allows you to run these labs and gives not only an environment to try the various code samples, but also to develop and export your own code for use in your production environment. DCLOUD  provides for rapid and safe POC/POV on-demand environment without impacting production environments. DCLOUD also negates the need for shipping equipment, associated lead times, and licensing issues associated with setting up your own private testing environment. Please do adhere to the best practices for the DCLOUD environment when using it.

DCLOUD allows for use with a web-based browser client for VPN-less connectivity, as well as AnyConnect VPN client connectivity for those who prefer it. The labs are hosted in Cisco San Jose Facility (Select US East or US West Region when scheduling in DCLOUD). Choose the Cisco Enterprise Network Sandbox version you prefer. 

> [!IMPORTANT]
> To access this or any other content, including demonstrations, labs, and training in DCLOUD please work with your **Cisco Account team** or **Cisco Partner Account Team** directly. Your Account teams will make sure the session is scheduled and shared for you to use. Once booked follow the guide within Github to complete the tasks adhering to the best practices of the DCLOUD environment.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](./README.md)