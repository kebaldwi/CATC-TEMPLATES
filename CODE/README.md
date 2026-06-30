# CODE [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kebaldwi/DNAC-TEMPLATES)

This folder includes code for all the labs as well as new and legacy configurations.

## **Folder Structure**

The following is an explanation of the folder structure:

This **CODE** repository is built out to share Cisco Catalyst Center Automations and Templates and allow for ongoing submissions from those inclined to share their work with the community. Initially the repository includes all the examples that we have used in this repository in RAW TEXT and JSON format.

The **CODE** is also offered in **[Latest Release Candidates](https://github.com/kebaldwi/DNAC-TEMPLATES/releases/latest)** automatically

> [!IMPORTANT]
> The locations for examples have been consolidated here. If you have a template your proud of and you want your name in lights please submit them and we will include them in the repository giving you an honourable mention.</br></br>
> If you wish to contribute to the templates please **[submit here](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/categories/feedback-and-ideas)**

### **Top-Level Folder Map**

| Folder | Purpose |
|--------|---------|
| [ANSIBLE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/)       | End-to-end Cisco Catalyst Center Ansible automation suite (10 ordered playbooks + bootstrap installer) |
| [BRUNO](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/BRUNO/)           | Bruno API client collections for Catalyst Center labs |
| [DATA](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DATA/)             | Source-of-truth data files (CSV, JSON, YAML) consumed by automations |
| [DOCS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DOCS/)             | Cisco reference PDFs and lab data sheets |
| [JENKINS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/JENKINS/)       | Jenkinsfiles for CI/CD pipelines driving Catalyst Center automations |
| [POSTMAN](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/)       | Postman collections and environments for the labs |
| [POWERSHELL](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POWERSHELL/) | PowerShell helpers for Windows-side services (CA, DHCP, DNS, GPO) |
| [PYTHON](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/PYTHON/)         | Python automation scripts and redistributable bundles |
| [SCRIPTS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/SCRIPTS/)       | Charting and Mermaid diagram generation helpers |
| [SHELL](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/SHELL/)           | Shell-based environment preparation scripts |
| [TEMPLATES](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/)   | Jinja2 and Velocity template library (raw `.j2` / `.vm` plus CatC import JSON) |
| [TRAFFIC](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TRAFFIC/)       | Traffic log sample data |
| [WORKFLOWS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/WORKFLOWS/)   | Catalyst Center Workflow Automation (CCWA) bundles — original CATC library and the v3 GitOps suite |

---

### [ANSIBLE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/)

End-to-end Ansible automation suite for Cisco Catalyst Center. Ten sequentially-ordered provisioning playbooks plus a standalone backup utility, bootstrapped by `install-ansible.sh`.

| Item | Description |
|------|-------------|
| [install-ansible.sh](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/ANSIBLE/install-ansible.sh) | One-shot Ubuntu installer (Python 3.9 venv + Ansible 8) |
| [1.0-Cisco-Catalyst-Center-Site-Hierarchy](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/1.0-Cisco-Catalyst-Center-Site-Hierarchy/)             | Create Areas / Buildings / Floors |
| [2.0-Cisco-Catalyst-Center-Settings](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/2.0-Cisco-Catalyst-Center-Settings/)                         | Apply site network settings |
| [3.0-Cisco-Catalyst-Center-Credentials](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/3.0-Cisco-Catalyst-Center-Credentials/)                   | Create and assign CLI / SNMP credentials |
| [4.0-Cisco-Catalyst-Center-Device-Discovery](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/4.0-Cisco-Catalyst-Center-Device-Discovery/)         | Run discovery jobs |
| [5.0-Cisco-Catalyst-Center-Assign-To-Site](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/5.0-Cisco-Catalyst-Center-Assign-To-Site/)             | Assign discovered devices to sites |
| [6.0-Cisco-Catalyst-Center-Templates-Github-integration](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/6.0-Cisco-Catalyst-Center-Templates-Github-integration/) | Sync templates from GitHub into CatC |
| [7.0-Cisco-Catalyst-Center-Network-Profile](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/7.0-Cisco-Catalyst-Center-Network-Profile/)           | Bind network profiles to sites |
| [8.0-Cisco-Catalyst-Center-Provision-Devices](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/8.0-Cisco-Catalyst-Center-Provision-Devices/)       | Provision devices |
| [9.0-Cisco-Catalyst-Center-Provision-Composite](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/9.0-Cisco-Catalyst-Center-Provision-Composite/)   | Provision with composite templates |
| [10.0-Backup-My-Configs](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/10.0-Backup-My-Configs/)                                                 | Standalone backup utility |
| [DIAGRAMS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/ANSIBLE/DIAGRAMS/)                                                                             | Mermaid / PNG suite diagrams |

See: [ANSIBLE/README.md](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/ANSIBLE/README.md) for full as-built documentation.

---

### [BRUNO](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/BRUNO/)

[Bruno](https://www.usebruno.com/) API client collections.

| Item | Description |
|------|-------------|
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/BRUNO/ARCHIVE/)             | Historical Bruno collections retained for reference |
| [DEVNET-IGNITE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/BRUNO/DEVNET-IGNITE/) | DevNet Ignite collection (placeholder — populated per event) |

---

### [DATA](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DATA/)

Source-of-truth data consumed by Ansible, Python and Workflow automations.

| Item | Description |
|------|-------------|
| [CSV](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DATA/CSV/)             | `CCC-Design-Settings-v3.csv`, `DNAC-Design-Settings.csv` and per-pod variants under `PODS/` (POD0 – POD9) |
| [JSON](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DATA/JSON/)           | JSON data examples (placeholder) |
| [YAML](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DATA/YAML/)           | `project_details.yml`, `site_operations.yml` |

---

### [DOCS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DOCS/)

Cisco reference PDFs and lab data sheets.

| Item | Description |
|------|-------------|
| `DNACenter_security_best_practices_guide.pdf` | Catalyst Center security best practices |
| `High_Availability_DG.pdf`                    | High Availability design guide |
| `cisco-dna-center-sd-access-wl-dg.pdf`        | SD-Access wireless deployment guide |
| `cisco_dna_center_ug_2_3_5.pdf`               | Catalyst Center user guide 2.3.5 |
| `configuring_autoconf.pdf`                    | Autoconf configuration reference |
| `provision-wireless-devices.pdf`              | Wireless device provisioning reference |
| `Lab9-Authentication-Rules.csv`               | ISE authentication rules used by Lab 9 |
| `Lab9-Authorization-Rules.csv`                | ISE authorization rules used by Lab 9 |
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/DOCS/ARCHIVE/) | Archived reference material |

---

### [JENKINS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/JENKINS/)

Jenkinsfiles driving the CI/CD pipelines used in the labs.

| Item | Description |
|------|-------------|
| [jenkinsfile_discovery](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/JENKINS/jenkinsfile_discovery)                 | Device discovery pipeline |
| [jenkinsfile_hierarchy](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/JENKINS/jenkinsfile_hierarchy)                 | Site hierarchy build pipeline |
| [jenkinsfile_inventory](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/JENKINS/jenkinsfile_inventory)                 | Device inventory export pipeline |
| [jenkinsfile_poe_sustainability](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/JENKINS/jenkinsfile_poe_sustainability) | PoE sustainability reporting pipeline |
| [jenkinsfile_templates](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/JENKINS/jenkinsfile_templates)                 | Template sync pipeline |

---

### [POSTMAN](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/)

Postman collections and environments for the labs.

| Item | Description |
|------|-------------|
| `lab-1-wired-auto-postman-collection.json` / `-environment.json` / `-files.zip`       | Lab 1 — Wired Automation |
| `lab-2-wireless-auto-postman-collection.json` / `-environment.json` / `-files.zip`    | Lab 2 — Wireless Automation |
| `lab-3-advanced-auto-postman-collection.json` / `-environment.json`                   | Lab 3 — Advanced Automation |
| `lab-9-ise-automation-collection.json` / `-environment.json`                          | Lab 9 — ISE Automation |
| [POSTMAN_VERSION_11](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/POSTMAN_VERSION_11/) | Lab 1 & Lab 2 collections re-exported for Postman v11 |
| [DEVNET-IGNITE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/DEVNET-IGNITE/)           | Catalyst Center Use-Case API Collection + per-pod design CSVs |
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POSTMAN/ARCHIVE/)                       | Historical Postman collections |

---

### [POWERSHELL](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POWERSHELL/)

PowerShell helpers for the Windows-side services used in the labs.

| Item | Description |
|------|-------------|
| [powershell.ps1](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell.ps1)         | General-purpose lab helper |
| [powershell-CA.ps1](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-CA.ps1)   | Certificate Authority configuration |
| [powershell-DHCP.ps1](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-DHCP.ps1) | DHCP service configuration |
| [powershell-DNS.ps1](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-DNS.ps1)   | DNS service configuration |
| [powershell-GPO.ps1](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/POWERSHELL/powershell-GPO.ps1)   | Group Policy configuration |
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/POWERSHELL/ARCHIVE/)                       | Previous-generation scripts |

---

### [PYTHON](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/PYTHON/)

Python automation scripts, importable API helpers, and redistributable zip bundles.

| Item | Description |
|------|-------------|
| `clean-up.py`                       | Tear-down helper for lab state |
| `deploy_hierarchy.py`               | Build the site hierarchy |
| `deploy_settings.py`                | Push site / network settings |
| `deploy_templates.py`               | Push templates into a CatC project |
| `device_discovery.py`               | Launch and monitor discovery jobs |
| `device_inventory.py`               | Export device inventory |
| `extract_templates_from_project.py` | Extract templates from a CatC project export |
| `poe_sustainability.py`             | PoE sustainability reporting |
| `template_sync.py`                  | Template repository ↔ CatC sync |
| `dnac_apis.py` / `dnac_api_kb.py`   | Reusable Catalyst Center API wrappers |
| `Bundle.zip`, `CATCLicenseSync.zip`, `CATCTelemetrySync.zip`, `DNACenterRecon.zip` | Redistributable script bundles |
| [CLONE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/PYTHON/CLONE/) | Cloneable lab skeletons: `CICD-LAB/`, `GITOPS/`, `PYTHON-LAB/` |
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/PYTHON/ARCHIVE/) | Historical scripts |

---

### [SCRIPTS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/SCRIPTS/)

Charting and Mermaid diagram-generation helpers used by the documentation tooling.

| Item | Description |
|------|-------------|
| [chart_gen.py](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SCRIPTS/chart_gen.py)         | Chart generator (v1) |
| [chart_gen_v2.py](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SCRIPTS/chart_gen_v2.py)   | Chart generator (v2) |
| [mermaid.j2](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SCRIPTS/mermaid.j2)             | Jinja2 template for Mermaid diagram rendering (v1) |
| [mermaid_v2.j2](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SCRIPTS/mermaid_v2.j2)       | Jinja2 template for Mermaid diagram rendering (v2) |
| [traffic_logging.py](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SCRIPTS/traffic_logging.py) | Traffic log generation helper |

---

### [SHELL](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/SHELL/)

Shell-based environment-preparation scripts.

| Item | Description |
|------|-------------|
| [prepserver.sh](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/SHELL/prepserver.sh) | Bootstrap a fresh lab server |
| [ARCHIVE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/SHELL/ARCHIVE/)             | Previous shell helpers |

---

### [TEMPLATES](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/)

The template library. Templates are provided both as raw scripting-language files (`.j2`, `.vm`) for editing and as JSON bundles ready for direct import into Cisco Catalyst Center.

| Item | Description |
|------|-------------|
| [JINJA2](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/)       | Jinja2 templates — `DAYN/`, `ONBOARDING/`, `WIRELESS/`, `UTILITIES/` (each with `J2/` raw text and `JSON/` import bundles) |
| [VELOCITY](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/VELOCITY/)   | Velocity templates — `DAYN/JSON/` and `ONBOARDING/{JSON,VM}/` |
| [DAYN](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/DAYN/)           | Legacy grouping — see `JINJA2/DAYN/` and `VELOCITY/DAYN/` |
| [ONBOARDING](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/ONBOARDING/) | Legacy grouping — see `JINJA2/ONBOARDING/` and `VELOCITY/ONBOARDING/` |

#### Jinja2 Quick Links

  * [DayN Jinja2 Examples (JSON)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/DAYN/JSON/) — JSON files for easy import to Cisco Catalyst Center for Day N
  * [DayN Jinja2 Raw Text (J2)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/DAYN/J2/) — Day N templates in raw text for editing
  * [Onboarding Jinja2 Examples (JSON)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/ONBOARDING/JSON/) — JSON files for easy import to Cisco Catalyst Center for Day Zero
  * [Onboarding Jinja2 Raw Text (J2)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/ONBOARDING/J2/) — Day Zero templates in raw text for editing
  * [Wireless Jinja2 Examples (JSON)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/WIRELESS/JSON/) — JSON files for easy import to Cisco Catalyst Center for Wireless
  * [Wireless Jinja2 Raw Text (J2)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/WIRELESS/J2/) — Wireless templates in raw text for editing
  * [Jinja2 Utilities](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/JINJA2/UTILITIES/) — Utility templates (placeholder)

#### Velocity Quick Links

  * [DayN Velocity Examples (JSON)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/VELOCITY/DAYN/JSON/) — JSON files for easy import to Cisco Catalyst Center for Day N
  * [Onboarding Velocity Examples (JSON)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/VELOCITY/ONBOARDING/JSON/) — JSON files for easy import to Cisco Catalyst Center for Day Zero
  * [Onboarding Velocity Raw Text (VM)](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TEMPLATES/VELOCITY/ONBOARDING/VM/) — Day Zero `.vm` templates in raw text for editing

---

### [TRAFFIC](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/TRAFFIC/)

Captured traffic log sample data.

| Item | Description |
|------|-------------|
| [traffic_log.csv](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TRAFFIC/traffic_log.csv) | Sample traffic log CSV |

See: [TRAFFIC/README.md](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/TRAFFIC/README.md).

---

### [WORKFLOWS](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/WORKFLOWS/)

Catalyst Center Workflow Automation (CCWA) bundles. Two libraries:

| Item | Description |
|------|-------------|
| [CATC](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/WORKFLOWS/CATC/)         | Original `CATC-*` building-block workflows (hierarchy, settings, discovery, templates, port-config, command runner, inventory, get-hierarchy, brown-field onboarding v2/v3) and the v1 `GitOps-*` build chain. See: [WORKFLOWS/CATC/README.md](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/WORKFLOWS/CATC/README.md) |
| [EXCHANGE](https://github.com/kebaldwi/DNAC-TEMPLATES/tree/master/CODE/WORKFLOWS/EXCHANGE/) | Recommended v3 suite — 12 ordered workflows (Site Hierarchy → Settings & Credentials → Discovery & Assign → Templates GitHub → Templates Composite → Network Profile → Provision Composite → Command Runner → Site Based Upgrade → Paginated Device Inventory → Paginated Site Hierarchy → Bulk Command Runner). See: [WORKFLOWS/EXCHANGE/README.md](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/CODE/WORKFLOWS/EXCHANGE/README.md) |

---

> [!IMPORTANT]
> **Feedback:** If you found this set of **labs** or **content** helpful, please fill in comments on this feedback form [give feedback](https://github.com/kebaldwi/DNAC-TEMPLATES/discussions/new?category=feedback-and-ideas).</br></br>
**Content Problems and Issues:** If you found an **issue** on the **lab** or **content** please fill in an [issue](https://github.com/kebaldwi/DNAC-TEMPLATES/issues/new) include what file, along with the issue you ran into.

> [**Return to Main Menu**](./README.md)
