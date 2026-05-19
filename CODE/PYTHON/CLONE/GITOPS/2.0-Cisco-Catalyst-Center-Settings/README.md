# 2.0 - Cisco Catalyst Center Settings

This example applies per-site network settings from `settings.json` using the site hierarchy path to resolve each site UUID.

## Script

- `network_settings.py` builds the composite payload for DHCP, DNS, NTP, MOTD, syslog, SNMP, NetFlow, and AAA settings, then sends only non-null values.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 network_settings.py
```

Optional:

```bash
export CATC_SETTINGS_JSON='/absolute/path/to/settings.json'
```

## Outcome

Use this after step 1.0 so the target site paths already exist in Catalyst Center.