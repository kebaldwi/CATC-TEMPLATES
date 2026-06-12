# REST API Orchestration with Python - IN DEVELOPMENT

![json](../../ASSETS/COMMON/BUILD/underconstruction.png?raw=true "Import JSON")

## Overview

This Lab is designed as a standalone lab to help customers with varying challenges in Automating and Orchestrating their network infrastructure using Python. Within the lab, we will use various tools and techniques to Automate various tasks and orchestrate Catalyst Center. 

## General Information

Until this point, we have used Rest-API for some basic setup tasks in labs 1 and 2, but there are so many situations that can be solved or at least eased using Rest-API in conjunction with Catalyst Center. In this lab, we will use a complete set of REST-API collections which will build upon the foundational knowledge acquired in the previous labs. For this lab, we will concentrate on Catalyst Center configuration and how Catalyst Center can be automated to perform various functions which we have already covered. 

Ultimately we are all striving to completely automate the network infrastructure. The closer we get to full service automation the closer we get to business process orchestration. Continual Implementation Continual Deployment is a goal that some companies aspire to and one which the concepts here can stive towards. 

![json](./assets/cicd-pipeline2.png?raw=true "Import JSON")

This lab is meant to mirror the concepts of **[LAB 4 REST-API Orchestration with Postman](../LAB-4-Rest-API-Orchestration/README.md)** so as to build on the existing foundation of knowledge. If you have not done so already please do go through lab four to acquaint yourself with the general concepts.

The lab will utilize a set of python programs shared in the code section of the repository. These programs will also be expanded to keep in line with this lab.

**IMPORTANT:** Please note that LAB content in this Repository is aligned with specific DCLOUD Demonstrations that have to be set up by either a **Cisco Employee** or a **Cisco Parter**. If you are having trouble accessing the DCLOUD content please get in touch with your **Local Cisco Account Team**.

## Lab Modules

The use cases we will cover are the following which you can access via the links below:

1. [**Python Orientation**](./python-0-orientation/01-intro.md)
2. [**Building Hierarchy**](./python-1-hierarchy/01-intro.md)
3. [**Assign Settings and Credentials**](./python-2-settings/01-intro.md)
4. [**Device Discovery**](./python-3-discovery/01-intro.md)
5. [**Template Deployment**](./python-4-templates/01-intro.md)

## Preparation Notes

To complete this module, it's best to connect to the dCloud lab environment using your laptop so that you can get accustomed to and begin using the tools. If you cannot install python, completing all tasks via the workstation in the dCloud environment is possible via the script server.

Our screenshots will all be from the jump host but remember you can use your laptop.

If you would like to connect to the DCLOUD environment, please ensure you install the following.

### Lab Requirements

#### The DCLOUD Environment

For DevNet Test Drive events, use this environment: [DNAC pods for DevNet Test Drives](https://tbv3-ui.ciscodcloud.com/edit/9uxy98sb1wresh3vrw60lfsa7)

The DCLOUD session includes the following equipment:

* Virtual Machines:
  * Cisco Catalyst Center 2.3.5.6 or better
  * Identity Services Engine (ISE) 3.0 Patch 4 or better (deployed)
  * Script Server - Ubuntu 20.04  or better
  * Windows 10 Jump Host 
  * Windows Server 2019 - Can be configured to provide identity, DHCP, DNS, etc.

* Virtual Networking Devices:
  * Catalyst 8000v Router - 17.06.01a IOS-XE Code
  * Catalyst 9300v Switch - 17.12.01 IOS-XE Code 

The following diagram shows the DCLOUD topology.

![DCLOUD LAB TOPOLOGY](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_A.png?raw=true)

The following diagram shows one of the CML pods topology.

![DCLOUD CML POD TOPOLOGY](../../ASSETS/COMMON/DCLOUD/DCLOUD_Topology_B.png?raw=true)

#### Management IPs:

This is the pod IP addressing schema that will be used to discover devices within the lab.
Your instructor will assign you a pod number:

| Pod: | Router:     | gi 1         | Switch 1:   | gi 0/0      | Switch2:    | gi 0/0      |
|------|-------------|--------------|-------------|-------------|-------------|-------------|
| 0    | c8000v-p0-1 | 198.18.140.1 | c9000v-p0-1 | 198.18.10.2 | c9000v-p0-2 | 198.18.20.2 |
| 1    | c8000v-p1-1 | 198.18.141.1 | c9000v-p1-1 | 198.18.11.2 | c9000v-p1-2 | 198.18.21.2 |
| 2    | c8000v-p2-1 | 198.18.142.1 | c9000v-p2-1 | 198.18.12.2 | c9000v-p2-2 | 198.18.22.2 |
| 3    | c8000v-p3-1 | 198.18.143.1 | c9000v-p3-1 | 198.18.13.2 | c9000v-p3-2 | 198.18.23.2 |
| 4    | c8000v-p4-1 | 198.18.144.1 | c9000v-p4-1 | 198.18.14.2 | c9000v-p4-2 | 198.18.24.2 |
| 5    | c8000v-p5-1 | 198.18.145.1 | c9000v-p5-1 | 198.18.15.2 | c9000v-p5-2 | 198.18.25.2 |
| 6    | c8000v-p6-1 | 198.18.146.1 | c9000v-p6-1 | 198.18.16.2 | c9000v-p6-2 | 198.18.26.2 |
| 7    | c8000v-p7-1 | 198.18.147.1 | c9000v-p7-1 | 198.18.17.2 | c9000v-p7-2 | 198.18.27.2 |
| 8    | c8000v-p8-1 | 198.18.148.1 | c9000v-p8-1 | 198.18.18.2 | c9000v-p8-2 | 198.18.28.2 |
| 9    | c8000v-p9-1 | 198.18.149.1 | c9000v-p9-1 | 198.18.19.2 | c9000v-p9-2 | 198.18.29.2 |

#### Credentials:

| Platform:       | IP Address:    | Username | Password   | 
|-----------------|----------------|----------|------------|
| Catalyst Center | 198.18.129.100 | admin    | C1sco12345 |
| ISE             | 198.18.133.27  | admin    | C1sco12345 |
| Windows AD      | 198.18.133.1   | admin    | C1sco12345 |
| Script Server   | 198.18.133.28  | root     | C1sco12345 |
| Router          | 198.18.14[X].1 | netadmin | C1sco12345 |
| Switch 1        | 198.18.1[X].2  | netadmin | C1sco12345 |
| Switch 2        | 198.18.2[X].2  | netadmin | C1sco12345 |

#### DCLOUD VPN Connection

Use AnyConnect VPN to connect to DCLOUD. When connecting, look at the session details and copy the credentials from the session booked into the client to connect.

![DCLOUD VPN CONNECTION](../../ASSETS/COMMON/DCLOUD/VPN-to-DCLOUD.png)

## Tools Required

Please utilize the following tools to run the lab effectively and ensure they are installed on your workstation/laptop before attempting the lab.

1. Cisco AnyConnect VPN Client
2. Python and Python SDK
3. Google Chrome

### Cisco AnyConnect VPN Client

This software is required to connect your workstation to Cisco DCLOUD. For an explanation of AnyConnect and how to use it with DCLOUD, please visit the following URL: 

> **Documentation**: For AnyConnect Documentation visit: <a href="https://DCLOUD-cms.cisco.com/help/android_anyconnect" target="_blank">DCLOUD AnyConnect Documentation</a>

> **Download**: Get AnyConnect here: <a href="https://DCLOUD-rtp-anyconnect.cisco.com" target="_blank">⬇︎ AnyConnect Download Site ⬇︎</a>

### Python and Catalyst Center SDK

Python will be used in this Lab to interact with Catalyst Center using REST API through use of the Catalyst Center Python SDK and normal HTTP Requests. As previously stated, the combination of Python programming language with the rich Cisco Catalyst Center API collection offers the utmost flexibility and power in developing custom applications or workflows.

As with any other Vendor Automation Controller, Cisco Catalyst Center Rest API capabilities get extended and maintained with each new release of Cisco Catalyst Center software. This presents a challenge to a Python developer, as code REST API syntax and parameters may change over time requiring the developer to revisit earlier developed code. To help developers abstract from Cisco Catalyst Center specific version implementation, [Cisco Catalyst Center SDK](https://dnacentersdk.readthedocs.io/en/latest/api/api.html) toolkit was introduced.

Simply put, SDK is a set of tools, libraries and documentation to simplify interacting with a REST API. The Cisco Catalyst Center SDK is written in Python and provides a Python library in PyPI and associated documentation. PyPI is the official python package index, and simplifies installation of the library. 

#### Python Installation, (Linux or MAC)

Install Homebrew package manager

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install PyEnv using HomeBrew. PyEnv is a CLI utility that helps you manage Python installations on your computer.

```shell
brew install pyenv
pyenv init

nano ~/.zshrc
Paste the eval line at the end of the file
eval "$(pyenv init -)"

press Control + X, type Y and press Enter when prompted for the file name

Now that PyEnv is installed and configured, exit and reload the Terminal
```

With PyEnv is installed and configured, we can install Python. Example below is installing Python version 3.9.1

```shell
pyenv install 3.9.1
pyenv global 3.9.1
```

And finally, verification of installed Python environment

```shell
pyenv version
```

Lets ensure that we have Python module manager PIP installed

```shell
python -m ensurepip --upgrade
```

#### Python Installation, (Windows)

[Installing Python](https://www.python.org/downloads/) - Python distributions

Lets ensure that we have Python module manager PIP installed

```shell
python -m ensurepip --upgrade
```

#### Cisco Catalyst Center SDK Installation

To isolate the installation folder structure from other libraries create a virtual environment, and activate it. Each time you want to come back and make changes to your code please remember to activate the virtual environment in your terminal (see below)

```shell
python -m venv dnacentersdk
source dnacentersdk/bin/activate
```

* Install Cisco Catalyst Center SDK in newly created virtual environment

```shell
pip install dnacentersdk
```

The SDK is ready for use!

### Google Chrome

Google Chrome is the optimal browser of choice when working in the DNA Center UI. 

> **Download**: Get Google Chrome here: <a href="https://www.google.com/chrome/downloads/" target="_blank">⬇︎ Chrome Download ⬇︎</a>

## Summary

This lab is intended for educational purposes only. Use outside of a lab environment should be done at the operator's risk. Cisco assumes no liability for incorrect usage.

This lab is intended to help drive the adoption of Rest-API and will be added to over time with various use cases. The Public Workspace will also mirror the changes and be kept up to date. We hope this set of labs helps explain how the Rest-API may be used and goes a little further in helping define and document them.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to LAB Main Menu**](../README.md)
