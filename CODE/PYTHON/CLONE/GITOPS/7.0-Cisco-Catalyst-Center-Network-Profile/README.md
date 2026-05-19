# 7.0 - Cisco Catalyst Center Network Profile

This example builds switching network profile payloads from `settings.json` and can optionally submit them to a user-supplied endpoint.

## Script

- `network_profile.py` extracts `network_profile` blocks, converts Day 0 and Day N template objects into the string lists expected by the workflow, and prints the final payload.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

Preview only:

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
python3 network_profile.py
```

Optional apply mode:

```bash
export CATC_APPLY_NETWORK_PROFILE=true
export CATC_NETWORK_PROFILE_ENDPOINT='/dna/intent/api/v1/network-profile/switching'
python3 network_profile.py
```

## Outcome

Use this after template preparation when you want to validate or apply switching profile bindings per site.