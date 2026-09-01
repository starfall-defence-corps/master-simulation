# Operation: Iron Curtain — Assessment Report

## Fleet Inventory

| Node | Hostname | OS | SSH Port | IP | Status |
|------|----------|----|----------|----|--------|
| sdc-iron-web-1 | | | 2281 | 172.36.0.11 | |
| sdc-iron-web-2 | | | 2282 | 172.36.0.12 | |
| sdc-iron-db-1 | | | 2283 | 172.36.0.13 | |
| sdc-iron-db-2 | | | 2284 | 172.36.0.14 | |
| sdc-iron-app | | | 2285 | 172.36.0.15 | |
| sdc-iron-comms | | | 2286 | 172.36.0.16 | |

## Lynis Baseline Scores

<!-- Run Lynis on each node BEFORE applying your role.
     Lynis is pre-installed on the Ubuntu nodes only (web-1, web-2, app,
     comms). The Rocky Linux db nodes (db-1, db-2) have no Lynis by default,
     so their rows are marked N/A — install it yourself and note that if you
     want scores. ARIA only requires baseline scores for the Ubuntu nodes.
     See HINTS.md ("Lynis not found"). -->

Ubuntu nodes: sdc-iron-web-1, sdc-iron-web-2, sdc-iron-app, sdc-iron-comms.
Rocky nodes (Lynis N/A): sdc-iron-db-1, sdc-iron-db-2.

| Node | Baseline Score | Post-Hardening Score | Improvement |
|------|---------------|---------------------|-------------|
| sdc-iron-web-1 | | | |
| sdc-iron-web-2 | | | |
| sdc-iron-db-1 | N/A | N/A | N/A |
| sdc-iron-db-2 | N/A | N/A | N/A |
| sdc-iron-app | | | |
| sdc-iron-comms | | | |

## CIS Violations Found

<!-- Document what you found during reconnaissance -->

### SSH (CIS 5.2.x)

### File Permissions (CIS 6.1.x)

### Kernel Parameters (CIS 3.x)

### Access Control (CIS 5.1.x)

### Initial Setup (CIS 1.x)

## CIS Controls Implemented

<!-- List each CIS control you implemented with its tag -->

| Control ID | Description | Ansible Tag | Status |
|-----------|-------------|-------------|--------|
| | | | |

## Remediation Plan

<!-- Your approach to bringing the fleet into compliance -->
