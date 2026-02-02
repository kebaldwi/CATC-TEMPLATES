# Postman and External Data Sources

Within Postman, we will utilize the collection `Build Hierarchy` to build out the Hierarchy of Cisco Catalyst Center into which we associate `settings` and `discover devices`. 

This Collection may be run whenever you wish to create a new section of the Hierarchy to **add** additional `Areas`, `Buildings`, or `floors`. 

Accompanying the Collection is a **required** Comma Separated Value (CSV) file, which is essentially an `answer file` for the values used to build the design. The CSV may be found here. 

> **Download**: Navigate to [this github repo](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/DEVNET-IGNITE/PODS) and select the csv file corresponding to your **POD NUMBER**

Click the "Download Raw File" ⬇️ button to download the csv

![CSV file for collection run](./assets/csv_download.png)

## *Optional review of CSV file*

<details closed><summary> Click to Display the Optional review of CSV file </br></br>

Use this section optionally to validate your downloaded CSV to make sure it conforms to your POD, follow the steps below. Otherwise if you **correctly** downloaded one of the pre-populated csv's above continue to the **next section**

</summary>

### Preparing the External Data File

#### Preparing Visual Studio Code

We will use **Visual Studio Code** to open the file, or alternative editor. Open **Visual Studio Code** from the task bar. 

![Visual Studio Code](./assets/vscode.png)

We will the install the CSV Editor, by selecting **Extensions**, searching for `CSV` then clicking **Install** link beside `Excel Viewer`. Once installed we can then **open and edit** the **CSV** for our use.

![VS Code CSV Editor](./assets/vscode-csveditor.png)

#### Editing the External Data File in Visual Studio Code

Next we will open the extracted CSV file within the download directory. Select the **Explorer** icon on the menu and click **Open Folder** and browse to the `Download` directory and select it. 

![VS Code Opening Directory](./assets/vscode-directory.png)

Expand the `Downloads` directory in the Explorer page to reveal the file **CCC-Design-Settings-v3.csv**.

**Right click** the file and select **Open with...** 

![VS Code Opening CSV](./assets/vscode-csv-open.png)

Then choose **CSV Editor** from the list at the top of the screen. You should then be able to resize the window and navigate it to paste in the information from the table below **RELEVANT** to **YOUR POD**.

![VS Code Opening CSV editor](./assets/vscode-csveditor-open.png)

#### POD Specific information

Below are the fields which will correspond to your version of the **CSV** file. **Do not edit the file** instead **download the correct one**.

|Hierarchy Area|Hierarchy Bldg|Hierarchy Floor|Hierarchy Parent|Hierarchy Bldg Address|Device List|
|--------------|--------------|---------------|----------------|----------------------|-----------|
|[POD 0](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD0_CCC-Design-Settings-v3.csv)|Building P0|Floor 1|Global/PODS|300 E Tasman Dr, Bldg 10, San Jose, CA 95134|198.18.140.1,198.18.10.2,198.18.20.2|
|[POD 1](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD1_CCC-Design-Settings-v3.csv)|Building P1|Floor 1|Global/PODS|3850 Zanker Rd, Bldg 1, San Jose, CA 95134  |198.18.141.1,198.18.11.2,198.18.21.2|
|[POD 2](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD2_CCC-Design-Settings-v3.csv)|Building P2|Floor 1|Global/PODS|3800 Zanker Rd, Bldg 2, San Jose, CA 95134  |198.18.142.1,198.18.12.2,198.18.22.2|
|[POD 3](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD3_CCC-Design-Settings-v3.csv)|Building P3|Floor 1|Global/PODS|225 E Tasman Dr, Bldg 3, San Jose, CA 95134 |198.18.143.1,198.18.13.2,198.18.23.2|
|[POD 4](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD4_CCC-Design-Settings-v3.csv)|Building P4|Floor 1|Global/PODS|275 E Tasman Dr, Bldg 4, San Jose, CA 95134 |198.18.144.1,198.18.14.2,198.18.24.2|
|[POD 5](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD5_CCC-Design-Settings-v3.csv)|Building P5|Floor 1|Global/PODS|325 E Tasman Dr, Bldg 5, San Jose, CA 95134 |198.18.145.1,198.18.15.2,198.18.25.2|
|[POD 6](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD6_CCC-Design-Settings-v3.csv)|Building P6|Floor 1|Global/PODS|375 E Tasman Dr, Bldg 6, San Jose, CA 95134 |198.18.146.1,198.18.16.2,198.18.26.2|
|[POD 7](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD7_CCC-Design-Settings-v3.csv)|Building P7|Floor 1|Global/PODS|425 E Tasman Dr, Bldg 7, San Jose, CA 95134 |198.18.147.1,198.18.17.2,198.18.27.2|
|[POD 8](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD8_CCC-Design-Settings-v3.csv)|Building P8|Floor 1|Global/PODS|3750 Zanker Rd, Bldg 8, San Jose, CA 95134  |198.18.148.1,198.18.18.2,198.18.28.2|
|[POD 9](https://github.com/kebaldwi/CATC-TEMPLATES/blob/master/CODE/POSTMAN/DEVNET-IGNITE/PODS/POD9_CCC-Design-Settings-v3.csv)|Building P9|Floor 1|Global/PODS|260 E Tasman Dr, Bldg 9, San Jose, CA 95134 |198.18.149.1,198.18.19.2,198.18.29.2|

Use the information within the table above to validate our **CSV** file ais correct. For this and subsequent examples we will assume we are using **POD 0** 

#### **Step 1**: Verifying the Hierarchy for the POD **(REQUIRED)**

Lets verify the 3rd line of the CSV with the correct POD information with the following: 

> *Note:* *Do not modify any fields*

1. Lets verify the **Hierarchy Area** with the correct POD Number
2. Lets verify the **Hierarchy Building**  
3. Lets verify the **Hierarchy Floor**
4. Lets verify the **Hierarchy Building Address**

So it looks like this but for your **POD**.

![VS Code CSV edits for Hierarchy](./assets/csv-edit-hierarchy.png)

#### **Step 2**: Verifying the Device List for the POD **(REQUIRED)**

Lets verify the 3rd line of the CSV with the correct POD information with the following: 

> *Note:* *Do not modify any fields*

1. Lets verify the **Device List** as indicated above

So it looks like this but for your **POD**.

![VS Code CSV edits for Devices](./assets/csv-edit-devices.png)

We will then **close** the CSV file as this will be used to build the hierarchy during the lab. 

As you review the CSV file, you will see each row has hierarchal information, settings, credentials, and other information. **Be Careful NOT to modify the file further**; if you feel you have modified the file incorrectly, please **download it again** and repeat the process.

</details>

The hierarchy the CSV will build will be this:

```text
Global >
Global > PODS
Global > PODS > POD 0 > Building P0 > Floor1
```

## Summary

You have set up the Postman client with a collection, the environment, and the settings to complete the Lab. In the following sections, you use environment variables within each collection to perform a task on Cisco Catalyst Center.

We have performed a few operations in the client, and you have seen the Collections where the REST APIs are configured and the Environment where the data is stored in variables within the database.

> **Note**: Before you continue, you may take additional time to familiarize yourself with Postman.

> [**Next Module**](../catc-catcenter-1-hierarchy/01-intro.md)

> [**Return to LAB Menu**](../README.md)