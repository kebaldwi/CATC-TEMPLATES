# 6.2 - Cisco Catalyst Center Templates Create Project

This example creates or reuses a Template Programmer project.

## Script

- `create_project.py` checks whether the project already exists, creates it if needed, and polls the asynchronous task until the project UUID is available.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
export CATC_PROJECT='DEBUG-PROJECT'
python3 create_project.py
```

## Outcome

Use this before creating member or composite templates, since both need a project UUID.