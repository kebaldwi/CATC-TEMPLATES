# Run the Settings and Credentials Playbooks

## Overview Video

[![Assign Settings and Credentials](https://img.youtube.com/vi/aJj658dfiws/0.jpg)](https://www.youtube.com/watch?v=aJj658dfiws)
> 💡 Tip: Ctrl/Cmd + Click the thumbnail to open the video in a new tab.

This section runs both playbooks (2.0 then 3.0) and walks through the verification screens.

> All commands run on the Script Server (`ssh root@198.18.133.28`) with the `~/tecops-venv` activated.

## Part A — Network Settings (2.0)

### Step 1 — Encrypt the Vault

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/2.0-Cisco-Catalyst-Center-Settings
cp vault.yml.example vault.yml
ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass
```

### Step 2 — Run the Playbook

```bash
ansible-playbook -i inventory.yml network_settings.yml \
    --vault-password-file ~/.vault_pass
```

Expect tasks for *Authenticate*, *Resolve site UUIDs*, *Build settings payload*, *PUT settings per site*, and *Poll execution status*. The recap should report `failed=0`.

### Step 3 — Verify in Catalyst Center

1. Open Catalyst Center → click the **&#8801;** menu → **Design → Network Settings**.

   ![Settings Menu](../../../ASSETS/LABS/ANSIBLE/settings/catc-Menu-Settings.png?raw=true)

2. Confirm DNS/NTP/Syslog/SNMP entries match `settings.json`.

   ![Settings Verify 1](../../../ASSETS/LABS/ANSIBLE/settings/catc-Settings-Verify1a.png?raw=true)

   ![Settings Verify 1b](../../../ASSETS/LABS/ANSIBLE/settings/catc-Settings-Verify1b.png?raw=true)

3. Switch to **Telemetry** and confirm the SNMP / Syslog server bindings.

   ![Settings Verify 2](../../../ASSETS/LABS/ANSIBLE/settings/catc-Settings-Verify2.png?raw=true)

4. Switch to **Device Controllability / AAA** and confirm the AAA server entry.

   ![Settings Verify 3a](../../../ASSETS/LABS/ANSIBLE/settings/catc-Settings-Verify3a.png?raw=true)

   ![Settings Verify 3b](../../../ASSETS/LABS/ANSIBLE/settings/catc-Settings-Verify3b.png?raw=true)

## Part B — Device Credentials (3.0)

### Step 4 — Encrypt the Vault

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/3.0-Cisco-Catalyst-Center-Credentials
cp vault.yml.example vault.yml
ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass
```

### Step 5 — Run the Playbook

```bash
ansible-playbook -i inventory.yml credentials.yml \
    --vault-password-file ~/.vault_pass
```

This run takes longer than 2.0 because it walks three credential types and assigns them to every site touched by `assign_credentials`. The Workflow Manager module batches its calls, so most tasks report `changed=true` once and `changed=false` on every subsequent run.

### Step 6 — Verify in Catalyst Center

In **Design → Network Settings → Device Credentials** you should see:

* CLI Credentials — one or more rows matching the `name` values in `device_credentials`.
* SNMPv2c Read and Write rows.
* NETCONF row with the configured port (830 by default).

Each site in the hierarchy should now show the assigned credentials in its detail panel.

## Summary

You have completed the **design** phase of Catalyst Center. Sites have settings and credentials. Catalyst Center now has everything it needs to log in to a real device — which is exactly what we do in the next module.

> [**Next Module**](../catc-catcenter-3-discovery/01-intro.md)

> [**Return to LAB Menu**](../README.md)
