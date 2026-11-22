# Starfall Defence Corps Academy

> 🧭 [← 2.6 Counterattack](https://github.com/starfall-defence-corps/mission-2-6-counterattack) · **You are here: Master Simulation** · 🎓 Module 2 complete — next: [MOS 4 · Eyes Everywhere →](https://github.com/starfall-defence-corps/mission-3-4-eyes-everywhere) · [MOS 5 · Battle Rattle →](https://github.com/starfall-defence-corps/mission-3-5-battle-rattle) · [🏠 Academy Hub](https://github.com/starfall-defence-corps/sdc-academy) · [📚 Field Manuals](https://github.com/starfall-defence-corps/sdc-academy/tree/main/field-manuals)

> ☁️ **No Docker on your machine?** Create your own copy first (Use this template), then on **your** repo: **Code → Codespaces → Create codespace** — everything is preinstalled. First boot takes ~5 min (one-time); after that it starts fast.

## Master Simulation — Operation: Iron Curtain

> *"Dread Admiral Snowflake. 6 servers, every one different. Hand-built. Undocumented. Your mission: uniform, tested, automated compliance."*

You are a Lieutenant at the Starfall Defence Corps Academy. You've completed all of Module 2. Now prove you can combine every skill — assessment, remediation, testing, automation, and incident response — in a single 3.5-hour timed simulation.

This is the Module 2 capstone and an **assessment, not a walkthrough**: you get orders and a verdict, nothing in between. Pass it to earn the rank of **Lieutenant Commander** and the **Iron Curtain — Master Operator** badge.

## Briefing

**Dread Admiral Snowflake** built this fleet by hand: six servers, every one different, nothing documented, tested or automated. He has been relieved of command and you inherit his infrastructure. The Voidborn have been probing it for weeks, and with no compliance baseline and no drift detection, nobody can tell what has already been changed.

Every node ships with his misconfigurations — SSH, file permissions, kernel parameters, access control, initial setup, unwanted services and a plaintext credentials file — catalogued as the known threat profile in the [Mission Briefing](docs/BRIEFING.md). Your job is to replace all of it with uniform, tested, automated CIS compliance. Then, once your automation is in place, the fleet comes under attack.

## Objectives

The simulation runs as four missions. `make test` verifies each one:

| Mission | Time | ARIA checks |
|---------|------|-------------|
| 1 — Assessment | 40 min | `workspace/inventory/hosts.yml` lists all 6 nodes with `debian` and `redhat` groups; at least two `group_vars` files exist; `ansible all -m ping` reaches all 6 nodes; `ASSESSMENT.md` records Lynis baseline scores |
| 2 — Remediation | 75 min | An `iron_curtain` role with at least 8 tasks in `tasks/main.yml` (at least 5 tagged), handlers, variables in `defaults/` (or `vars/`) and at least one `.j2` template; `site.yml` uses `serial` and applies the role; `vault.yml` is Vault-encrypted and `.vault-pass` exists; SSH root login is disabled on every node and `/etc/shadow` is `0640` on the Ubuntu nodes; `molecule/default/molecule.yml` exists; your Testinfra tests in `workspace/tests/` have at least 8 test functions |
| 3 — Automation | 60 min | `.github/workflows/ci.yml` (under `workspace/`) has lint and test stages linked with `needs` and a `matrix`; `.github/workflows/drift-detection.yml` has a `schedule`/`cron` trigger and raises an issue on failure; a `Makefile` with `lint`, `test` and `scan` targets; `.ansible-lint`; a completed `PIPELINE.md` |
| 4 — Incident | 35 min | Triggered by `make incident`. `INCIDENT.md` is filled in and names the compromised node, and that node has been remediated: its effective SSH config is hardened again and the intruder's persistence is gone |

All paths are relative to `workspace/`. The full deliverables for each mission, including the role layout and the Vault password to use, are in the [Mission Briefing](docs/BRIEFING.md).

> **Do not run `make incident` until Missions 1–3 are complete.** It compromises the fleet; the Mission 4 remediation checks apply once it has fired.

## What This Assesses

Everything from Modules 1 and 2, under one clock:

- Inventory, `group_vars` and facts across a mixed Ubuntu / Rocky Linux fleet (Module 1)
- Roles, Jinja2 templates, handlers, conditionals and Ansible Vault (Module 1)
- CIS Level 1 controls as tagged tasks, with Lynis as evidence ([2.2](https://github.com/starfall-defence-corps/mission-2-2-compliance-as-code))
- Molecule configuration and Testinfra tests ([2.1](https://github.com/starfall-defence-corps/mission-2-1-weapon-handling-test))
- Rolling deployment with `serial`, and an idempotent role (second run: `changed=0`) ([2.3](https://github.com/starfall-defence-corps/mission-2-3-fleet-sync))
- CI workflow, drift detection, `ansible-lint` and pipeline documentation ([2.4](https://github.com/starfall-defence-corps/mission-2-4-defence-in-depth))
- Incident response: detect, identify, remediate and document a compromise ([2.5](https://github.com/starfall-defence-corps/mission-2-5-noise-storm), [2.6](https://github.com/starfall-defence-corps/mission-2-6-counterattack))
- Keeping the fleet reachable while you rebuild it

## Prerequisites

- Completed Module 2 (Missions 2.1–2.6)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- **Ansible**: provided by the lab — `make setup` builds a local venv with `ansible-core`, Molecule and pytest-testinfra; no host install needed
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
# 1. Use this template on GitHub (green button, top right) to create YOUR OWN
#    copy. Set it Public, then clone it:
git clone https://github.com/YOUR-USERNAME/master-simulation.git
cd master-simulation

# 2. Check your machine is mission-ready
make doctor

# 3. Launch the 6-node Iron Curtain fleet — this starts the clock
make setup

# 4. Activate the virtual environment
source venv/bin/activate
```

5. **Read your orders**: [Mission Briefing](docs/BRIEFING.md)
6. **Stuck?** [Hints & Troubleshooting](docs/HINTS.md)
7. **Track progress**: [Checklist](CHECKLIST.md)
8. **After Missions 1–3**: `make incident`
9. **Ready?** `make test`, then `make submit`

All work happens in `workspace/`. Run `make` targets from the **project root**.

## Lab Architecture

```
 Your Machine
+--------------------------------------------------------------+
|  workspace/                                                  |
|    ansible.cfg            (provided)                         |
|    site.yml               (commented skeleton — you complete) |
|    files/sysctl-hardened.conf  (provided)                    |
|    inventory/             (you write hosts.yml + group_vars) |
|    roles/iron_curtain/    (you build)                        |
|    molecule/default/      (you write molecule.yml)           |
|    tests/                 (you write Testinfra tests)        |
|    ASSESSMENT.md · PIPELINE.md · INCIDENT.md  (templates)    |
|                                                              |
|  Iron Curtain fleet — Docker Network: 172.36.0.0/24          |
|  +----------------------+  +----------------------+          |
|  | sdc-iron-web-1 :2281 |  | sdc-iron-db-1  :2283 |          |
|  | sdc-iron-web-2 :2282 |  | sdc-iron-db-2  :2284 |          |
|  | Ubuntu 22.04         |  | Rocky Linux 9        |          |
|  +----------------------+  +----------------------+          |
|  +----------------------+  +----------------------+          |
|  | sdc-iron-app   :2285 |  | sdc-iron-comms :2286 |          |
|  | Ubuntu 22.04         |  | Ubuntu 22.04         |          |
|  +----------------------+  +----------------------+          |
+--------------------------------------------------------------+
```

| Node | OS | SSH port | IP | Role |
|------|----|----------|----|------|
| `sdc-iron-web-1` | Ubuntu 22.04 | 2281 | 172.36.0.11 | Web server |
| `sdc-iron-web-2` | Ubuntu 22.04 | 2282 | 172.36.0.12 | Web server |
| `sdc-iron-db-1` | Rocky Linux 9 | 2283 | 172.36.0.13 | Database |
| `sdc-iron-db-2` | Rocky Linux 9 | 2284 | 172.36.0.14 | Database |
| `sdc-iron-app` | Ubuntu 22.04 | 2285 | 172.36.0.15 | Application |
| `sdc-iron-comms` | Ubuntu 22.04 | 2286 | 172.36.0.16 | Communications |

All nodes accept SSH as `cadet` with the key `make setup` generates (`workspace/.ssh/cadet_key`). Lynis is pre-installed on the Ubuntu nodes only; the Rocky Linux nodes are marked N/A in the `ASSESSMENT.md` template.

## Timing and Scoring

Start your timer at the beginning of Mission 1 and stop it when `make test` confirms all four missions:

| Total time | Rating |
|------------|--------|
| Under 2.5 hrs | Outstanding |
| 2.5–3 hrs | Excellent |
| 3–3.5 hrs | Qualified |
| 3.5–4 hrs | Passed |
| 4+ hrs | Return to AIT — retry |

ARIA also keeps time for you. `make setup` records the start, and when all four missions pass `make test` reports your performance tier from the elapsed time.

From `make setup` onwards, a background scoring poller probes every node's SSH port every 10 seconds, the way a cyber-exercise scoreboard measures uptime. `make test` reports an **Exercise score** (out of 100) that blends service availability across the whole run with objective completion. A remediation that takes a node offline costs you availability, so keep the fleet reachable while you rebuild it. `make reset` and `make destroy` stop the poller.

## Available Commands

```
make help       Show available commands
make doctor     Check your machine is mission-ready (Docker, ports, tools)
make setup      Launch 6-node Iron Curtain fleet (starts the clock and the scoring poller)
make test       Run ARIA assessment verification
make incident   Trigger the surprise incident (Mission 4)
make submit     Submit your work for ARIA review (branch, commit, push, PR)
make reset      Destroy and rebuild all nodes
make destroy    Tear down everything (containers, keys, venv)
make ssh-web-1  SSH into sdc-iron-web-1 (Ubuntu, port 2281)
make ssh-web-2  SSH into sdc-iron-web-2 (Ubuntu, port 2282)
make ssh-db-1   SSH into sdc-iron-db-1 (Rocky Linux, port 2283)
make ssh-db-2   SSH into sdc-iron-db-2 (Rocky Linux, port 2284)
make ssh-app    SSH into sdc-iron-app (Ubuntu, port 2285)
make ssh-comms  SSH into sdc-iron-comms (Ubuntu, port 2286)
```

> **Note:** `make submit` uses the [GitHub CLI](https://cli.github.com/) — install `gh` and run `gh auth login` once before your first submission.

## Mission Files

| File | Purpose |
|------|---------|
| [BRIEFING.md](docs/BRIEFING.md) | Orders: situation, threat profile, rules of engagement, deliverables per mission — **read this first** |
| [HINTS.md](docs/HINTS.md) | Troubleshooting and quick references |
| [CHECKLIST.md](CHECKLIST.md) | Progress tracker, with space to record your times |
| [ASSESSMENT.md](workspace/ASSESSMENT.md) | Your assessment report (Missions 1–2) |
| [PIPELINE.md](workspace/PIPELINE.md) | Your pipeline documentation (Mission 3) |
| [INCIDENT.md](workspace/INCIDENT.md) | Your incident report (Mission 4) |

There is deliberately no `EXERCISES.md`: the simulations are assessments — orders, not walkthroughs.

## Checking Your Work: `make test`

`make test` runs ARIA's grader (`molecule/default/tests/test_iron_curtain.py`) against the running fleet and reports each objective, mission by mission. It runs Ansible ad-hoc commands against the nodes (connectivity, effective SSH configuration, file permissions, incident remediation) and inspects your workspace files, so the fleet must be up. It needs no API key and works offline.

- Run it as often as you like; the simulation is complete when all four missions are green.
- `make reset` rebuilds all six containers (and restarts the clock and the scoring poller). Your `workspace/` files are preserved.
- Your CI and drift-detection workflows live under `workspace/.github/workflows/`. GitHub only runs workflows from the repository's top-level `.github/workflows/`, so they are graded as files, not executed.

## Submission and ARIA Review

When `make test` is green, `make submit` creates a `mission-submission` branch (or uses your current branch if you are not on `main`), commits `workspace/` and `CHECKLIST.md`, pushes, and opens a pull request to `main` in **your own** copy. You can also do this by hand with `git` and the GitHub web UI. `workspace/.vault-pass` is in `.gitignore`, so your Vault password file is not committed.

Opening or updating the pull request runs the **ARIA Review** workflow (`.github/workflows/aria-review.yml`). It does not re-run the grader — the deterministic checks need the Docker lab, so your local `make test` is the verdict. Instead, ARIA reads your submitted files, including `ASSESSMENT.md`, `PIPELINE.md` and `INCIDENT.md`, and posts a qualitative, in-character review as a PR comment. Each new push updates the same comment.

To enable PR reviews, add an API key to your repo:
1. Get a key from [platform.claude.com](https://platform.claude.com/)
2. In your repo: **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
3. Name: `ANTHROPIC_API_KEY`, Value: your key

Without a key, the comment says the review was skipped and the check still passes; `make test` works locally either way.

## Hints Policy

At this rung you get the scenario description and full autonomy. There are no exercises and no worked solutions. [HINTS.md](docs/HINTS.md) is limited to troubleshooting (SSH, Lynis on Rocky, sysctl in containers, Rocky vs Ubuntu differences, Vault, `serial`, `ansible-lint`, Molecule, `make incident`) and a few quick-reference commands. Your best guides are the briefing, your own work from Modules 1 and 2, and ARIA's messages in `make test`. For deeper reference, see [FM-3 — Molecule & Testing Reference](https://github.com/starfall-defence-corps/sdc-academy/blob/main/field-manuals/FM-3-molecule-testing-reference.md) and [FM-4 — CIS & Compliance Reference](https://github.com/starfall-defence-corps/sdc-academy/blob/main/field-manuals/FM-4-cis-compliance-reference.md).

## Troubleshooting

**SSH issues**: Run `make setup` first, then check `docker ps` shows all 6 containers.

**Rocky Linux differs**: `dnf` not `apt`, `firewalld` not `ufw`, `sshd` not `ssh` — your role must handle both OS families.

**`make incident` does nothing**: Run it from the project root, not from `workspace/`, with all containers running.

**`make test` fails with "No module named pytest"**: Run `make setup` first — it creates the Python virtual environment.

**Need a clean slate**: `make reset` destroys and rebuilds all nodes; `make destroy` tears everything down.
