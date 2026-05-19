# Preparation — DCLOUD and the Script Server

## Module Overview

In this section we make sure you can reach the **Script Server** — the Ubuntu host (`198.18.133.28`) where every Ansible playbook in this lab will be executed. The Script Server already has Python and Git available; the next module ([Orientation](./03-orientation.md)) installs Ansible and the Cisco collections on top of it.

## Step 1 — Schedule the DCLOUD Demo

The lab uses the [**Catalyst Center + ISE Lab for Automation & Orchestration**](https://dcloud2.cisco.com/demo/catalyst-center-ise-lab-for-automation-orchestration) demonstration. You must be a Cisco employee or Cisco partner to schedule this; if you are neither, contact your local Cisco account team.

Once scheduled, DCLOUD will issue session details including:

* AnyConnect VPN endpoint, group, username, and password
* RDP details for the Windows 10 jump host (optional — you can also work directly from your laptop)
* IP addressing for every component (Catalyst Center, ISE, Script Server, CML pods)

## Step 2 — Connect to DCLOUD via VPN

1. Launch **Cisco AnyConnect Secure Mobility Client**.
2. Enter the VPN server address from your DCLOUD session.
3. Authenticate using the group, username, and password from the session details.

   ![DCLOUD VPN CONNECTION](../../../ASSETS/LABS/COMMON/VPN-to-DCLOUD.png?raw=true)

4. Verify connectivity from a terminal on your laptop:

   ```bash
   ping 198.18.129.100   # Catalyst Center
   ping 198.18.133.28    # Script Server
   ```

> [!TIP]
> If pings fail, confirm AnyConnect is reporting *Connected* and that your local firewall is not blocking ICMP. The lab IP range is `198.18.0.0/16` — all traffic to that range must transit the AnyConnect tunnel.

## Step 3 — SSH to the Script Server

Open a terminal and SSH into the Script Server. **All subsequent commands in the orientation and module deployment guides run inside this SSH session.**

```bash
ssh root@198.18.133.28
# Password: C1sco12345
```

You should land in `/root` with a standard Ubuntu shell.

```bash
$ uname -a
Linux script-server 5.15.0-... x86_64 GNU/Linux
$ python3 --version
Python 3.10.12
$ git --version
git version 2.34.1
```

> [!IMPORTANT]
> Everything from this point onward is performed on the Script Server (`198.18.133.28`), not on your laptop. Your laptop is only the means of opening that SSH session and a browser to Catalyst Center for verification.

## Step 4 — Verify Catalyst Center is Reachable

From the Script Server SSH session, confirm the Catalyst Center API endpoint responds:

```bash
curl -k -s -o /dev/null -w '%{http_code}\n' https://198.18.129.100/dna/system/api/v1/auth/token
# Expect: 401  (auth required, but the endpoint is reachable)
```

A `401` is expected and correct — it means TLS negotiated successfully and the API responded; it just refused the unauthenticated request. Anything else (timeout, connection refused) indicates a routing or VPN problem.

## Step 5 — Open Catalyst Center in a Browser

While not used by Ansible itself, the Catalyst Center UI is how we **verify** what each playbook produced. Open Chrome and navigate to:

* URL: `https://198.18.129.100`
* Username: `admin`
* Password: `C1sco12345`

You should see the SSL warning (DCLOUD uses self-signed certificates). Click **Proceed to `https://198.18.129.100` (unsafe)** to continue.

![SSL Error](../../../ASSETS/LABS/COMMON/platform/catc-SSLERROR.png?raw=true)

After login you will see the Catalyst Center dashboard. Leave this browser tab open — every later module ends with a verification step in the UI.

![Login](../../../ASSETS/LABS/COMMON/platform/catc-Login.png?raw=true)

## Overview Video

[![Prepping Lab](https://img.youtube.com/vi/2vaBbtkBpYc/0.jpg)](https://www.youtube.com/watch?v=2vaBbtkBpYc)
> 💡 Tip: Ctrl/Cmd + Click the thumbnail to open the video in a new tab.

> [**Next Section**](./03-orientation.md)

> [**Return to LAB Menu**](../README.md)
