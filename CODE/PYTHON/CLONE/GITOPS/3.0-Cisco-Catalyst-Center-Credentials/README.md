# 3.0 - Cisco Catalyst Center Credentials

This example creates missing global credentials from `settings.json`.

## Script

- `credentials.py` processes CLI, SNMPv2 read, SNMPv2 write, and NETCONF credentials and skips entries that already exist by description.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 credentials.py
```

Optional:

```bash
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
```

## Outcome

Use this before device discovery so Catalyst Center has the credentials needed to log into the target devices.