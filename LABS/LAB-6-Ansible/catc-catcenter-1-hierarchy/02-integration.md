# Review ISE Integration

In this module our focus changes slightly as we start to automate host and device onboarding. A large component of host onboarding is the authentication of hosts and assignments within the network.

In this section, and in preparation for the steps that follow, we verify that Catalyst Center is integrated with **Identity Services Engine (ISE)**. This integration enables pxGrid communication between Catalyst Center and ISE. The **PxGrid persona** must be enabled on at least one ISE node in the cluster — this has **already been completed** in the DCLOUD sandbox.

PxGrid integration allows Catalyst Center to automate ISE configuration for Network Access Devices, SGT creation, and SGACL builds via Contracts and Policy.

## Step 1: Verify ISE is Prepared for Integration

1. Open a web browser to [**Identity Services Engine (ISE)**](https://198.18.133.27) and select the hamburger menu to open the system menu.

   * username: `admin`
   * password: `C1sco12345`

   ![ISE Dashboard](../../../ASSETS/LABS/COMMON/ise/ise-dashboard.png?raw=true)

2. From the system menu under Administration, select **PxGrid Settings**.

   ![ISE Menu](../../../ASSETS/LABS/COMMON/ise/ise-menu.png?raw=true)

3. On the PxGrid Settings page, verify both options have been selected and saved to allow Catalyst Center integration.

   ![ISE PxGrid](../../../ASSETS/LABS/COMMON/ise/ise-pxgrid-settings.png?raw=true)

   ![ISE PxGrid Setup](../../../ASSETS/LABS/COMMON/ise/ise-pxgrid-setup.png?raw=true)

## Step 2: Verify Catalyst Center and ISE Integration

1. Open a web browser to [**Catalyst Center**](https://198.18.129.100), select the hamburger menu, and navigate to **System → Settings**.

   * username: `admin`
   * password: `C1sco12345`

   ![Catalyst Center Settings](../../../ASSETS/LABS/COMMON/platform/catc-system-settings.png?raw=true)

2. Within the System Settings page, navigate down the list on the left and select the **Authentication and Policy Server** section.

   ![Catalyst Center AAA Settings](../../../ASSETS/LABS/COMMON/platform/catc-system-settings-aaa.png?raw=true)

3. On the page you should see the ISE node integrated with Catalyst Center as shown below.

   ![Catalyst Center ISE Integrated](../../../ASSETS/LABS/COMMON/platform/catc-system-settings-aaa-ise-complete.png?raw=true)

> [**Next Section**](./03-deploy.md)

> [**Return to LAB Menu**](../README.md)
