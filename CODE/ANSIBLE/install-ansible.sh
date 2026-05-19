#!/bin/bash
# =============================================================================
#  TECOPS-2599 — Ansible Environment Setup
#  Installs all prerequisites for playbooks 1.0 – 10.0
#
#  Tested on: Ubuntu 22.04 / 24.04
#  Run as a regular user with sudo privileges
#
#  All Python packages are installed inside an isolated virtual environment
#  at ~/tecops-venv to avoid conflicts with system Python packages.
# =============================================================================
set -e

VENV_DIR="$HOME/tecops-venv"

echo "============================================================"
echo "  TECOPS-2599 — Ansible Environment Setup"
echo "============================================================"

# ── 0. Preflight: restore system python3 for apt compatibility ────────────────
# On Ubuntu 20.04 (focal), apt_pkg and add-apt-repository are compiled for
# python3.8. If a previous script run used update-alternatives to point
# /usr/bin/python3 at python3.9, every subsequent apt command breaks with
# "No module named 'apt_pkg'". Restore it here before touching apt.
# Also remove any stale 'alias python=python3.x' lines that would shadow the
# venv's python binary and the update-alternatives setting.
echo ""
echo "[ 0/9 ] Preflight: ensuring system python3 points to python3.8..."
sed -i "/alias python=/d" ~/.bashrc ~/.bash_aliases 2>/dev/null || true
unalias python 2>/dev/null || true
if [ -f /usr/bin/python3.8 ]; then
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10 2>/dev/null || true
    sudo update-alternatives --set python3 /usr/bin/python3.8 2>/dev/null || true
    echo "  /usr/bin/python3 → $(python3 --version 2>&1) (apt compatibility restored)"
else
    echo "  python3.8 not found — skipping (not Ubuntu 20.04 focal)"
fi

# ── 1. System update ──────────────────────────────────────────────────────────
echo ""
echo "[ 1/9 ] Updating apt package lists..."
# || true prevents set -e from aborting on pre-existing GPG/repo warnings
# (e.g. expired Grafana/Jenkins keys common on shared lab jumpboxes)
sudo apt-get update || true

# ── 2. Python 3.10 ────────────────────────────────────────────────────────────
echo ""
echo "[ 2/9 ] Installing Python 3.10..."
# Ubuntu 20.04 focal is EOL — the deadsnakes PPA no longer provides packages
# for focal. Build Python 3.10 from source instead.
# Python 3.10 satisfies ansible 9.x (ansible-core 2.16) which needs Python >=3.10.
if command -v python3.10 &>/dev/null; then
    echo "  python3.10 already installed: $(python3.10 --version)"
else
    echo "  Building Python 3.10 from source..."
    PYTHON310_VERSION="3.10.16"
    sudo apt-get install -y --no-install-recommends \
        build-essential libssl-dev zlib1g-dev libncurses5-dev \
        libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
        libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev \
        tk-dev curl
    TMP_SRC=$(mktemp -d)
    curl -fsSL "https://www.python.org/ftp/python/${PYTHON310_VERSION}/Python-${PYTHON310_VERSION}.tgz" \
        -o "${TMP_SRC}/Python-${PYTHON310_VERSION}.tgz"
    tar -xf "${TMP_SRC}/Python-${PYTHON310_VERSION}.tgz" -C "${TMP_SRC}"
    pushd "${TMP_SRC}/Python-${PYTHON310_VERSION}" > /dev/null
    ./configure --prefix=/usr/local --enable-optimizations --with-ensurepip=install 2>&1 | tail -3
    make -j"$(nproc)" 2>&1 | tail -3
    sudo make altinstall 2>&1 | tail -3
    popd > /dev/null
    rm -rf "${TMP_SRC}"
fi

# Verify the python3.10 binary is available — do NOT change python3 system default
# (apt_pkg is compiled for python3.8; touching python3 alternative breaks apt).
# Register the unversioned 'python' command → python3.10 so it survives reboots.
python3.10 --version
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.10 10
sudo update-alternatives --set python /usr/local/bin/python3.10
echo "  python → $(python --version)"

# ── 3. Virtual environment ────────────────────────────────────────────────────
echo ""
echo "[ 3/9 ] Creating virtual environment at $VENV_DIR..."
# If an existing venv was built with a different Python (e.g. 3.9 from a
# previous failed run), remove it so python3.10 creates a clean one.
if [ -d "$VENV_DIR" ]; then
    EXISTING_PY=$("$VENV_DIR/bin/python3" --version 2>&1 | awk '{print $2}')
    if [[ "$EXISTING_PY" != 3.10* ]]; then
        echo "  Existing venv uses Python $EXISTING_PY — removing and recreating with Python 3.10..."
        rm -rf "$VENV_DIR"
    else
        echo "  Existing venv already uses Python $EXISTING_PY — reusing."
    fi
fi
# Use python3.10 explicitly — system python3 may still point to 3.8 on focal
python3.10 -m venv "$VENV_DIR"

# Activate the venv for the remainder of this script
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "  Virtual environment active: $(which python3) ($(python3 --version))"

# Upgrade pip inside the venv
python3 -m pip install --upgrade pip

# Persist venv activation for all future shell sessions
ACTIVATE_LINE="source \"$VENV_DIR/bin/activate\""
if ! grep -qF "$ACTIVATE_LINE" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# TECOPS-2599 — activate Ansible virtual environment" >> ~/.bashrc
    echo "$ACTIVATE_LINE" >> ~/.bashrc
    echo "  Added venv activation to ~/.bashrc"
else
    echo "  ~/.bashrc already contains venv activation — skipping"
fi

# ── 4. Ansible ────────────────────────────────────────────────────────────────
echo ""
echo "[ 4/9 ] Installing Ansible into venv..."
# ansible 9.x ships ansible-core 2.16 — required to support the latest
# cisco.catalystcenter collection (>=2.4.0 requires ansible-core >=2.16).
# ansible 9.x requires Python >=3.10 (venv uses Python 3.10 — satisfied).
pip install 'ansible>=9.0.0,<10.0.0'
ansible --version

# ── 5. Python SDK dependencies ────────────────────────────────────────────────
echo ""
echo "[ 5/9 ] Installing Python SDK dependencies into venv..."

# libssh-dev — C library required to build ansible-pylibssh (see below)
# Must be installed before pip attempts to compile the extension module.
sudo apt-get install -y --no-install-recommends libssh-dev

# catalystcentersdk — required by cisco.catalystcenter collection
#   Used by: playbooks 1.0 (Site Hierarchy) and 2.0 (Settings)
pip install 'catalystcentersdk>=2.3.7.9,<3.0.0'

# dnacentersdk — required by cisco.dnac collection
#   Used by: playbooks 3.0 (Credentials) through 9.0 (Provision Composite)
pip install 'dnacentersdk>=2.11.0'

# github-clone — used by playbook 6.0 (Templates GitHub integration)
pip install github-clone

# paramiko — SSH transport library; fallback backend for ansible.netcommon network_cli
#   Used by: backup-lab-configs.yml (playbook 10.0)
pip install 'paramiko>=2.11'

# ansible-pylibssh — preferred SSH backend for ansible.netcommon network_cli
#   Used by: backup-lab-configs.yml (playbook 10.0)
#   Without this, network_cli falls back to paramiko which fails with
#   "transport shut down or saw EOF" on Python 3.10+ when connecting to
#   Cisco IOS-XE/NX-OS devices via interactive PTY shells.
#   Requires libssh-dev (installed above via apt) for the C extension build.
pip install 'ansible-pylibssh>=1.4.0'

# ── 6. Ansible Galaxy collections ─────────────────────────────────────────────
echo ""
echo "[ 6/9 ] Installing Ansible Galaxy collections..."
# Collections are installed to ~/.ansible/collections (user scope) so they
# persist independently of the venv and are available to all playbooks.

# cisco.catalystcenter — new collection namespace
#   Used by: playbooks 1.0 (Site Hierarchy), 2.0 (Settings)
ansible-galaxy collection install 'cisco.catalystcenter:==2.1.3' --force

# cisco.dnac — legacy collection namespace
#   Used by: playbooks 3.0 (Credentials) through 9.0 (Provision Composite)
ansible-galaxy collection install 'cisco.dnac:==6.46.0' --force

# ansible.utils — utility filters/plugins required by both cisco collections
#   Used by: playbooks 1.0, 2.0, 3.0
ansible-galaxy collection install 'ansible.utils:==5.1.2' --force

# community.general — general-purpose modules (git_config, uri extras, etc.)
#   Used by: playbook 6.0 (Templates GitHub integration)
ansible-galaxy collection install 'community.general:==10.7.0' --force

# cisco.ios — SSH-based IOS device management
#   Used by: playbook 10.0 (Backup My Configs)
ansible-galaxy collection install 'cisco.ios:>=4.0.0' --force

# cisco.nxos — SSH-based NX-OS device management
#   Used by: playbook 10.0 (Backup My Configs)
ansible-galaxy collection install 'cisco.nxos:>=5.0.0' --force

# ── 7. Vault password file ────────────────────────────────────────────────────
echo ""
echo "[ 7/9 ] Checking vault password file..."
if [ ! -f "$HOME/.vault_pass" ]; then
    echo "  WARNING: ~/.vault_pass not found."
    echo "  Create it before running any playbook:"
    echo "    echo 'YourVaultPassword' > ~/.vault_pass && chmod 600 ~/.vault_pass"
else
    chmod 600 "$HOME/.vault_pass"
    echo "  ~/.vault_pass exists — permissions set to 600."
fi

# ── 8. Verify ─────────────────────────────────────────────────────────────────
echo ""
echo "[ 8/9 ] Verifying installation..."

echo ""
echo "--- Virtual environment ---"
echo "  Path:   $VIRTUAL_ENV"
echo "  Python: $(python3 --version)"

echo ""
echo "--- Ansible version ---"
ansible --version

echo ""
echo "--- Installed Python packages ---"
pip show catalystcentersdk dnacentersdk ansible paramiko ansible-pylibssh | grep -E '^(Name|Version)'

echo ""
echo "--- Installed Ansible collections ---"
ansible-galaxy collection list | grep -E 'cisco\.|ansible\.utils|community\.general'

echo ""
echo "============================================================"
echo "  Setup complete!"
echo ""
echo "  The virtual environment is at: $VENV_DIR"
echo "  It will activate automatically in new shell sessions via ~/.bashrc."
echo "  To activate it now in your current shell, run:"
echo "    source \"$VENV_DIR/bin/activate\""
echo ""
echo "  Next steps:"
echo "  1. Activate the venv in your current shell (see above)"
echo "  2. Create the vault password file (if not done already):"
echo "     echo 'YourVaultPassword' > ~/.vault_pass && chmod 600 ~/.vault_pass"
echo "  3. Update vault.yml in the root of each playbook directory"
echo "     with your Catalyst Center credentials, then encrypt it:"
echo "     ansible-vault encrypt vault.yml --vault-password-file ~/.vault_pass"
echo "============================================================"
