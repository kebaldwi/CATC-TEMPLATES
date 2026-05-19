# Orientation — Install Ansible and Bootstrap the Vault

In this section we clone the lab repository onto the Script Server, run the bundled `install-ansible.sh` bootstrap script, and create the Ansible Vault password file that every playbook in the lab will use to decrypt its credentials.

> [!IMPORTANT]
> All commands run inside the SSH session you opened in [the previous section](./02-preparation.md): `ssh root@198.18.133.28`.

## Step 1 — Clone the Repository

```bash
cd ~
git clone https://github.com/kebaldwi/TECOPS-2599.git
cd TECOPS-2599/Support/Resources/Ansible
ls
```

You should see ten numbered playbook directories (`1.0-...` through `10.0-...`), an `install-ansible.sh` script, and a top-level `README.md`. The `README.md` here is the [as-built reference](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/README.md) we link to from every module — bookmark it.

## Step 2 — Run the Bootstrap Script

`install-ansible.sh` automates the full installation of Python 3.9, the venv, Ansible, and every Cisco collection in a single step.

```bash
chmod +x install-ansible.sh
./install-ansible.sh
```

The script performs the following actions:

| Step | Action |
|------|--------|
| 1 | `apt update` |
| 2 | Installs Python 3.9 from the `deadsnakes` PPA |
| 3 | Creates an isolated venv at `~/tecops-venv` and adds activation to `~/.bashrc` |
| 4 | Installs `ansible >= 8.0` (ansible-core 2.15) into the venv |
| 5 | Installs Python SDKs: `catalystcentersdk`, `dnacentersdk`, `github-clone` |
| 6 | Installs Ansible Galaxy collections: `cisco.catalystcenter`, `cisco.dnac`, `ansible.utils`, `community.general`, `cisco.ios`, `cisco.nxos` |
| 7 | Verifies `~/.vault_pass` permissions if it already exists |
| 8 | Prints a verification summary |

Expect the run to take a few minutes (mostly downloading packages and SDK wheels). When it finishes you will see a green-tick verification block listing every component installed.

## Step 3 — Activate the venv

After the script completes, activate the venv in your **current** shell:

```bash
source ~/tecops-venv/bin/activate
```

Your prompt now starts with `(tecops-venv)`. Future SSH sessions will activate the venv automatically because the script appended the activation line to `~/.bashrc`.

Verify the toolchain:

```bash
ansible --version
# Expect: ansible [core 2.15.x], python version 3.9.x

ansible-galaxy collection list cisco.catalystcenter
# Expect: cisco.catalystcenter 2.1.3

ansible-galaxy collection list cisco.dnac
# Expect: cisco.dnac 6.46.x or newer
```

## Step 4 — Create the Vault Password File

All playbooks use **Ansible Vault** to protect Catalyst Center and device credentials at rest. Every `vault.yml` in every playbook directory is encrypted with the same master password — that password lives in `~/.vault_pass`.

Pick a password (anything will do for the lab; this is local to the Script Server). Then:

```bash
echo 'YourVaultPassword' > ~/.vault_pass
chmod 600 ~/.vault_pass
ls -l ~/.vault_pass
# Expect: -rw------- 1 root root ...
```

> [!IMPORTANT]
> The `chmod 600` is **mandatory**. Ansible will refuse to use the file if its permissions are world-readable (`ssh-agent` style protection). If you forget this, every playbook will exit immediately with a `vault password file is world-readable` error.

## Step 5 — Verify a Playbook Loads

Quick smoke test — without running it, ask Ansible to syntax-check the first playbook in the suite:

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/1.0-Cisco-Catalyst-Center-Site-Hierarchy
ansible-playbook --syntax-check site_hierarchy.yml -i inventory.yml
# Expect: playbook: site_hierarchy.yml
```

If syntax check passes, the venv, collections, and inventory paths are all wired up correctly. We're ready to set up per-playbook credentials in the next section.

## Recap

What you have now on the Script Server:

* `~/TECOPS-2599/` — the lab repository checked out fresh from GitHub
* `~/tecops-venv/` — isolated Python 3.9 venv with Ansible 8 and all Cisco collections
* `~/.vault_pass` — `0600`-protected master vault password
* `~/.bashrc` — auto-activates the venv on every new SSH session

> [**Next Section**](./04-labsetup.md)

> [**Return to LAB Menu**](../README.md)
