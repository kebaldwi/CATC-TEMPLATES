# 6.1 - Cisco Catalyst Center Templates Authenticate

This example shows the first REST call required by every later template workflow step.

## Script

- `authenticate.py` exchanges HTTP Basic credentials for the short-lived Catalyst Center JWT used as `X-Auth-Token`.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 authenticate.py
```

## Outcome

Use this as the simplest connectivity and credential validation step before moving into project or template operations.