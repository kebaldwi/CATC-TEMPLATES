# 5.0 - Cisco Catalyst Center Assign To Site

This example assigns discovered devices to their target site path using the hierarchy data in `settings.json`.

## Script

- `assign_to_site.py` groups device IPs by site path, resolves the site UUID, and submits the assignment payload for each site.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 assign_to_site.py
```

Optional:

```bash
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
```

## Outcome

Use this after discovery so devices appear under the correct site hierarchy in Catalyst Center.