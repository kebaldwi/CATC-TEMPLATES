# 6.4 - Cisco Catalyst Center Templates Create Composite Template

This example creates a composite template that wraps one or more member templates.

## Script

- `create_composite_template.py` locates the member template, creates a composite container with `containingTemplates`, commits it, and resolves the latest version UUID.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
export CATC_PROJECT='DEBUG-PROJECT'
export CATC_MEMBER='DEBUG-MEMBER.j2'
export CATC_COMPOSITE='DEBUG-COMPOSITE.j2'
python3 create_composite_template.py
```

## Outcome

Use this before deployment so both the composite root UUID and latest version UUID are available.