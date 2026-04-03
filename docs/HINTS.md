# Operation: Iron Curtain — Hints

> Back to: [Briefing](BRIEFING.md) | [Checklist](../CHECKLIST.md)

## Troubleshooting

**SSH issues**: Run `make setup` first. Check `docker ps` to verify 6 containers are running.

**Lynis not found**: Lynis is pre-installed on Ubuntu containers only. Rocky Linux nodes don't have Lynis — focus Lynis scans on Ubuntu nodes, or install it manually.

**sysctl errors in Docker**: Some sysctl parameters can't be set in Docker containers. Use `ignore_errors: true` for those, or check if the parameter exists first with `when`.

**Rocky Linux packages differ**: Rocky uses `dnf` instead of `apt`, `firewalld` instead of `ufw`, `sshd` instead of `ssh`. Your role must handle both OS families with `when: ansible_os_family`.

**Vault password**: The briefing specifies `iron-curtain` as the vault password. ARIA checks for this.

**Serial deployment**: Use `serial: 2` or `serial: "33%"` in your play to roll updates across the fleet. Don't deploy to all 6 nodes simultaneously.

**ansible-lint warnings**: Some rules can be safely added to `skip_list` in `.ansible-lint`. Common ones: `yaml[truthy]`, `no-changed-when`.

**Molecule in workspace**: Your Molecule config at `workspace/molecule/default/molecule.yml` should reference unmanaged platforms matching your inventory.

**Incident not triggering**: Run `make incident` from the repo root (not from `workspace/`). Ensure all containers are running.

**Need a clean slate**: Run `make reset` to rebuild all 6 containers. Your workspace files are preserved.

## Quick References

**CIS tag format**: `tags: [cis_5_2]` — underscore-separated section numbers.

**Lynis ad-hoc scan**:
```bash
ansible debian -m shell -a "lynis audit system --quick --no-colors 2>/dev/null | tail -5"
```

**Connectivity test**:
```bash
cd workspace
ansible all -m ping
```

**Check SSH config on a node**:
```bash
ansible sdc-iron-web-1 -m shell -a "grep -E 'PermitRootLogin|PasswordAuth|MaxAuthTries' /etc/ssh/sshd_config"
```
