# Preparing Postman for use with Catalyst Center

To use Postman with Catalyst Center, we import the collection and environment into our workspace.

## Postman Collection and Environment Import

To prepare Postman for the lab, please download the following collection and environment zip file and upload them into Postman. Download the following Student Collection, which includes seven collections and one environment. To do this right, click and open this link in a new tab to download them:

> **Download**: <a href="https://git-link.vercel.app/api/download?url=https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/CatalystCenter-UseCase-API-Collection.zip" target="_blank">⬇︎ Catalyst Center Use-Case API Collection ⬇︎</a>

After you download the file, decompress the compressed files and import all the files into Postman.

Follow these steps:

1. Click on the Postman shortcut on the desktop.

   ![Postman icon](./assets/Postman.png)

2. Click **Import**. A window for importing files appears.

   ![Postman Import Begin](./assets/Postman-Import-Begin.png)

3. Click **Upload File** to begin the file select process.

   ![Postman Import Files](./assets/Postman-Import-File.png)

4. Select the files from the Student Folder and click **Open**.

   ![Postman Import Select](./assets/Postman-Import-Select-Open.png)

5. Postman shows a list of files ready for import. Click **Import**.

   ![Postman Import Upload](./assets/Postman-Import-Upload.png)

6. Confirm all the Collections in the image are present. 

   ![Postman Collections](./assets/Postman-Collection-Confirm.png)

7. Confirm that the environment is present.

   ![Postman Environments](./assets/Postman-Environment-Confirm.png)

## Postman Environment Variables

Next, set up the client with the correct environment variables and SSL settings.

To ensure uniformity across all calls made from the client when we use different collections, we use Environmental Variables. These variables form a database that can be used in many collections. Also, the variables enable you to build specific collections for many functions to devote them to specific use cases.

1. Navigate to the environment on the left sidebar.

2. Hover over the environment in the list. Notice a box to set it to **Active**.

   ![Environment with check box](./assets/Postman-Environment-Check.png)

3. Select the check box.

   ![Active environment](./assets/Postman-Environment-Active.png)

> **Note**: This environment is pre-populated with the information to build Catalyst Center. At specific points in the lab, we will **customize** it for **your use**.

## SSL Settings and Disabling Validation

For Lab purposes, Catalyst Center uses a self-signed certificate. This certificate may fail a validation pre-check. Disable this setting to proceed with the Lab.

1. Click the Settings gear icon on the top right of Postman.

   ![Postman Settings Menu](./assets/Postman-Settings-Menu.png)

2. In the Settings window, deselect **SSL certificate verification**.

    ![Disabled SSL Validation](./assets/Postman-Settings-SSL-Validation-Off.png)

3. Close the settings window.

> [**Next Section**](./04-externaldata.md)

> [**Return to LAB Menu**](../README.md)