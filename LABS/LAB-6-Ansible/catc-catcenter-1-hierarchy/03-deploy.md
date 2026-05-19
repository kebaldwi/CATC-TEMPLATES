# Run the Site Hierarchy Playbook

## Overview Video

[![Build Site Hierarchy](https://img.youtube.com/vi/e7lGFKs2i1w/0.jpg)](https://www.youtube.com/watch?v=e7lGFKs2i1w)
> 💡 Tip: Ctrl/Cmd + Click the thumbnail to open the video in a new tab.

In this section we encrypt the playbook's vault, run `site_hierarchy.yml`, and verify the resulting hierarchy in the Catalyst Center UI.

> All commands run on the **Script Server** (`ssh root@198.18.133.28`) inside the activated `~/tecops-venv` from the orientation module.

## Step 1 — Inspect the Playbook

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/1.0-Cisco-Catalyst-Center-Site-Hierarchy
ls
```

```text
ansible.cfg          requirements.txt        tasks/
DIAGRAMS/            requirements.yml        vault.yml.example
inventory.yml        site_hierarchy.yml
README.md
```

The `tasks/` subfolder contains the two include files used by the main playbook:

* `tasks/create_or_update_site.yml` — runs once per path to create or update an Area/Building/Floor.
* `tasks/delete_site.yml` — runs once per path (in deepest-first order) when `state: deleted`.

Open `inventory.yml` to confirm the data path:

```bash
grep settings_json_path inventory.yml
# Expect: settings_json_path: "../../../Projects/BGP_EVPN/Settings/settings.json"
```

This relative path resolves to `~/TECOPS-2599/Projects/BGP_EVPN/Settings/settings.json` — the shared source-of-truth file.

## Step 2 — Encrypt the Vault

```bash
cp vault.yml.example vault.yml
cat vault.yml
# catc_username: admin
# catc_password: C1sco12345
```

For DCLOUD the values in `vault.yml.example` are already correct, so just encrypt:

```bash
ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass
head -1 vault.yml
# Expect: $ANSIBLE_VAULT;1.1;AES256
```

## Step 3 — Dry Run (Optional)

Confirm the playbook can read its inputs and authenticate to Catalyst Center without making any changes:

```bash
ansible-playbook -i inventory.yml site_hierarchy.yml \
    --vault-password-file ~/.vault_pass \
    --check -v
```

If `--check` produces a `PLAY RECAP` with `failed=0`, the connection, vault, and JSON parsing are all wired up correctly.

## Step 4 — Apply the Hierarchy

```bash
ansible-playbook -i inventory.yml site_hierarchy.yml \
    --vault-password-file ~/.vault_pass
```

A successful run looks like:

```text
PLAY [Build Catalyst Center Site Hierarchy] *********************************

TASK [Read settings.json] ***************************************************
ok: [catalyst_center]

TASK [Build sorted hierarchy path list] *************************************
ok: [catalyst_center]

TASK [Fetch existing site map] **********************************************
ok: [catalyst_center]

TASK [include_tasks : create_or_update_site.yml] ****************************
included: tasks/create_or_update_site.yml for catalyst_center => (item=Global/NA)
included: tasks/create_or_update_site.yml for catalyst_center => (item=Global/NA/HQ San Jose)
included: tasks/create_or_update_site.yml for catalyst_center => (item=Global/NA/HQ San Jose/Floor 1)
...

PLAY RECAP ******************************************************************
catalyst_center  : ok=27   changed=8    unreachable=0    failed=0    skipped=3
```

> [!TIP]
> Re-run the same command immediately. The second run should report `changed=0` — that is idempotency.

## Step 5 — Verify the Hierarchy in Catalyst Center

1. In Chrome, navigate to [**Catalyst Center**](https://198.18.129.100). If an SSL warning is displayed, click **Proceed to `https://198.18.129.100` (unsafe)**.

   ![SSL Error](../../../ASSETS/LABS/COMMON/platform/catc-SSLERROR.png?raw=true)

2. Log in:
   * **username:** `admin`
   * **password:** `C1sco12345`

   ![Login](../../../ASSETS/LABS/COMMON/platform/catc-Login.png?raw=true)

3. Click the **&#8801;** icon to open the menu.

   ![Hamburger](../../../ASSETS/LABS/COMMON/platform/catc-Menu.png?raw=true)

4. Select **Design → Network Hierarchy**.

   ![Menu](../../../ASSETS/LABS/COMMON/platform/catc-Menu-Hierarchy.png?raw=true)

5. Expand the hierarchy on the left and confirm that the Area / Building / Floor entries from `settings.json` are present.

   ![Verify](../../../ASSETS/LABS/ANSIBLE/hierarchy/catc-Hierarchy-Student-Verify.png?raw=true)

## Summary

You have used a single declarative file (`settings.json`) and one Ansible playbook to build the foundational Catalyst Center site hierarchy. No clicking through Design pages, no UI screenshots to follow, and the same playbook can be re-run any time `settings.json` changes — only the deltas will be applied.

> [**Next Module**](../catc-catcenter-2-settings/01-intro.md)

> [**Return to LAB Menu**](../README.md)
