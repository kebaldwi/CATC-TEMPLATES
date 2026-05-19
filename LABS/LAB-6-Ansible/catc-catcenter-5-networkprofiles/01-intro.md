# Network Profile

In this module we build a **Switching Network Profile** in Catalyst Center using the **`cisco.dnac.network_profile_switching_workflow_manager`** module. A Switching Network Profile is the binding layer between the templates synced in Module 4 and the sites built in Module 1 — it tells Catalyst Center "*these templates apply to switches in these sites*".

> Reference: [7.0 Network Profile — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/7.0-Cisco-Catalyst-Center-Network-Profile/README.md)

## What a Network Profile Is

A Network Profile groups together:

* One or more **sites** the profile is assigned to.
* One or more **Day-N templates** (the `.j2` and composite templates synced in Module 4).
* Optionally **onboarding/PnP templates** for zero-touch device deployment.

Once a profile is assigned to a site, every device subsequently provisioned to that site (Module 6) inherits the profile's templates as its Day-N configuration source.

In `settings.json`, a profile is described like this:

```json
"network_profile": {
  "name": "EVPN-FABRIC-PROFILE",
  "type": "switching",
  "site_names": ["Global/NA/Pod-1"],
  "day_n_templates": ["BGP-EVPN-BUILD"],
  "onboarding_templates": []
}
```

## What 7.0 Does

`network_profile.yml` is short and direct — almost all the work is delegated to a single Workflow Manager module:

| Step | Mechanism |
|------|-----------|
| Read every project entry that has a `network_profile` block | Jinja2 filter |
| Build a unified `config` payload (one entry per profile) | `set_fact` with `combine` |
| Submit the batch as `state: merged` | `cisco.dnac.network_profile_switching_workflow_manager` |

The Workflow Manager module handles the underlying CatC API set internally — create vs. update, site UUID resolution, template UUID resolution, and binding the profile to its sites. It is fully idempotent: re-running with the same `settings.json` produces no change.

## What You Will Do

1. Encrypt the `vault.yml` for the 7.0 playbook.
2. Run `network_profile.yml`.
3. Verify the new Network Profile in **Design → Network Profiles**, including its site assignment and template binding.

> **Prerequisites:** Modules 1–4 complete. The Day-N templates referenced in `settings.json` (e.g. `BGP-EVPN-BUILD`) must already exist in the Catalyst Center Template Project — that is what Module 4 produced.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)
