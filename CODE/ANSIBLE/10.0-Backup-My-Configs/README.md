# 10.0-Backup-My-Configs

## Overview
This workflow backs up `show running-config` from the lab network devices and stores the output on the Ansible controller.

What it does:

| Capability | Details |
|---|---|
| Multi-platform backup | Supports IOS-XE and NX-OS groups in the same workflow |
| Timestamped archive | Each run writes to `config-backups/<YYYYMMDD-HHMMSS>/` |
| Auto-retention pruning | Keeps only the most recent `backup_retention_count` runs |
| Secure credential handling | Uses `vault.yml` with Ansible Vault |
| Controller-local storage | Writes files with `delegate_to: localhost` |

## API Endpoints and Modules Summary

### Modules Summary

| Collection | Module | Purpose in this playbook | Module Docs |
|---|---|---|---|
| cisco.ios | ios_command | Collect running configuration from IOS-XE devices | cisco.ios >= 4.0.0: [ios_command](https://galaxy.ansible.com/ui/repo/published/cisco/ios/content/module/ios_command/) |
| cisco.nxos | nxos_command | Collect running configuration from NX-OS devices | cisco.nxos >= 5.0.0: [nxos_command](https://galaxy.ansible.com/ui/repo/published/cisco/nxos/content/module/nxos_command/) |
| ansible.builtin | copy | Write collected configs to timestamped files on localhost | ansible-core: [copy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html) |
| ansible.builtin | find, file | Retention and directory lifecycle on backup storage | ansible-core: [find](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/find_module.html), [file](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html) |

### Endpoint/Transport Summary by Phase

| Phase | Transport | Endpoint/Command | Why it is used | API Docs |
|---|---|---|---|---|
| IOS-XE collection | network_cli over SSH | show running-config | Retrieve current device configuration text | N/A (CLI workflow, no Catalyst Center API endpoint) |
| NX-OS collection | network_cli over SSH | show running-config | Retrieve current device configuration text | N/A (CLI workflow, no Catalyst Center API endpoint) |
| Local archive write | localhost filesystem | config-backups/<timestamp>/<hostname>.cfg | Persist per-device backup artifacts | N/A (local filesystem operation) |

### Notes

- This workflow does not call Catalyst Center REST APIs.
- Device interaction is CLI-based using network collections over SSH.

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9+ (tested on 3.13) |
| Ansible Core | 2.14+ |
| `cisco.ios` collection | `>=4.0.0` |
| `cisco.nxos` collection | `>=5.0.0` |
| `paramiko` pip package | `>=2.11` |
| `ansible-pylibssh` pip package | `>=1.4.0` |

Install required collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

Install required Python packages:

> **macOS (Apple Silicon / Homebrew) — Important:** `ansible-pylibssh` must be compiled against the Homebrew `libssh` library. A plain `pip install ansible-pylibssh` will fail with `libssh/libssh.h file not found` because the compiler cannot find the Homebrew headers at their non-standard path. Always install it with the flags below:

```bash
brew install libssh
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install ansible-pylibssh
```

On Linux or if `libssh` headers are on the default system path:

```bash
pip install -r requirements.txt
```

## Directory Structure

```text
10.0-Backup-My-Configs/
├── ansible.cfg
├── backup-lab-configs.yml      # main playbook
├── inventory.yml
├── requirements.yml            # Ansible Galaxy collections
├── requirements.txt            # Python pip packages
├── vault.yml
├── vault.yml.example
├── .vault_pass
└── config-backups/
```

## Installation

1. Open the project folder.
2. Install collections.
3. Create and encrypt `vault.yml`.
4. Run the playbook.

```bash
cd Support/Resources/Ansible/10.0-Backup-My-Configs
ansible-galaxy collection install -r requirements.yml
cp vault.yml.example vault.yml
ansible-vault encrypt vault.yml --vault-password-file .vault_pass
```

## Configuration

Inventory defaults live in `inventory.yml`.

| Variable | Default | Description |
|---|---|---|
| `ansible_connection` | `network_cli` | CLI transport for network devices |
| `ansible_user` | `{{ vault_device_username }}` | Device login username from vault |
| `ansible_password` | `{{ vault_device_password }}` | Device login password from vault |
| `ansible_become` | `yes` | Enable privilege escalation |
| `ansible_become_method` | `enable` | Network enable method |
| `ansible_become_password` | `{{ vault_device_enable_password }}` | Enable password from vault |
| `backup_root_dir` | `config-backups` | Parent directory for backup artifacts |
| `backup_retention_count` | `3` | Number of newest timestamped backup folders to keep |

## Input Data Structure

`vault.yml` keys used by this workflow:

```yaml
vault_device_username: "netadmin"
vault_device_password: "<device-password>"
vault_device_enable_password: "<enable-password>"
```

## How It Works

1. Loads encrypted credentials from `vault.yml`.
2. Builds a run timestamp using controller time.
3. Creates `config-backups/<timestamp>/` on localhost.
4. Runs `show running-config` on IOS-XE and NX-OS hosts.
5. Writes one output file per host:
   `config-backups/<timestamp>/<inventory_hostname>.cfg`
6. Prunes old backup folders and keeps only the latest `backup_retention_count`.

Notes:

> File writes use `ansible.builtin.copy` delegated to localhost.

> Command collection tasks set `changed_when: false` for cleaner idempotent output.

## Running the Playbook

Back up all hosts:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass
```

Back up only IOS-XE hosts:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass --limit iosxe
```

Back up only NX-OS hosts:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass --limit nxos
```

Back up a single host:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass --limit Spine01
```

Syntax check:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass --syntax-check
```

## Debug Mode

Increase verbosity:

```bash
ansible-playbook backup-lab-configs.yml --vault-password-file .vault_pass -vvv
```

## Expected Output

```text
PLAY [Backup running-config from IOS-XE devices] *******************************
TASK [Collect running configuration from IOS-XE] *******************************
ok: [Spine01]
...
TASK [Save IOS-XE config to local backup file] *********************************
changed: [Spine01 -> localhost]

PLAY [Backup running-config from NX-OS devices] ********************************
...
PLAY RECAP *********************************************************************
Spine01 : ok=3 changed=1 failed=0
Core-02 : ok=3 changed=1 failed=0
```

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `Decryption failed` | Wrong vault password | Verify `.vault_pass` value and re-run |
| `Collection not found` | Missing Galaxy collections | Install with `ansible-galaxy collection install -r requirements.yml` |
| `transport shut down or saw EOF` | `ansible-pylibssh` not installed — `network_cli` fell back to paramiko, which cannot open interactive PTY shells to Cisco devices on Python 3.13 | Install `ansible-pylibssh` with Homebrew headers: `brew install libssh && CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install ansible-pylibssh` |
| `libssh/libssh.h file not found` during `pip install ansible-pylibssh` | Compiler cannot find Homebrew libssh headers at the non-standard `/opt/homebrew` path | Pass the include/lib paths explicitly: `CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install ansible-pylibssh` |
| Timeout to device | Management IP unreachable | Test connectivity to `ansible_host` and credentials |
| Empty or missing `.cfg` file | Command failed on device | Re-run with `-vvv`, validate SSH and privilege mode |
| Permission error writing backup | Local filesystem permissions | Ensure write access to `backup_root_dir` |
