# Review ISE Integration

In this module, our focus changes slightly as we start to automate host and device onboarding. A large component of host onboarding is the authentication of hosts and assignments within the network. 

In this section, and in preparation for the steps which follow, we will integrate Catalyst Center with Identity Services Engine. This integration allows pxGrid communication between the Catalyst Center and ISE. For this reason, the **PxGrid** **persona** does need to be enabled on at least 1 ISE Node within an ISE Cluster. This has **already been completed** in the sandbox. 

PxGrid integration allows configuration automation by Catalyst Center within ISE for Network Access Devices, SGT creation, and SGACL builds via Contracts and Policy.

## Step 1: Verify ISE is Prepared for Integration

1. Open a web browser connection to [**Identity Services Engine (ISE)**](https://198.18.133.27) and select the hamburger menu to open the system menu.

   * username: `admin`
   * password: `C1sco12345`

   ![ISE Dashboard](../../../ASSETS/LABS/COMMON/ise/ise-dashboard.png?raw=true)

2. From the system menu under Administration, select PxGrid Settings

   ![ISE Menu](../../../ASSETS/LABS/COMMON/ise/ise-menu.png?raw=true)

3. On the PxGrid Settings page, verify both options have been selected and saved to allow for Catalyst Center to integration.

   ![ISE PxGrid](../../../ASSETS/LABS/COMMON/ise/ise-pxgrid-settings.png?raw=true)
   
   ![ISE PxGrid](../../../ASSETS/LABS/COMMON/ise/ise-pxgrid-setup.png?raw=true)

## Step 2: Verify Catalyst Center and ISE Integration

1. Open a web browser connection to [**Catalyst Center**](https://198.18.129.100), select the hamburger menu, and navigate to the System > Settings menu item.

   * username: `admin`
   * password: `C1sco12345`

   ![Catalyst Center Settings](../../../ASSETS/LABS/COMMON/platform/catc-system-settings.png?raw=true)

2. Within the System Settings page, navigate down the list on the left and select the Authentication and Policy Server section.

   ![Catalyst Center AAA Settings](../../../ASSETS/LABS/COMMON/platform/catc-system-settings-aaa.png?raw=true)

3. On the page, you will see the ISE node integrated with Catalyst Center as shown below.

   ![Catalyst Center ISE Integrated](../../../ASSETS/LABS/COMMON/platform/catc-system-settings-aaa-ise-complete.png?raw=true)

> [**Next Section**](./03-deploy.md)

> [**Return to LAB Menu**](../README.md)