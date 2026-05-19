# 1.0 - Cisco Catalyst Center Site Hierarchy

This example builds missing area, building, and floor objects in Catalyst Center from `settings.json`.

## Script

- `site_hierarchy.py` reads hierarchy fields from the input data, expands intermediate parent paths, and creates sites in parent-before-child order.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 site_hierarchy.py
```

Optional:

```bash
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
```

## Outcome

Use this step before applying settings, discovery, or site assignment so the target hierarchy already exists.