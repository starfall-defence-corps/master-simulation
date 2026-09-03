# Starfall Defence Corps Academy

> 🧭 [← 2.6 Counterattack](https://github.com/starfall-defence-corps/mission-2-6-counterattack) · **You are here: Master Simulation** · 🎓 Module 2 complete — next: [MOS 4 · Eyes Everywhere →](https://github.com/starfall-defence-corps/mission-3-4-eyes-everywhere) · [🏠 Academy Hub](https://github.com/starfall-defence-corps/sdc-academy)

> ☁️ **No Docker on your machine?** Create your own copy first (Use this template), then on **your** repo: **Code → Codespaces → Create codespace** — everything is preinstalled. First boot takes ~5 min (one-time); after that it starts fast.

## Master Simulation: Operation Iron Curtain

> *"Dread Admiral Snowflake. 6 servers, every one different. Hand-built. Undocumented. Your mission: uniform, tested, automated compliance."*

You are a Lieutenant at the Starfall Defence Corps Academy. You've completed all of Module 2. Now prove you can combine every skill — assessment, remediation, testing, automation, and incident response — in a single 3.5-hour timed simulation.

## Prerequisites

- Completed Module 2 (Missions 2.1–2.4)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
git clone https://github.com/YOUR-USERNAME/master-simulation.git
cd master-simulation
make doctor
make setup
source venv/bin/activate
```

Read your orders: [Mission Briefing](docs/BRIEFING.md)

Stuck? [Hints](docs/HINTS.md) | Track progress: [Checklist](CHECKLIST.md)

## Lab Architecture

```
 Iron Curtain Fleet (6 nodes)
+---------------------+  +---------------------+
| sdc-iron-web-1 :2281|  | sdc-iron-db-1  :2283|
| sdc-iron-web-2 :2282|  | sdc-iron-db-2  :2284|
| Ubuntu 22.04        |  | Rocky Linux 9       |
+---------------------+  +---------------------+
+---------------------+  +---------------------+
| sdc-iron-app   :2285|  | sdc-iron-comms :2286|
| Ubuntu 22.04        |  | Ubuntu 22.04        |
+---------------------+  +---------------------+
```

## Mission Structure

| Mission | Description | Time |
|---------|-------------|------|
| 1 — Assessment | Inventory, Lynis baseline, document findings | 40 min |
| 2 — Remediation | CIS role, rolling deploy, Molecule tests, Vault | 75 min |
| 3 — Automation | CI pipeline, ansible-lint, Makefile, drift detection | 60 min |
| 4 — Incident | Detect, identify, remediate, document | 35 min |

**Total**: 3.5 hours | **Rank Earned**: Lieutenant Commander | **Badge**: Iron Curtain — Master Operator

## Available Commands

```
make help       Show available commands
make doctor     Check your machine is mission-ready (Docker, ports, tools)
make setup      Launch 6-node Iron Curtain fleet
make test       Run ARIA assessment verification
make incident   Trigger the surprise incident (Mission 4)
make submit     Submit your work for ARIA review (branch, commit, push, PR)
make reset      Destroy and rebuild all nodes
make destroy    Complete teardown
make ssh-web-1  SSH into sdc-iron-web-1 (Ubuntu)
make ssh-web-2  SSH into sdc-iron-web-2 (Ubuntu)
make ssh-db-1   SSH into sdc-iron-db-1 (Rocky Linux)
make ssh-db-2   SSH into sdc-iron-db-2 (Rocky Linux)
make ssh-app    SSH into sdc-iron-app (Ubuntu)
make ssh-comms  SSH into sdc-iron-comms (Ubuntu)
```

## ARIA Review (Pull Request Workflow)

**Locally** — run `make test` for instant verification.

**On Pull Request** — push your work, open a PR, ARIA reviews automatically.

To enable PR reviews, add `ANTHROPIC_API_KEY` to your repo's Secrets.
