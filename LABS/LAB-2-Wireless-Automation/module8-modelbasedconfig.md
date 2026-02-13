# Model-Based Configuration

In this subsection we will design and provision the Wireless Controller with model-based configurations to augment the wireless settings of WLAN's. Whenever a new WLAN or a configuration change is made, the change will need to be provisioned to the controller using this process. The Model-Based Configurations may be added to the wireless profiles to modify settings for the wireless SSID that are provisioned by Catalyst Center.

The various use cases for model-based configuration are as follows:

1. **AAA Radius Attributes Configuration** - *(Modify Called Station ID)*
2. **Advanced SSID Configuration** - *(General, Client and SSID Data Rates, 802.AX)*
3. **CleanAir Configuration** - *(Enabling, Interferer Features)*
4. **Dot11ax Configuration** - *(AX BSS Color etc)*
5. **Event Driven RRM Configuration** - *(Enabling EDRRM and Sensitivity Thresholds)* - *(in 2.3.5.x)*
6. **Flex Configuration** - *(IP Overlap)*
7. **Global IPv6 Configuration** - *(Global IPv6)*
8. **Multicast Configuration** - *(Enabling Multicast Globally for Unicast or Multicast)*
9. **RRM FRA Configuration** - *(Enabling Flexible Radio Assignment)* - *(in 2.3.5.x)*
10. **RRM General Configuration** - *(Thresholds, Monitoring and Coverage)* - *(in 2.3.5.x)*

## Model-Based Configuration Scenario

In this module we will go through a scenario which explains the ways that you can use and implement the various configurations for differing use cases in a way that makes sense.

As we have 4 SSID's our scenario will be as such:

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-PSK      | PHONES         | P2P, Voice, Video, DHCP Req'd                |
| CAMPUS-EAP      | DATA & VOICE   | P2P, VMware Fusion, Voice, Video, DHCP Req'd |
| GUESTNET        | GUEST TRAFFIC  | No P2P, VMware Fusion, DHCP Req'd            |

<details open>
<summary> Click the arrow for details</summary>

## Section 1 - **Create Model-Based Configurations**

1. Open a web browser on the Windows Workstation Jump host. Open a connection to Catalyst Center and select the hamburger menu icon to open the menu. Select **`Tools > Model Config Editor`**.

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-navigation.png?raw=true "Import JSON")

### Step 1 - **Create AAA Configuration**

Sometimes it is required to send additional information in the RADIUS request. To insert information about the SSID, or loaction or AP MAC address for instance from the called station id. In this step we will modify the global parameter for RADIUS in the wireless configurations for the controller.

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **AAA Radius Attributes Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-aaa-1.png?raw=true "Import JSON")

   3. Enter a Name for the Design Element, `AAA`
   4. From the dropdown select the value `ap-macaddress-ssid` for the **Called Station Id**
   5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-aaa-2.png?raw=true "Import JSON")

### Step 2 - **Create SSID Configurations**

In this section we have three scenarios we will deal with from above, as detailed in the following table. We have a set of wireless requirements for the 8821 ip phones on the PSK SSID. Additionally a data and voice requirment which is needed on the IPSK and EAP SSID's. Lastly a Guest network requirement. Lets build out the model based configurations which will be applied to the 4 SSID mentioned. 

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-PSK      | PHONES         | P2P, Voice, Video, DHCP Req'd                |
| CAMPUS-EAP      | DATA & VOICE   | P2P, VMware Fusion, Voice, Video, DHCP Req'd |
| GUESTNET        | GUEST TRAFFIC  | No P2P, VMware Fusion, DHCP Req'd            |

#### Step 2a - **Create Voice SSID Configuration**

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Advanced SSID Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-1.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `VOICE`
      2. From the dropdown for **DHCP Required** select the value `YES`
      3. Enable the slider as shown for **Aironet IE**
      4. Set the **DTIM period** to **2** for both the **2.4 and 5 Ghz** networks
      5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-2.png?raw=true "Import JSON")

#### Step 2b - **Create Guest SSID Configuration**

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Advanced SSID Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-3.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `GUEST`
      2. From the dropdown for **Peer to Peer Blocking** select the value `DROP`
      3. Enable the slider as shown for **Passive Client Enable**
      4. From the dropdown for **DHCP Required** select the value `YES`
      5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-4.png?raw=true "Import JSON")

#### Step 2c - **Create Internal SSID Configuration**

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Advanced SSID Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-5.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `EMPLOYEE`
      2. Enable the slider as shown for **Passive Client Enable**
      3. From the dropdown for **DHCP Required** select the value `YES`
      4. Set the **DTIM period** to **2** for both the **2.4 and 5 Ghz** networks
      5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ssid-6.png?raw=true "Import JSON")

### Step 3 - **Create CleanAir Configuration**

To enable CleanAir on a Wireless Controller, you can do that for each band. In the lab lets do this for the 2.4 and 5 Ghz bands.

#### CleanAir Configuration for 2.4 Ghz

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Clean Air Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ca-1.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `CA-24`
      2. From the dropdown for **Radio Band** select the value `2.4 Ghz`
      3. Enable the sliders as shown for:
         * **CleanAir Enable**
         * **CleanAir Device Reporting Enable**
         * **Persistant Device Propogation**
      4. From the **Enable Interferer Features** section select:
         * **Generic DECT**
         * **Jammer**
         * **Microwave Oven**
         * **Video Camera**
      5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ca-2.png?raw=true "Import JSON")

#### CleanAir Configuration for 5 Ghz

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Clean Air Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ca-3.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `CA-5`
      2. From the dropdown for **Radio Band** select the value `5 Ghz`
      3. Enable the sliders as shown for:
         * **CleanAir Enable**
         * **CleanAir Device Reporting Enable**
         * **Persistant Device Propogation**
      4. From the **Enable Interferer Features** section select:
         * **Generic DECT**
         * **Jammer**
         * **Video Camera**
      5. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-ca-4.png?raw=true "Import JSON")

### Step 4 - **Create EDRRM Configuration**

To enable Event Driven RRM (EDRRM) for the wireless controller for the 2.4 and 5 Ghz radios complete the following:

#### EDRRM Configuration for 2.4 Ghz

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Clean Air Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-edrrm-1.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `EDRRM-24`
      2. Enable the following:
         * From the dropdown for **Radio Band** select the value `2.4 Ghz`
         * Enable the sliders as shown for **Event Driven RRM**
         * From the dropdown for **Sensitivity Threshold** select the value `Low`
      3. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-edrrm-2.png?raw=true "Import JSON")

#### EDRRM Configuration for 5 Ghz

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **Clean Air Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-edrrm-3.png?raw=true "Import JSON")

   3. Then on the page that appears:
      1. Enter a Name for the Design Element, `EDRRM-5`
      2. Enable the following:
         * From the dropdown for **Radio Band** select the value `5 Ghz`
         * Enable the sliders as shown for **Event Driven RRM**
         * From the dropdown for **Sensitivity Threshold** select the value `Low`
      3. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-edrrm-4.png?raw=true "Import JSON")

### Step 5 - **Create Flex Configuration**

For times when we have overlapping IP with wireless or when using VN's or VRF we can account for this with the Flex feature for overlapping IP.

1. On the **Model Config Editor** page click the `Design` tab and complete the following:

   1. Select a model-based config as shown **AAA Radius Attributes Configuration**
   2. Click the **⨁ Add** button to create custom config.

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-flex-1.png?raw=true "Import JSON")

   3. Complete the following:
      1. Enter a Name for the Design Element, `FLEX`
      2. Enable the slider for **IP Overlap**
      3. Click **Save**

      ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-sect-flex-2.png?raw=true "Import JSON")

## Section 2 - **Assigning Model-Based Configuration**

1. Select the hamburger menu icon to open the menu. Select **`Design > Network Profiles`**.

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-menu-profiles.png?raw=true "Import JSON")

2. Select the **edit** button beside the Wireless Network Profile

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-profiles-edit.png?raw=true "Import JSON")

3. Select the **Model Configs** Tab 

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-1.png?raw=true "Import JSON")

### Global Parameters in Model Based-Configs

We now will add Model configs for the various global configurations all at once. Global configuration parameters may be added together like the following:

* AAA Radius Atributes Configuration
* CleanAir Configurations
* Event Driven RRM Configurations
* Flex Configuration

1. Click the **⨁ Add Model Config** button

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-2.png?raw=true "Import JSON")

2. In the Window that appears select the following:
   
   1. Within Event Driven RRM Configuration select:
      * **EDRRM-24**
      * **EDRRM-5**
   2. Within AAA Radius Atributes Configuration select:
      * **AAA**
   3. Within Flex Configuration select:
      * **FLEX**
   4. Within CleanAir Configuration select:
      * **CA-24**
      * **CA-5**
   5. Click **Add**

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-3.png?raw=true "Import JSON")

### Voice Phone Parameters for 8821 IP Phones on the CAMPUS-PSK SSID

We now will add the Voice Model config for 8821 IP Phones attached to the CAMPUS-PSK SSID. 

Remember the following settings are attached to the VOICE Model-Based Config:

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-PSK      | PHONES         | P2P, Voice, Video, DHCP Req'd                |

Complete the following:

1. Click the **⨁ Add Model Config** button

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-4.png?raw=true "Import JSON")

2. In the Window that appears select the following:
   
   1. Within Advanced SSID Configuration select **VOICE**:
   2. Within **Applicability** select **CAMPUS-PSK**:
   3. Click **Add**

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-5.png?raw=true "Import JSON")

### Guest Parameters for Guest Traffic on the GUESTNET SSID

We now will add the Guest Parameters for the GUESTNET SSID. 

Remember the following settings are attached to the GUEST Model-Based Config:

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| GUESTNET        | GUEST TRAFFIC  | No P2P, VMware Fusion, DHCP Req'd            |

Complete the following:

1. Click the **⨁ Add Model Config** button

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-6.png?raw=true "Import JSON")

2. In the Window that appears select the following:
   
   1. Within Advanced SSID Configuration select **GUEST**:
   2. Within **Applicability** select **GUESTNET**:
   3. Click **Add**

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-7.png?raw=true "Import JSON")

### Employee and IOT Parameters for Internal Traffic on the CAMPUS-EAP SSID

We now will add the Employee Parameters for the CAMPUS-EAP SSID. 

Remember the following settings are attached to the EMPLOYEE Model-Based Config:

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-EAP      | DATA & VOICE   | P2P, VMware Fusion, Voice, Video, DHCP Req'd |

Complete the following:

1. Click the **⨁ Add Model Config** button

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-8.png?raw=true "Import JSON")

2. In the Window that appears select the following:
   
   1. Within Advanced SSID Configuration select **EMPLOYEE**:
   2. Within **Applicability** select **CAMPUS-EAP**:
   3. Click **Add**

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-9.png?raw=true "Import JSON")

### To complete the selections SAVE

1. Click Save to add the changes.

   ![json](../../ASSETS/LABS/WIRELESS/module7-modelbasedconfig/dnac-design-ftmbc-deploy-save.png?raw=true "Import JSON")

2. The configuration changes would now need to be provisioned to the Wireless Controller.

</details>

## Summary

Congratulations you have completed the Model-Based Config module of the lab and added configurations to add the following configurations.

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-PSK      | PHONES         | P2P, Voice, Video, DHCP Req'd                |
| CAMPUS-EAP      | DATA & VOICE   | P2P, VMware Fusion, Voice, Video, DHCP Req'd |
| GUESTNET        | GUEST TRAFFIC  | No P2P, VMware Fusion, DHCP Req'd            |

For bonus points go and add another Model-Based config for the final SSID:

| SSID:           | USE CASE:      | Description of Requirements                  | 
|-----------------|----------------|----------------------------------------------|
| CAMPUS-IPSK     | IOT            | P2P, Silent Hosts, DHCP Req'd                |

Additional Model-Based Configuration may also be added in a simlar fashion. Please consult the Cisco Unified Wireless Design Guide for further details. Please use the navigatation below to continue your learning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Continue to Wireless Templates Module**](../LAB-2-Wireless-Automation/module9-wirelesstemplates.md)

> [**Return to Lab Menu**](./README.md)