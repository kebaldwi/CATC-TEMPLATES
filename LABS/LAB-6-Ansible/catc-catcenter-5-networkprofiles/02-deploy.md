# Run the Network Profile Playbook

## Overview Video

[![Build Network Profile](https://img.youtube.com/vi/Id4XFi3-OK4/0.jpg)](https://www.youtube.com/watch?v=Id4XFi3-OK4)
> 💡 Tip: Ctrl/Cmd + Click the thumbnail to open the video in a new tab.

> All commands run on the Script Server (`ssh root@198.18.133.28`) with the `~/tecops-venv` activated.

## Step 1 — Encrypt the Vault

```bash
cd ~/TECOPS-2599/Support/Resources/Ansible/7.0-Cisco-Catalyst-Center-Network-Profile
cp vault.yml.example vault.yml
ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass
```

## Step 2 — Run the Playbook

```bash
ansible-playbook -i inventory.yml network_profile.yml \
    --vault-password-file ~/.vault_pass
```

The recap should report `failed=0`. On the first run expect one `changed=true` task per profile defined in `settings.json`; on subsequent runs the same task reports `changed=false`.

## Step 3 — Verify in Catalyst Center

1. Open Catalyst Center → **&#8801; Menu → Design → Network Profiles**.

   ![Network Profiles](../../../ASSETS/LABS/ANSIBLE/networkprofile/networkprofile.png?raw=true)

2. Click into the profile you just created (e.g. `EVPN-FABRIC-PROFILE`). On the **Sites** tab, confirm the assigned site path matches the `site_names` from `settings.json`. On the **Templates** tab, confirm the bound Day-N template (e.g. `BGP-EVPN-BUILD`).

   ![Network Profile Detail](../../../ASSETS/LABS/ANSIBLE/networkprofile/networkprofile-detail.png?raw=true)

## Summary

The Network Profile is now bound to the lab sites and references the BGP EVPN composite template. Provisioning a device to one of those sites in the next module will use this profile to determine which Day-N template to push.

> [**Next Module**](../catc-catcenter-6-provisioning/01-intro.md)

> [**Return to LAB Menu**](../README.md)
