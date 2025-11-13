# ISE Certificate Setup

## Overview

Cisco Identity Services Engine (ISE) uses certificates to provide secure communication and authentication within the network. Certificates identify ISE nodes to endpoints and secure communications between nodes, external servers, and end-user portals such as guest, sponsor, and BYOD portals. ISE manages system certificates for node identification and trusted certificates for establishing trust with users and devices. It supports certificate issuance, key management, and storage through its internal Certificate Authority (CA) service, which can issue and sign certificates for endpoints, enabling secure personal device authentication. Certificates are also used for TLS-based EAP authentication, RADIUS DTLS server authentication, and SAML verification, ensuring secure access control and communication across the network infrastructure.  ISE’s certificate management includes generating Certificate Signing Requests (CSRs), importing CA-signed certificates, and configuring certificate usage for different purposes such as admin communication, portal access, and pxGrid communication -- which is what we will accomplish in this lab.

## General Information

The process for getting ISE setup with certificates is similar to that of Catalyst Center - or any PKI certificate process for that matter.

1. A Root Certificate Authority certificate is installed as a "Trusted Root" on the end host (in this case, ISE)

2. A Certificate Signing Request (CSR) is generated from the end host

3. That CSR is then signed by the root CA to generate a signed certificate

4. The signed certificate is installed on the end host

    
With ISE, we can do this via either the GUI or the API.  For the purposes of this lab, you only need to complete one option - but feel free to attempt both for your own knowledge.

Go to:

[**ISE Certificate Setup via GUI**](./03a-ISE-GUI.md)

[**ISE Certificate Setup via API**](./03b-ISE-API.md)

[**Return to ISE Automation Lab Overview**](../README.md)

