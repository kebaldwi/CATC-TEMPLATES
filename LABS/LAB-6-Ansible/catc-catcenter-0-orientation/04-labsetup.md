# Lab Setup — Inventory, Vault, and Running a Playbook

This section explains the **execution pattern** that every later module follows. Once you understand it here, the per-module deploy guides become very short — they are mostly just `cd <directory>` and `ansible-playbook ...`.

## Overview Video

[![Preparing Ansible](https://img.youtube.com/vi/SP1f1ISY76Y/0.jpg)](https://www.youtube.com/watch?v=SP1f1ISY76Y)
> 💡 Tip: Ctrl/Cmd + Click the thumbnail to open the video in a new tab.

## The Repeating Pattern

Each playbook directory under [`Support/Resources/Ansible`](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/README.md) follows the same shape:

```text
N.0-Cisco-Catalyst-Center-<Function>/
├── ansible.cfg              # local config (vault, callback plugins)
├── inventory.yml            # connection + path variables
├── requirements.txt         # Python deps (already satisfied by install-ansible.sh)
├── requirements.yml         # Galaxy collections (already satisfied by install-ansible.sh)
├── vault.yml.example        # template — tells you which credentials are needed
├── <playbook>.yml           # the actual playbook
└── tasks/                   # included task files (when present)
```

To run any playbook you do three things, **once per directory**:

1. Copy `vault.yml.example` → `vault.yml` and fill in credentials.
2. Encrypt `vault.yml` with the master password from `~/.vault_pass`.
3. Run the playbook with `ansible-playbook -i inventory.yml <playbook>.yml --vault-password-file ~/.vault_pass`.

## The Source of Truth — `settings.json`

The intent that drives every playbook in this suite lives in a single file:

```text
~/TECOPS-2599/Projects/BGP_EVPN/Settings/settings.json
```

This is the same file consumed by the Cisco Workflows track. Each playbook reads it (the path is set in each `inventory.yml` as `settings_json_path`) and acts on the relevant block:

| Block in `settings.json` | Consumed by |
|--------------------------|-------------|
| `HierarchyParent / Area / Bldg / Floor / BldgAddress` | 1.0 Hierarchy |
| `network_settings` | 2.0 Settings |
| `device_credentials` / `assign_credentials` | 3.0 Credentials |
| `device_list` | 4.0 Discovery, 5.0 Assign-to-Site, 8.0 Provision |
| `network_profile` | 7.0 Network Profile |
| `DayNTemplateNames` | 9.0 Composite Deploy |

Edit this single file and every downstream playbook will pick up the change on its next run.

## The Vault — Credentials at Rest

`vault.yml.example` in each directory is a YAML file with placeholder values telling you which variables that playbook needs. For example, in `1.0-Cisco-Catalyst-Center-Site-Hierarchy/vault.yml.example`:

```yaml
catc_username: admin
catc_password: C1sco12345
```

The required-variable matrix is:

| Playbook | Required Vault Variables |
|----------|--------------------------|
| 1.0 Hierarchy | `catc_username`, `catc_password` |
| 2.0 Settings | `catc_username`, `catc_password` |
| 3.0 Credentials | `catc_username`, `catc_password` |
| 4.0 Discovery | `dnac_username`, `dnac_password` |
| 5.0 Assign-to-Site | `dnac_username`, `dnac_password` |
| 6.0 Templates GitHub | `dnac_username`, `dnac_password` (+ optional `git_token` for private repos) |
| 7.0 Network Profile | `dnac_username`, `dnac_password` |
| 8.0 Provision Devices | `dnac_username`, `dnac_password` |
| 9.0 Composite Deploy | `dnac_username`, `dnac_password` |

For DCLOUD, both username and password are always `admin` / `C1sco12345`.

### Encrypt-in-Place Workflow

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/1.0-Cisco-Catalyst-Center-Site-Hierarchy

# 1. Create plain-text vault from the template
cp vault.yml.example vault.yml

# 2. Edit vault.yml with your values (already correct for DCLOUD)
nano vault.yml

# 3. Encrypt it in place — uses the master password from ~/.vault_pass
ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass

# Verify
head -1 vault.yml
# Expect: $ANSIBLE_VAULT;1.1;AES256
```

Repeat for every module's directory. The good news: the vault contents are typically identical (same `admin / C1sco12345`) so you can copy `vault.yml` from the previous module and skip the `nano` step.

> [!TIP]
> The encrypted `vault.yml` is `.gitignore`d at the root of the resources tree. The unencrypted `vault.yml.example` is committed for documentation. **Never commit a decrypted `vault.yml`.**

## Running a Playbook — The One-Liner

Once a directory's `vault.yml` is encrypted, running the playbook is always:

```bash
ansible-playbook -i inventory.yml <playbook>.yml --vault-password-file ~/.vault_pass
```

Useful flags:

| Flag | Purpose |
|------|---------|
| `--check` | Dry-run — show what *would* change without calling CatC |
| `-v` / `-vv` / `-vvv` | Increase verbosity (the third `-v` shows raw HTTP traffic) |
| `--tags <tag>` | Run only tasks with the given tag (rarely needed in this lab) |
| `--limit <host>` | Restrict to a subset of inventory hosts |

### Reading a `PLAY RECAP`

Every successful run finishes with a recap line per host. For Catalyst Center playbooks the only "host" is `catalyst_center` and you want:

```text
PLAY RECAP *********************************************************************
catalyst_center            : ok=12   changed=4    unreachable=0    failed=0    skipped=2
```

* **`ok`** — task ran and target is in desired state (no API change required).
* **`changed`** — task ran and changed state in CatC (e.g. created a site, updated a setting).
* **`unreachable`** — Catalyst Center could not be contacted (VPN down? wrong IP?).
* **`failed`** — module returned an error (look immediately above for the failing task and its `msg:`).

Re-running a successful playbook should always produce `changed=0` — that is *idempotency* in action and is the property that makes Ansible safe to run on a schedule.

## What's Next

You are fully set up. From here, every module follows the same drumbeat:

1. `cd` into the module's directory under `Support/Resources/Ansible`.
2. Encrypt that directory's `vault.yml`.
3. Run the playbook.
4. Verify the result in the Catalyst Center UI.

> [**Next Module**](../catc-catcenter-1-hierarchy/01-intro.md)

> [**Return to LAB Menu**](../README.md)
