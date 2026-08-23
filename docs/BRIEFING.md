---
CLASSIFICATION: LIEUTENANT EYES ONLY
SIMULATION: MASTER — OPERATION: IRON CURTAIN
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# MASTER SIMULATION — OPERATION: IRON CURTAIN

---

## 1. SITUATION

### 1a. Enemy Forces

**Dread Admiral Snowflake** built this fleet by hand. Six servers. Every one different. Nothing documented. Nothing tested. Nothing automated. His defence: "I know where everything is." His incident response plan: "Call me."

Dread Admiral Snowflake has been relieved of command. You inherit his infrastructure.

The Voidborn have been probing the fleet for weeks. With no compliance baseline, no automated testing, and no drift detection, you have no way to know what's already been changed — or what's about to be.

### 1b. Friendly Forces

You have completed all of Module 2. You can:
- **Assess** systems against CIS benchmarks using Lynis (Mission 2.2)
- **Test** infrastructure with Molecule and Testinfra (Mission 2.1)
- **Deploy** with rolling updates and error handling (Mission 2.3)
- **Automate** with CI/CD pipelines and drift detection (Mission 2.4)
- Plus every skill from Module 1: inventory, roles, Vault, templates, handlers, multi-OS support

This simulation requires all of it.

### 1c. Attachments / Support

**ARIA** will verify your work across four missions. Run `make test` at any time.

**Lynis** is pre-installed on all Ubuntu containers. Use it to measure your hardening index before and after applying your role.

---

## 2. MISSION

Replace Dread Admiral Snowflake's hand-built infrastructure with uniform, tested, automated CIS compliance across all six nodes.

| Mission | Description | Time |
|---------|-------------|------|
| 1 — Assessment | Inventory, baseline, document | 40 min |
| 2 — Remediation | CIS role, deploy, test, improve | 75 min |
| 3 — Automation | CI pipeline, lint, drift detection | 60 min |
| 4 — Incident | Detect, identify, remediate, document | 35 min |

**Total**: 3.5 hours

---

## 3. EXECUTION

### 3a. Commander's Intent

Dread Admiral Snowflake's reign of hand-built infrastructure ends today. When this simulation is complete, the fleet will have: a CIS-compliant hardening role with tagged controls, Molecule tests proving compliance, a CI pipeline enforcing quality, drift detection catching unauthorised changes, and documentation proving all of it.

### 3b. Lab Assets

**Iron Curtain Fleet** (6 nodes):

| Designation | OS | SSH Port | IP | Role |
|-------------|----|----------|----|------|
| `sdc-iron-web-1` | Ubuntu 22.04 | 2281 | 172.36.0.11 | Web server |
| `sdc-iron-web-2` | Ubuntu 22.04 | 2282 | 172.36.0.12 | Web server |
| `sdc-iron-db-1` | Rocky Linux 9 | 2283 | 172.36.0.13 | Database |
| `sdc-iron-db-2` | Rocky Linux 9 | 2284 | 172.36.0.14 | Database |
| `sdc-iron-app` | Ubuntu 22.04 | 2285 | 172.36.0.15 | Application |
| `sdc-iron-comms` | Ubuntu 22.04 | 2286 | 172.36.0.16 | Communications |

**SSH user**: `cadet` (key-based auth, key at `workspace/.ssh/cadet_key`)

### 3c. Known Threat Profile

All containers ship with Dread Admiral Snowflake's misconfigurations:

**SSH (CIS 5.2.x)**:
- Root login enabled, password authentication enabled
- MaxAuthTries 6 (should be 4 or less)
- LoginGraceTime 120 (should be 60 or less)
- ClientAliveInterval 0 (should be 300)

**Filesystem (CIS 6.1.x)**:
- `/etc/shadow` permissions 0644 (should be 0640) — Ubuntu nodes
- `/etc/gshadow` permissions 0644 (should be 0640) — Ubuntu nodes

**Kernel (CIS 3.x)**:
- IP forwarding enabled
- ICMP redirects accepted

**Access Control (CIS 5.1.x)**:
- No `/etc/cron.allow` (cron unrestricted)
- No `/etc/at.allow` (at unrestricted)

**Initial Setup (CIS 1.x)**:
- Core dumps unrestricted
- No login banner (`/etc/issue.net` missing)

**Services**:
- `telnet` and `xinetd` installed on Ubuntu nodes
- Hardcoded credentials at `/opt/fleet-db-creds.txt`

### 3d. Lynis Quick Reference

```bash
# Full audit (quick mode)
lynis audit system --quick --no-colors

# Last 5 lines include the hardening index
lynis audit system --quick --no-colors 2>/dev/null | tail -5

# Via Ansible ad-hoc on all Ubuntu nodes
ansible debian -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

### 3e. Rules of Engagement

- Every CIS task must have a tag matching the control section (e.g., `tags: [cis_5_2]`)
- Lynis scores are your evidence — record before and after in `workspace/ASSESSMENT.md`
- You may consult CIS benchmark documentation and Ansible docs
- No looking at other missions' solution files

---

## 4. MISSION DETAILS

### Mission 1: Assessment (40 min)

**Objective**: Understand the current state of all six nodes.

**Deliverables** (all paths relative to `workspace/`):
1. **`inventory/hosts.yml`** — Full inventory with `debian` and `redhat` groups
2. **`inventory/group_vars/debian.yml`** and **`inventory/group_vars/redhat.yml`** — OS-specific variables
3. **`ASSESSMENT.md`** — Completed with:
   - Fleet inventory table filled in
   - Lynis baseline scores for each node
   - CIS violations documented per category
   - Remediation plan

**Verification**: `ansible all -m ping` succeeds on all 6 nodes.

### Mission 2: Remediation (75 min)

**Objective**: Bring the entire fleet into CIS Level 1 compliance.

**Deliverables** (all paths relative to `workspace/`):
1. **`roles/iron_curtain/`** — CIS hardening role with:
   - `tasks/main.yml` — CIS controls with tags (minimum 8 tasks)
   - `handlers/main.yml` — Service restart handlers
   - `defaults/main.yml` — Configurable variables
   - `templates/` — At least `sshd_config.j2`
2. **`site.yml`** — Playbook using `serial` for rolling deployment
3. **`vault.yml`** — Encrypted sensitive variables
4. **`.vault-pass`** — Vault password file (use password: `iron-curtain`)
5. **`molecule/default/molecule.yml`** — Molecule configuration
6. **`tests/test_iron_curtain.py`** — At least 8 Testinfra test functions
7. **`ASSESSMENT.md`** — Updated with post-hardening Lynis scores

**Requirements**:
- Role must be idempotent (second run: `changed=0`)
- Deploy with `serial` (rolling update — do not hit all 6 at once)
- All CIS tasks tagged with control section
- Lynis improvement documented

### Mission 3: Automation (60 min)

**Objective**: Build the CI/CD pipeline that prevents Dread Admiral Snowflake from ever happening again.

**Deliverables** (all paths relative to `workspace/`):
1. **`.github/workflows/ci.yml`** — CI workflow with:
   - Trigger on push/PR to main
   - Stages: lint → test (with matrix for both OS families)
   - `needs` keyword for stage dependencies
2. **`.github/workflows/drift-detection.yml`** — Scheduled workflow with:
   - Weekly cron trigger
   - Molecule verify against fleet
   - Create GitHub issue on failure
3. **`Makefile`** — Targets: `lint`, `test`, `scan`
4. **`.ansible-lint`** — Linting configuration
5. **`PIPELINE.md`** — Completed pipeline documentation

### Mission 4: Incident (35 min — triggered by `make incident`)

**Objective**: Detect, identify, and remediate a Voidborn compromise.

> **Do NOT run `make incident` until Missions 1-3 are complete.**

After running `make incident`, ARIA will report anomalous activity. One or more nodes have been compromised.

**Deliverables** (all paths relative to `workspace/`):
1. **`INCIDENT.md`** — Completed with:
   - Compromised node(s) identified
   - Specific changes documented
   - Timeline of investigation
   - Remediation steps taken
   - Verification that node is clean

**Requirements**:
- Identify the correct compromised node
- Remediate all unauthorised changes
- All nodes must pass compliance checks after remediation

---

## 5. TIMING

> **START YOUR TIMER** at the beginning of Mission 1.

| Total Time | Rating |
|------------|--------|
| Under 2.5 hrs | Outstanding |
| 2.5–3 hrs | Excellent |
| 3–3.5 hrs | Qualified |
| 3.5–4 hrs | Passed |
| 4+ hrs | Return to AIT — retry |

> **STOP YOUR TIMER** after `make test` confirms all four missions pass.

---

## 6. COMMAND AND SIGNAL

**Commander's Final Order**: Dread Admiral Snowflake built six servers by hand and called it infrastructure. You will replace it with code. Measurable. Testable. Automated. When ARIA confirms all four missions, Dread Admiral Snowflake is relieved of duty and you earn the Iron Curtain badge.

**Rank Earned**: Lieutenant Commander
**Badge**: Iron Curtain — Master Operator

---

## 7. GETTING STARTED

1. Activate your environment: `source venv/bin/activate`
2. All work happens in the `workspace/` directory
3. Stuck? Consult [HINTS.md](HINTS.md) for troubleshooting
4. Track your progress: [CHECKLIST.md](../CHECKLIST.md)
5. Verify your work: `make test`

---

*SDC Cyber Command — 2187 — LIEUTENANT EYES ONLY*
