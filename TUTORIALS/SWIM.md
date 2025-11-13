# Software Image Management (SWIM) and Catalyst Center [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

## What is Software Image Management?

**Software Image Management** refers to the process of controlling and maintaining software versions and configurations across devices in a network. This discipline ensures that the correct software images are deployed, updated, and managed efficiently, which is crucial for maintaining optimal device performance and security. Effective software image management helps organizations streamline their operations, reduce downtime, and ensure compliance with software standards.

## How is Software Image Management used with Catalyst Center?

**Software Image Management** is integrated into the Catalyst Center to provide a centralized platform for managing software images across network devices. This functionality allows network administrators to automate the deployment of software updates, monitor image compliance, and ensure that all devices are running the correct versions of software. By leveraging software image management capabilities, organizations can enhance their network reliability and security while minimizing manual intervention.

## What can Software Image Management do for Catalyst Center?

**Software Image Management** with Catalyst Center can be utilized for a range of tasks, including:

1. **Image Deployment**: Automatically deploy the latest software images to network devices, ensuring that all devices are up-to-date and secure.

2. **Version Control**: Maintain a repository of software images, allowing for easy rollback to previous versions if necessary.

3. **Compliance Monitoring**: Continuously monitor devices to ensure they are running the approved software images, helping maintain compliance with organizational policies.

4. **Automated Updates**: Schedule and automate software updates to minimize downtime and reduce the operational burden on IT staff.

5. **Image Validation**: Validate software images before deployment to ensure compatibility and prevent issues in the network.

6. **Validation Checks**: Pre, Post checks cand be completed on Distribution and Activation to include custom checks added by the administrator.

7. **Integration with CI/CD Pipelines**: Integrate software image management with Continuous Integration and Continuous Deployment (CI/CD) practices, enabling rapid and reliable software updates.

Overall, **Software Image Management** with Catalyst Center simplifies the process of maintaining software across devices, reduces operational risks, and enhances overall network performance and security.

---

## REST API and Orchestration of Software Image Management

**REST APIs** play a critical role in the orchestration of Software Image Management (SWIM) by enabling seamless integration with various IT service management (ITSM) platforms like **ServiceNow** and Infrastructure as Code (IaC) practices. 

### Integration with ServiceNow ITSM

By leveraging REST APIs, organizations can automate workflows between Catalyst Center and ServiceNow. This integration allows for:

- **Incident Management**: Automatically create incidents in ServiceNow when software image compliance issues are detected, streamlining the response process.
- **Change Management**: Manage software updates and changes through ServiceNow, ensuring that all changes are tracked and approved according to organizational policies.
- **Reporting and Analytics**: Utilize ServiceNow’s reporting capabilities to analyze software image deployment and compliance metrics, providing insights for better decision-making.

### Infrastructure as Code (IaC)

Integrating SWIM with IaC practices allows organizations to define and manage their infrastructure through code, enhancing automation and consistency. REST APIs facilitate this by enabling:

- **Automated Provisioning**: Automatically provision network devices with the correct software images as part of the deployment process, reducing the potential for human error.
- **Configuration Management**: Use tools like Terraform or Ansible to manage software image versions and configurations as code, allowing for version control and repeatable deployments.
- **Continuous Deployment**: Incorporate software image updates into CI/CD pipelines, ensuring that the latest images are automatically deployed in a controlled manner.

Overall, the combination of REST APIs and orchestration through ITSM platforms and IaC practices enhances the efficiency and reliability of Software Image Management, allowing organizations to maintain optimal network performance and security while reducing operational risks.

---

## Operation of Software Image Management (SWIM)

**Software Image Management (SWIM)** in the Catalyst Center provides a streamlined approach to managing software images across network devices. SWIM allows network administrators to automate the deployment, validation, and compliance of software images, ensuring that all devices run the correct versions of software for optimal performance and security.

### Golden Images

#### What are Golden Images?

**Golden images** are pre-configured software images that serve as the baseline for deploying software across multiple devices. These images are tested and verified to ensure they meet organizational standards and requirements. By using golden images, organizations can minimize inconsistencies and reduce the time required for software deployment.

#### TAG's Hierarchy and Roles

The **Hierarchy, Roles** and **TAG's** in Catalyst Center play a critical role in aligning the right golden images for deployment:

![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-image-management.png?raw=true "Software Image Management")

- **Hierarchy**: This structure allows administrators to categorize devices based on their specific requirements and characteristics. Each part of the hierarchy can include different factors such as device type, and location, or function, enabling targeted deployments of golden images. In the image above you will notice hte Golden Image for the DEMO site. 
  
- **Roles**: By assigning roles to devices, administrators can ensure that only the appropriate golden images are deployed to specific groups. For example, a role assigned to access switches may require a different golden image than that of border routers.

- **TAG's** This structure allows administrators to categorize devices based on their use case specific requirements and characteristics. Each tag can represent different factors such as device type, feature, or function, enabling targeted deployments of golden images. These TAGs may mirror those used in Templates.

By leveraging TAG's Hierarchy and Roles, organizations can effectively manage which golden images are deployed to which devices, ensuring compliance and optimizing network performance.

#### Golden Images in Plug and Play (PnP)

In the context of **Plug and Play (PnP)**, golden images are utilized to simplify the onboarding process of new devices. When a new device is connected to the network, it can automatically retrieve its designated golden image based on its TAG and Role. This automation reduces manual configuration efforts and accelerates device deployment, ensuring consistency across the network.

---

### Readiness, Pre and Post Checks

There are essentially three separate checks which can be completed when automating through Software Image Management. Seen in the image below they are the following: 

- **Image Readiness Check** which checks the target system readiness

  ![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-ReadinessCheck.png?raw=true "Software Image Management")

- **Software Distribution** which carries out pre and post checks for distribution of the target system

  ![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Distribution-Checks.png?raw=true "Software Image Management")

- **Software Activation** which carries out pre and post checks for activation of the target system.

  ![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Activation-Checks.png?raw=true "Software Image Management")

- **Custom Checks** which allow additional checks of the target system.

  ![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Custom-Checks.png?raw=true "Software Image Management")

---

### Image Deployment Options

There are essentially three separate actions to automate through Software Image Management. The steps typically include:

- **Select the Golden Image**: Choose the appropriate golden image based on TAGs and Roles. and assign to the devices via Hierarchy, Role and TAG.

Then to deploy the images we use the following:

- **Software Distribution** which is transfering the image to the target system
- **Software Activation** which is activating (using) the image on the target system.

### 1. Deploying and Activating the Image in the Same Workflow

In this method, the deployment and activation of the software image occur within a single workflow. This approach is efficient for scenarios where immediate activation is required. 

During the Deployment of Software use Deploy and Activate the image after deployment. This includes:

- **Distribute the Image**: Push the image to the target devices.
- **Activate the Image**: Automatically activate the image once deployment is complete

This method is ideal for environments where downtime is minimal, and quick updates are necessary. During this type of upgrade both the **Distribution** and **Activation** would be completed in a **single workflow** as seen here.

![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Distribution-Activation.png?raw=true "Software Image Management")

### 2. Deploying (Staging) and Activating the Image in Separate Workflows

This approach involves two distinct workflows: one for staging the image and another for activation. This includes:

- **Staging the Image**: Distribute the golden image to the target devices without activating it immediately. This allows for testing and validation.
- **Activating the Image**: Once the image has been verified, a separate workflow is initiated to activate the image on the devices.

This method provides greater control and flexibility, allowing administrators to ensure that the images are functioning correctly before activation. During this type of upgrade both the **Distribution** and **Activation** would be completed in a **separate workflows** as seen here. In the first workflow you can see we have **SKIPPED** **Activation** and thus the image is only **Distributed**.

![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Distribution-Skip-Activation.png?raw=true "Software Image Management")

In the second workflow you can see we complete the **Activation** of the image.

![Software Image Management](../ASSETS/TUTORIALS/SWIM/SWIM-Activation.png?raw=true "Software Image Management")

---

### Image Distribution Server

An **Image Distribution Server** plays a crucial role in the deployment of software images. This server acts as a centralized repository where golden images are stored and managed. This is assigned in the **Network Settings** within the Design.

#### How Images are Deployed

- **Centralized Management**: Administrators can manage all software images from a single location, making it easier to track versions and updates.
- **Efficient Distribution**: The server facilitates the distribution of images to multiple devices simultaneously, reducing the time required for deployment.
- **Version Control**: By maintaining a repository of images, organizations can easily roll back to previous versions if necessary, ensuring stability in the network.

---

### Mode Conversion for INSTALL and BUNDLE

We have two modes a Catalyst switch can operate in. The are the following:

#### Bundle Mode

Bundle mode is a fancy way to say that switch runs the traditional way of Cisco IOS®. You **boot** a **.bin file** that contains everything you need to run the Cisco IOS. As per traditional Cisco IOS, you have a boot statement that points to the .bin file you want to load and that gets loaded at the time of boot. This means the switch unpacks the OS every time it boots which takes longer.

#### Install Mode

Install mode is the newer and recommended mode to run. This **breaks** the **.bin file** up into smaller **.pkg files** that must be loaded into memory independently of each other, and allows you to boot faster and utilize memory better. The .bin file that you download from software.cisco.com has all the .pkg files you need inside.

#### Mode Conversion

To convert between modes there is a process which must be followed in order to ensure success. In order to alleviate the burden of conversion I have developed a template which allows the conversion process to be scheduled.

In order to use this template you would do the following process:

1. **Distribute** and **SKIP** **Activation** of the **new IOS-XE version** to the switch. (**caveat** the image distributed **must be newer** than the existing image)
2. Provision the template converting the mode to the switch ensuring the date and time for the conversion are used. <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TEMPLATES/JINJA2/UTILITIES/JSON/Mode_Conversion_Template.json">⬇︎Mode_Conversion_Template.json⬇︎</a></br>

The template will take care of the rest.

---

### Monitoring and Control via ServiceNow

**SWIM** can be effectively monitored and controlled through **ServiceNow**, an IT service management platform. Integration with ServiceNow allows organizations to:

- **Automate Incident Management**: Automatically create incidents in ServiceNow when issues related to software images are detected.
- **Change Management**: Manage and track changes to software images through ServiceNow, ensuring compliance with organizational policies.
- **Reporting and Analytics**: Utilize ServiceNow's reporting tools to gain insights into software image deployments, compliance status, and operational metrics.

By leveraging ServiceNow, organizations can enhance their operational efficiency and ensure that software image management aligns with broader IT service management practices.

---

## Summary

In summary, **SWIM** in the Catalyst Center simplifies the management of software images through the use of golden images, structured deployment options, centralized distribution, and integration with ITSM tools like ServiceNow. This approach not only enhances network reliability but also streamlines operational processes.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Main Menu**](../README.md)