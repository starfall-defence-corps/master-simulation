# Operation: Iron Curtain — Progress Checklist

**Start time**: _______________

---

## Mission 1: Assessment (40 min)

- [ ] Fleet online (`make setup`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Inventory written (`workspace/inventory/hosts.yml`)
- [ ] group_vars created for both OS families
- [ ] `ansible all -m ping` succeeds on all 6 nodes
- [ ] Lynis baseline scores recorded
- [ ] CIS violations documented in ASSESSMENT.md
- [ ] Remediation plan written

## Mission 2: Remediation (75 min)

- [ ] Role created (`workspace/roles/iron_curtain/`)
- [ ] defaults/main.yml has configurable variables
- [ ] tasks/main.yml has CIS controls (8+ tasks)
- [ ] All tasks tagged with CIS section (e.g., `tags: [cis_5_2]`)
- [ ] handlers/main.yml has service restart handlers
- [ ] templates/sshd_config.j2 created
- [ ] site.yml uses `serial` for rolling deploy
- [ ] vault.yml created and encrypted (password: `iron-curtain`)
- [ ] .vault-pass file created
- [ ] ansible.cfg updated with vault_password_file
- [ ] First run: nodes hardened
- [ ] Second run: `changed=0` (idempotent)
- [ ] Molecule configuration created (`workspace/molecule/default/molecule.yml`)
- [ ] Testinfra tests written (`workspace/tests/test_iron_curtain.py`, 8+ functions)
- [ ] Post-hardening Lynis scores in ASSESSMENT.md

## Mission 3: Automation (60 min)

- [ ] CI workflow (`workspace/.github/workflows/ci.yml`)
- [ ] Workflow has lint and test stages with `needs`
- [ ] Matrix strategy for multi-OS testing
- [ ] Drift detection workflow (`workspace/.github/workflows/drift-detection.yml`)
- [ ] Drift workflow uses `schedule` trigger
- [ ] Failure notification creates GitHub issue
- [ ] Makefile with `lint`, `test`, `scan` targets
- [ ] `.ansible-lint` configuration
- [ ] PIPELINE.md completed

## Mission 4: Incident (35 min)

- [ ] `make incident` triggered (after Missions 1-3)
- [ ] Compromised node identified
- [ ] Unauthorised changes documented
- [ ] Node remediated
- [ ] All nodes pass compliance checks
- [ ] INCIDENT.md completed with timeline

---

## Final Verification

- [ ] `make test` — all 4 missions pass

**End time**: _______________

**Total time**: _______________

| Total Time | Rating |
|------------|--------|
| Under 2.5 hrs | Outstanding |
| 2.5–3 hrs | Excellent |
| 3–3.5 hrs | Qualified |
| 3.5–4 hrs | Passed |
| 4+ hrs | Return to AIT — retry |
