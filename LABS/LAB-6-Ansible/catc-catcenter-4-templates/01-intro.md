# Templates from GitHub

In this module we use Ansible to implement a **GitOps** workflow for Catalyst Center templates: a single playbook (`ansible-git-catc.yml`) reads a folder of Jinja2 templates from a GitHub repository, builds composite (multi-template) bundles from `.yml` definition files, and syncs everything into a Catalyst Center Template Project.

> Reference: [6.0 Template GitHub Sync — full as-built](https://github.com/kebaldwi/TECOPS-2599/tree/main/Support/Resources/Ansible/6.0-Cisco-Catalyst-Center-Templates-Github-integration/README.md)

## What "GitOps for Templates" Means

The traditional way of populating Catalyst Center templates is to paste each `.j2` body into the Template Editor in the UI. That works for one or two templates; it does not work for the BGP EVPN template library used in this lab, which has dozens of cross-referenced files.

Instead, the playbook treats GitHub as the source of truth:

1. List every file in the target repo subfolder.
2. Pull the raw content of every `.j2` and `.yml`.
3. Annotate each template with its latest commit metadata (author, message, timestamp).
4. Order templates topologically — composite definition files (`.yml`) tell the playbook which children must exist before their parent composite.
5. Push each template into the configured Catalyst Center Template Project using `cisco.dnac.template_workflow_manager` with `state: merged` (idempotent — creates or updates as needed).

The same playbook can sync any GitHub folder of `.j2` files. Pointing it at a different `repo` / `branch` / `path` re-runs the full sync against that source.

## Composite Templates — One Bundle, Many Members

A *composite template* is a single deployable unit that wraps an ordered list of member templates. In this repository, composite definitions live alongside the `.j2` files as small YAML manifests:

```yaml
# BGP-EVPN-BUILD.yml
name: BGP-EVPN-BUILD
description: Day-N BGP EVPN composite
project_name: TECOPS-2599
member_templates:
  - DEFN-VRF
  - DEFN-OVERLAY
  - DEFN-LOOPBACKS
  - FABRIC-VRF
  - FABRIC-OVERLAY
  - FABRIC-LOOPBACKS
  - FABRIC-EVPN
  - FABRIC-NVE
```

The playbook reads this file, resolves each `member_templates` entry against the templates synced earlier in the run, builds the `containingTemplates` payload, and submits the composite. Member ordering is preserved — at deploy time (Module 6) Catalyst Center pushes the members in the order listed.

## API & Module Surface

| Phase | HTTP | Endpoint / Module | Purpose |
|-------|------|-------------------|---------|
| Repository check | GET | `https://api.github.com/repos/{owner}/{repo}` | Validate access |
| Branch check | GET | `https://api.github.com/repos/{owner}/{repo}/branches/{branch}` | Confirm branch exists |
| Tree listing | GET | `https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1` | Find every `.j2` and `.yml` |
| Raw content | GET | `https://raw.githubusercontent.com/...` | Pull template bodies |
| Commit metadata | GET | `https://api.github.com/repos/.../commits?...` | Author / timestamp / diff |
| Template create / update | module-managed | `cisco.dnac.template_workflow_manager` | Sync to CatC Template Project |

GitHub-side calls go through `ansible.builtin.uri`; Catalyst Center writes go through the Workflow Manager module.

## Source — `inventory.yml`

The playbook is configured entirely from `inventory.yml`:

```yaml
github_owner: kebaldwi
github_repo:  TECOPS-2599
github_branch: main
github_path:   Projects/BGP_EVPN/DayNTemplates
template_project_name: TECOPS-2599
```

To sync a different template library, edit those five values and re-run.

## What You Will Do

1. Encrypt the `vault.yml` for the 6.0 playbook (same `admin / C1sco12345`; optionally add `git_token` for higher GitHub rate limits).
2. Run `ansible-git-catc.yml`. Watch for the per-template *create / update* lines.
3. Verify in **Tools → Template Editor** that the Template Project exists and contains both individual templates and at least one composite.

> **Prerequisites:** Modules 1–3 complete. The Catalyst Center Template Project named in `inventory.yml` will be auto-created if it does not already exist.

> [**Next Section**](./02-deploy.md)

> [**Return to LAB Menu**](../README.md)
