# 4.0 - Cisco Catalyst Center Device Discovery

This example submits discovery jobs using the `device_list` values stored in `settings.json`.

## Script

- `device_discovery.py` creates one discovery request per hierarchy path and submits the device IPs as a multi-range discovery target.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 device_discovery.py
```

Optional:

```bash
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
```

## Outcome

Use this after credentials are in place so Catalyst Center can discover and manage the devices referenced in the lab data.