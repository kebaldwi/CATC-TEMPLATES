# 6.3 - Cisco Catalyst Center Templates Create Member Template

This example creates a simple member template and commits it so Catalyst Center generates a version UUID.

## Script

- `create_member_template.py` creates a leaf Jinja template, commits it, then resolves the latest version entry from `versionsInfo`.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
export CATC_PROJECT='DEBUG-PROJECT'
export CATC_MEMBER='DEBUG-MEMBER.j2'
python3 create_member_template.py
```

## Outcome

Use this before step 6.4 because the composite template references the member template by root UUID.