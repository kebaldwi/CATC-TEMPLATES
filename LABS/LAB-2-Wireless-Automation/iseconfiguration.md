# Identity Services Engine (ISE) Configuration - In Development

Within this section, we will configure ISE to work with various sections of the Wireless Lab. This section is not a definitive guide into how to configure ISE, and should not negate the use of the configuration guide.

This section is merely here to help new users of ISE to build test environments and help them with general understandings of Intent Based Network System concepts like 802.1x with iPSK, and EAP.

## Logical Topology

To review the lab envionment that is available is depicted here:

![json](../../ASSETS/LABS/WIRELESS/DCLOUD_Topology_Wireless-v1.png?raw=true "Import JSON")

ISE is stood up beside the Windows AD server. The two are configured but not integrated. Beyond basic IP connectivity the ISE server is in a default state.

Windows AD, while it had workstations added, and general users and groups, does not have the Active Directory Certificate Services (ADCS) role turned on nor is it handing out certificates.

## Authentication Methods

To test with ISE a general understanding of the differences between authentication methods is required among **OPEN, PSK, and EAP** methods.

### OPEN and PSK Authentication

While all **SSID** may be built without ISE both the **OPEN and PSK** policies can built via **Catalyst Center** and tested *without* configuration being created on ISE directly. 

Thus for **OPEN and PSK** you may return to the lab modules and continue configuration as no further additional configuration steps are required.

### iPSK Authentication

**Identity PSK (iPSK)** is an authentication methodology whereby Pre-Shared Keys may be configured to be used in addition to Profiling in order to apply policy from ISE. This can be utilized to allow for differing Pre-Shared Keys, and also for differing device types on the same SSID. 

Additionally, Secure Group Tags (SGT) and Change of Authorization methods may also be incorporated into the overall policy.

**Identity PSK (iPSK)** can be tested in this environment *with* ISE. ADCS is not a requirement. 

For **iPSK** you may follow the section below to configure ISE to work with the Wireless LAN located [here](./iseconfiguration.md#ise-ipsk-configuration-section).

### EAP Authentication

EAP stands for Extensible Authentication Protocol. EAP methods are different ways to authenticate users and devices in a network. There are many different EAP methods, such as EAP-TLS, EAP-PEAP, and EAP-TTLS. Each method has its own strengths and weaknesses, and some are more commonly used than others depending on the specific network environment and security requirements.

Here is a list of some common EAP methods:

- **EAP-TLS**
- **EAP-PEAP**
- **EAP-TTLS**
- EAP-SIM
- EAP-AKA
- EAP-GTC
- EAP-MD5
- **EAP-FAST**
- EAP-IKEv2
- **EAP-MSCHAPv2**

There are many other EAP methods as well, but these are some of the most commonly used ones. The EAP methods in bold above are typical ones found used in most wireless networks.

If EAP is to be tested, it is recommended to complete the following tasks:

1. Build ADCS server if Certificate based authentication is used
   - To build ADCS follow the steps in this [section](./Certificates.md#pki-infrastructure-build)
2. Join ISE to Active Directory
3. Build AD and ISE Policies for the use case

For **EAP** you may follow the section below to configure ISE and AD to work with the Wireless LAN located [here](./iseconfiguration.md#ise-eap-configuration-section).

## ISE iPSK Configuration Section

profiling
profiling build logical profile
authz profiles and policy
endpoint logical authz profile and policy
endpoint ipsk authz profile and policy

## ISE EAP Configuration Section

Prerequisites for EAP

ISE Certificate Prep
ISE Join to direct
ISE CAP profile

profiling, authz profiles and policy w/wo SGT

## Summary

Congratulations you have completed the XXX module of the lab and . Please use the navigatation below to continue your learning.

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into. 

> [**Return to Lab Menu**](./README.md)