# 9.0 - Cisco Catalyst Center Provision Deploy Composite

This example deploys the committed composite template to a managed device.

## Script

- `deploy_composite.py` resolves root and version UUIDs, builds the v2 deploy payload, resolves the target device UUID by management IP, and polls the deployment task to completion.
- Shared utilities are imported from `../common/helpers.py` via the `common` package.

## Run

```bash
export CATC_HOST=198.18.129.100
export CATC_USERNAME=admin
export CATC_PASSWORD='<password>'
export CATC_PROJECT='DEBUG-PROJECT'
export CATC_MEMBER='DEBUG-MEMBER.j2'
export CATC_COMPOSITE='DEBUG-COMPOSITE.j2'
export CATC_DEVICE_IP='198.19.1.1'
python3 deploy_composite.py
```

## Outcome

Use this as the final end-to-end template deployment validation step.