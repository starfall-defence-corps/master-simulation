#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$ROOT_DIR/.docker"
SSH_DIR="$DOCKER_DIR/ssh-keys"

echo ""
echo "=============================================="
echo "  STARFALL DEFENCE CORPS ACADEMY"
echo "  Master Simulation: Operation Iron Curtain"
echo "  Initialising Iron Curtain fleet..."
echo "=============================================="
echo ""

# Check python3-venv is available
if ! python3 -m venv --help &>/dev/null; then
    echo "  ERROR: python3-venv is not installed."
    echo "  On Debian/Ubuntu: sudo apt install python3-venv"
    echo "  On Fedora/RHEL:   sudo dnf install python3-virtualenv"
    exit 1
fi

# Set up Python virtual environment if not present
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "  Setting up Python environment..."
    python3 -m venv "$ROOT_DIR/venv"
    "$ROOT_DIR/venv/bin/pip" install -q -r "$ROOT_DIR/requirements.txt"
    "$ROOT_DIR/venv/bin/ansible-galaxy" collection install community.general ansible.posix > /dev/null
    echo "  Python environment ready."
    echo ""
fi

# Generate SSH key pair if not already present
if [ ! -f "$SSH_DIR/cadet_key" ]; then
    echo "  Generating SSH credentials..."
    mkdir -p "$SSH_DIR"
    ssh-keygen -t ed25519 -f "$SSH_DIR/cadet_key" -N "" -C "cadet@starfall-academy" -q
    cp "$SSH_DIR/cadet_key.pub" "$SSH_DIR/authorized_keys"
    chmod 600 "$SSH_DIR/cadet_key"
    chmod 644 "$SSH_DIR/authorized_keys"
    echo "  SSH credentials generated."
    echo ""
fi

# Copy private key to workspace for Ansible to use
mkdir -p "$ROOT_DIR/workspace/.ssh"
cp "$SSH_DIR/cadet_key" "$ROOT_DIR/workspace/.ssh/cadet_key"
chmod 600 "$ROOT_DIR/workspace/.ssh/cadet_key"

# Build and start containers
echo "  Building Iron Curtain fleet nodes..."
docker compose -f "$DOCKER_DIR/docker-compose.yml" up -d --build 2>&1 | while read -r line; do
    echo "    $line"
done

echo ""
echo "  Waiting for SSH to become available..."
for node in sdc-iron-web-1:2281 sdc-iron-web-2:2282 sdc-iron-db-1:2283 sdc-iron-db-2:2284 sdc-iron-app:2285 sdc-iron-comms:2286; do
    name="${node%%:*}"
    port="${node##*:}"
    for i in $(seq 1 30); do
        if ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=1 \
            -i "$SSH_DIR/cadet_key" cadet@localhost -p "$port" exit 2>/dev/null; then
            echo "    $name (port $port): ONLINE"
            break
        fi
        if [ "$i" -eq 30 ]; then
            echo "    $name (port $port): TIMEOUT — check 'docker compose logs $name'"
        fi
        sleep 1
    done
done

echo ""
echo "=============================================="
echo "  Iron Curtain Fleet: 6 nodes ONLINE"
echo ""
echo "  Dread Admiral Snowflake built this fleet by hand."
echo "  Every server different. Nothing documented."
echo "  Nothing tested. Nothing automated."
echo ""
echo "  Your mission: uniform, tested, automated"
echo "  compliance across all six nodes."
echo ""
echo "  You have 3.5 hours."
echo ""
echo "  Your workspace: workspace/"
echo "  Mission brief:  docs/BRIEFING.md"
echo "  Verify work:    make test"
echo "=============================================="
echo ""

# #50 — stamp mission start for the ARIA performance tier (make test reads it)
date +%s > "$ROOT_DIR/.aria_start" 2>/dev/null || true

# #56 — start the exercise scoring poller (kill any prior instance, fresh log).
# It TCP-probes each node's published SSH port so ARIA can score service
# availability across the whole run. Killed by make reset/destroy.
if [ -f "$ROOT_DIR/.aria_score.pid" ]; then
    kill "$(cat "$ROOT_DIR/.aria_score.pid")" 2>/dev/null || true
fi
: > "$ROOT_DIR/.aria_score.jsonl"
ARIA_SCORE_LOG="$ROOT_DIR/.aria_score.jsonl" \
ARIA_SCORE_TARGETS="sdc-iron-web-1=2281 sdc-iron-web-2=2282 sdc-iron-db-1=2283 sdc-iron-db-2=2284 sdc-iron-app=2285 sdc-iron-comms=2286" \
    nohup bash "$SCRIPT_DIR/score-poller.sh" >/dev/null 2>&1 &
echo $! > "$ROOT_DIR/.aria_score.pid"
