"""
=== STARFALL DEFENCE CORPS ACADEMY ===
ARIA Automated Verification — Master Simulation: Operation Iron Curtain
=======================================================================
"""
import os
import re
import subprocess
import yaml
import pytest


def _root_dir():
    """Return the mission root directory."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(tests_dir, "..", "..", ".."))


def _workspace_dir():
    return os.path.join(_root_dir(), "workspace")


def _role_dir():
    return os.path.join(_workspace_dir(), "roles", "iron_curtain")


def _run_ansible(*args, **kwargs):
    """Run an ansible command from the workspace directory."""
    timeout = kwargs.pop("timeout", 120)
    result = subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=_workspace_dir(),
    )
    return result


def _file_exists(rel_path):
    """Check if a file exists relative to workspace."""
    return os.path.isfile(os.path.join(_workspace_dir(), rel_path))


def _file_contains(rel_path, pattern):
    """Check if a file contains a regex pattern."""
    path = os.path.join(_workspace_dir(), rel_path)
    if not os.path.isfile(path):
        return False
    with open(path) as f:
        content = f.read()
    return bool(re.search(pattern, content, re.MULTILINE))


def _read_file(rel_path):
    """Read a file relative to workspace."""
    path = os.path.join(_workspace_dir(), rel_path)
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return f.read()


def _collect_keys(obj, keys_set):
    """Recursively collect all dictionary keys."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys_set.add(k)
            _collect_keys(v, keys_set)
    elif isinstance(obj, list):
        for item in obj:
            _collect_keys(item, keys_set)


# -------------------------------------------------------------------
# Mission 1: Assessment
# -------------------------------------------------------------------

class TestAssessment:
    """ARIA verifies: Has the Lieutenant assessed the Iron Curtain fleet?"""

    def test_inventory_exists(self):
        """Inventory file must exist"""
        assert _file_exists("inventory/hosts.yml"), (
            "ARIA: No inventory found at inventory/hosts.yml. "
            "Write your fleet inventory — 6 nodes, 2 OS families."
        )

    def test_inventory_has_groups(self):
        """Inventory must define debian and redhat groups"""
        path = os.path.join(_workspace_dir(), "inventory", "hosts.yml")
        if not os.path.isfile(path):
            pytest.skip("Inventory does not exist yet")
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, "ARIA: Inventory file is empty."
        all_keys = set()
        _collect_keys(data, all_keys)
        has_debian = any(k in all_keys for k in ("debian", "Debian"))
        has_redhat = any(k in all_keys for k in ("redhat", "RedHat", "redhat_servers"))
        assert has_debian and has_redhat, (
            "ARIA: Inventory must define 'debian' and 'redhat' groups. "
            "The fleet runs 4 Ubuntu + 2 Rocky Linux."
        )

    def test_inventory_has_six_hosts(self):
        """Inventory must include all 6 nodes"""
        path = os.path.join(_workspace_dir(), "inventory", "hosts.yml")
        if not os.path.isfile(path):
            pytest.skip("Inventory does not exist yet")
        with open(path) as f:
            content = f.read()
        # Count host entries by looking for port definitions
        port_matches = re.findall(r"ansible_port:\s*\d+", content)
        assert len(port_matches) >= 6, (
            f"ARIA: Only {len(port_matches)} host(s) found in inventory. "
            "The Iron Curtain fleet has 6 nodes."
        )

    def test_group_vars_exist(self):
        """group_vars files must exist for OS-specific settings"""
        gv_dir = os.path.join(_workspace_dir(), "inventory", "group_vars")
        if not os.path.isdir(gv_dir):
            gv_dir = os.path.join(_workspace_dir(), "group_vars")
        assert os.path.isdir(gv_dir), (
            "ARIA: No group_vars directory found. Create "
            "inventory/group_vars/ with OS-specific variables."
        )
        files = os.listdir(gv_dir)
        yml_files = [f for f in files if f.endswith((".yml", ".yaml"))]
        assert len(yml_files) >= 2, (
            "ARIA: group_vars needs at least 2 files (one per OS family)."
        )

    def test_assessment_md_exists(self):
        """ASSESSMENT.md must exist and contain findings"""
        assert _file_exists("ASSESSMENT.md"), (
            "ARIA: ASSESSMENT.md not found in workspace/."
        )
        content = _read_file("ASSESSMENT.md")
        # Look for filled Lynis score cells in the baseline table
        # The template has empty cells: "| sdc-iron-web-1 | | | |"
        # A filled entry looks like: "| sdc-iron-web-1 | 52 | | |"
        # Match: node name, pipe, then a number (the baseline score)
        score_pattern = r"sdc-iron-\w+\s*\|\s*\d{2}"
        has_scores = bool(re.search(score_pattern, content))
        assert has_scores, (
            "ARIA: ASSESSMENT.md has no Lynis scores recorded. "
            "Run Lynis baseline scans and document the results."
        )

    def test_connectivity(self):
        """All 6 nodes must be reachable via ansible ping"""
        path = os.path.join(_workspace_dir(), "inventory", "hosts.yml")
        if not os.path.isfile(path):
            pytest.skip("Inventory does not exist yet")
        result = _run_ansible("ansible", "all", "-m", "ping")
        # Count SUCCESS responses
        successes = result.stdout.count("SUCCESS")
        assert successes >= 6, (
            f"ARIA: Only {successes} of 6 nodes responded to ping. "
            "Check your inventory and SSH configuration."
        )


# -------------------------------------------------------------------
# Mission 2: Remediation
# -------------------------------------------------------------------

class TestRemediation:
    """ARIA verifies: Has the Lieutenant hardened the Iron Curtain fleet?"""

    def test_role_exists(self):
        """Role must exist at roles/iron_curtain/"""
        assert os.path.isdir(_role_dir()), (
            "ARIA: No role found at roles/iron_curtain/. "
            "Create it with: ansible-galaxy init roles/iron_curtain"
        )

    def test_tasks_have_content(self):
        """tasks/main.yml must have at least 8 CIS tasks"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "tasks", "main.yml")
        assert os.path.isfile(path), "ARIA: tasks/main.yml not found."
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None and isinstance(data, list) and len(data) >= 8, (
            f"ARIA: tasks/main.yml has {len(data) if data else 0} task(s). "
            "Need at least 8 CIS controls."
        )

    def test_tasks_have_tags(self):
        """CIS tasks must have tags"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "tasks", "main.yml")
        if not os.path.isfile(path):
            pytest.skip("tasks/main.yml does not exist yet")
        with open(path) as f:
            content = f.read()
        tag_count = len(re.findall(r"tags:\s*\[", content))
        assert tag_count >= 5, (
            f"ARIA: Only {tag_count} task(s) have tags. "
            "Every CIS task must have a tag: tags: [cis_X_Y]"
        )

    def test_handlers_exist(self):
        """handlers/main.yml must have service restart handlers"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "handlers", "main.yml")
        assert os.path.isfile(path), "ARIA: handlers/main.yml not found."
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None and isinstance(data, list) and len(data) >= 1, (
            "ARIA: handlers/main.yml is empty. Add SSH restart handler."
        )

    def test_defaults_have_variables(self):
        """defaults/main.yml must have configurable variables"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        defaults = os.path.join(_role_dir(), "defaults", "main.yml")
        role_vars = os.path.join(_role_dir(), "vars", "main.yml")
        has_content = False
        for p in (defaults, role_vars):
            if os.path.isfile(p):
                with open(p) as f:
                    data = yaml.safe_load(f)
                if data and isinstance(data, dict) and len(data) >= 1:
                    has_content = True
                    break
        assert has_content, (
            "ARIA: No variables defined in defaults/ or vars/."
        )

    def test_templates_exist(self):
        """templates/ must have at least sshd_config.j2"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "templates")
        if not os.path.isdir(path):
            assert False, "ARIA: templates/ directory not found."
        templates = [f for f in os.listdir(path) if f.endswith(".j2")]
        assert len(templates) >= 1, (
            "ARIA: No .j2 templates found. Create sshd_config.j2 at minimum."
        )

    def test_site_yml_uses_serial(self):
        """site.yml must use serial for rolling deployment"""
        path = os.path.join(_workspace_dir(), "site.yml")
        if not os.path.isfile(path):
            pytest.skip("site.yml does not exist yet")
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None or not isinstance(data, list):
            pytest.skip("site.yml is empty or commented out")
        play = data[0]
        has_serial = "serial" in play
        assert has_serial, (
            "ARIA: site.yml does not use 'serial' for rolling deployment. "
            "Never deploy to all 6 nodes simultaneously."
        )

    def test_site_yml_references_role(self):
        """site.yml must reference the iron_curtain role"""
        path = os.path.join(_workspace_dir(), "site.yml")
        if not os.path.isfile(path):
            pytest.skip("site.yml does not exist yet")
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None or not isinstance(data, list):
            pytest.skip("site.yml is empty or commented out")
        play = data[0]
        roles = play.get("roles") or []
        role_names = []
        for r in roles:
            if isinstance(r, str):
                role_names.append(r)
            elif isinstance(r, dict):
                role_names.append(r.get("role", r.get("name", "")))
        assert "iron_curtain" in role_names, (
            "ARIA: site.yml does not reference the iron_curtain role."
        )

    def test_vault_encrypted(self):
        """vault.yml must exist and be encrypted"""
        path = os.path.join(_workspace_dir(), "vault.yml")
        assert os.path.isfile(path), (
            "ARIA: vault.yml not found. Create and encrypt it."
        )
        with open(path) as f:
            first_line = f.readline().strip()
        assert first_line.startswith("$ANSIBLE_VAULT;"), (
            "ARIA: vault.yml is NOT encrypted."
        )

    def test_vault_pass_exists(self):
        """.vault-pass must exist"""
        assert _file_exists(".vault-pass"), (
            "ARIA: .vault-pass not found. Create it with the vault password."
        )

    def test_ssh_hardened(self):
        """SSH must be hardened on all nodes"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "all", "-m", "shell",
            "-a", "grep -E '^PermitRootLogin\\s+no' /etc/ssh/sshd_config",
        )
        assert result.returncode == 0, (
            "ARIA: SSH root login not disabled on all nodes."
        )

    def test_shadow_permissions(self):
        """Ubuntu nodes must have /etc/shadow at 0640"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "debian", "-m", "shell",
            "-a", "stat -c '%a' /etc/shadow",
        )
        if result.returncode != 0:
            pytest.skip("Cannot check shadow permissions")
        # All responses should be 640
        for line in result.stdout.splitlines():
            if "640" in line:
                continue
            if ">>" in line or "CHANGED" in line or "SUCCESS" in line:
                continue
            if line.strip() and line.strip().isdigit() and line.strip() != "640":
                assert False, (
                    "ARIA: /etc/shadow permissions incorrect on Ubuntu nodes. "
                    "Should be 0640."
                )

    def test_molecule_config_exists(self):
        """Molecule configuration must exist"""
        mol_path = os.path.join(_workspace_dir(), "molecule", "default", "molecule.yml")
        assert os.path.isfile(mol_path), (
            "ARIA: Molecule config not found at molecule/default/molecule.yml."
        )

    def test_testinfra_tests_exist(self):
        """Student Testinfra tests must exist with sufficient coverage"""
        tests_dir = os.path.join(_workspace_dir(), "tests")
        if not os.path.isdir(tests_dir):
            assert False, "ARIA: tests/ directory not found in workspace."
        test_files = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
        assert len(test_files) >= 1, (
            "ARIA: No test files found in tests/."
        )
        # Check test count in the first test file
        test_path = os.path.join(tests_dir, test_files[0])
        with open(test_path) as f:
            content = f.read()
        test_count = len(re.findall(r"def test_", content))
        assert test_count >= 8, (
            f"ARIA: Only {test_count} test function(s) found. "
            "Need at least 8 to verify CIS compliance."
        )


# -------------------------------------------------------------------
# Mission 3: Automation
# -------------------------------------------------------------------

class TestAutomation:
    """ARIA verifies: Has the Lieutenant automated the pipeline?"""

    def test_ci_workflow_exists(self):
        """CI workflow must exist"""
        ci_path = os.path.join(_workspace_dir(), ".github", "workflows", "ci.yml")
        assert os.path.isfile(ci_path), (
            "ARIA: CI workflow not found at .github/workflows/ci.yml."
        )

    def test_ci_workflow_has_stages(self):
        """CI workflow must have lint and test stages"""
        ci_path = os.path.join(_workspace_dir(), ".github", "workflows", "ci.yml")
        if not os.path.isfile(ci_path):
            pytest.skip("CI workflow does not exist yet")
        with open(ci_path) as f:
            content = f.read()
        has_lint = bool(re.search(r"lint", content, re.IGNORECASE))
        has_test = bool(re.search(r"test", content, re.IGNORECASE))
        has_needs = bool(re.search(r"needs:", content))
        assert has_lint and has_test, (
            "ARIA: CI workflow missing lint or test stage."
        )
        assert has_needs, (
            "ARIA: CI workflow has no 'needs' keyword. "
            "Stages should depend on each other."
        )

    def test_ci_workflow_has_matrix(self):
        """CI workflow should use matrix strategy for multi-OS"""
        ci_path = os.path.join(_workspace_dir(), ".github", "workflows", "ci.yml")
        if not os.path.isfile(ci_path):
            pytest.skip("CI workflow does not exist yet")
        with open(ci_path) as f:
            content = f.read()
        has_matrix = bool(re.search(r"matrix:", content))
        assert has_matrix, (
            "ARIA: CI workflow has no matrix strategy. "
            "Test across both OS families."
        )

    def test_drift_workflow_exists(self):
        """Drift detection workflow must exist with schedule trigger"""
        drift_path = os.path.join(
            _workspace_dir(), ".github", "workflows", "drift-detection.yml"
        )
        assert os.path.isfile(drift_path), (
            "ARIA: Drift detection workflow not found at "
            ".github/workflows/drift-detection.yml."
        )

    def test_drift_workflow_has_schedule(self):
        """Drift detection workflow must use schedule trigger"""
        drift_path = os.path.join(
            _workspace_dir(), ".github", "workflows", "drift-detection.yml"
        )
        if not os.path.isfile(drift_path):
            pytest.skip("Drift workflow does not exist yet")
        with open(drift_path) as f:
            content = f.read()
        has_schedule = bool(re.search(r"schedule:", content))
        has_cron = bool(re.search(r"cron:", content))
        assert has_schedule and has_cron, (
            "ARIA: Drift workflow has no schedule/cron trigger."
        )

    def test_drift_workflow_has_notification(self):
        """Drift workflow must create issue on failure"""
        drift_path = os.path.join(
            _workspace_dir(), ".github", "workflows", "drift-detection.yml"
        )
        if not os.path.isfile(drift_path):
            pytest.skip("Drift workflow does not exist yet")
        with open(drift_path) as f:
            content = f.read()
        has_issue = bool(re.search(r"issue", content, re.IGNORECASE))
        assert has_issue, (
            "ARIA: Drift workflow has no failure notification. "
            "Create a GitHub issue when drift is detected."
        )

    def test_makefile_exists(self):
        """Makefile must exist with lint, test, scan targets"""
        mk_path = os.path.join(_workspace_dir(), "Makefile")
        assert os.path.isfile(mk_path), (
            "ARIA: Makefile not found in workspace/."
        )
        with open(mk_path) as f:
            content = f.read()
        has_lint = bool(re.search(r"^lint:", content, re.MULTILINE))
        has_test = bool(re.search(r"^test:", content, re.MULTILINE))
        has_scan = bool(re.search(r"^scan:", content, re.MULTILINE))
        assert has_lint and has_test and has_scan, (
            "ARIA: Makefile missing required targets. "
            "Need: lint, test, scan."
        )

    def test_ansible_lint_config(self):
        """ansible-lint configuration must exist"""
        lint_path = os.path.join(_workspace_dir(), ".ansible-lint")
        assert os.path.isfile(lint_path), (
            "ARIA: .ansible-lint config not found in workspace/."
        )

    def test_pipeline_md_completed(self):
        """PIPELINE.md must be completed with pipeline documentation"""
        assert _file_exists("PIPELINE.md"), (
            "ARIA: PIPELINE.md not found in workspace/."
        )
        content = _read_file("PIPELINE.md")
        # Strip template content (HTML comments, headers, table headers)
        lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if (stripped
                    and not stripped.startswith("#")
                    and not stripped.startswith("<!--")
                    and not stripped.startswith("-->")
                    and not stripped.startswith("|")
                    and not stripped.startswith("---")):
                lines.append(stripped)
        assert len(lines) >= 10, (
            "ARIA: PIPELINE.md appears mostly empty. "
            "Document your CI/CD pipeline design."
        )


# -------------------------------------------------------------------
# Mission 4: Incident
# -------------------------------------------------------------------

class TestIncident:
    """ARIA verifies: Has the Lieutenant handled the incident?"""

    def test_incident_md_exists(self):
        """INCIDENT.md must exist and contain findings"""
        assert _file_exists("INCIDENT.md"), (
            "ARIA: INCIDENT.md not found in workspace/."
        )
        content = _read_file("INCIDENT.md")
        # Check that it's been filled in beyond the template
        lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if (stripped
                    and not stripped.startswith("#")
                    and not stripped.startswith("<!--")
                    and not stripped.startswith("-->")
                    and not stripped.startswith("|")
                    and not stripped.startswith("---")
                    and not stripped.startswith("- **")):
                lines.append(stripped)
        assert len(lines) >= 8, (
            "ARIA: INCIDENT.md appears mostly empty. "
            "Document the incident: what happened, what you found, "
            "what you did."
        )

    def test_incident_identifies_node(self):
        """INCIDENT.md must identify the compromised node"""
        content = _read_file("INCIDENT.md")
        if content is None:
            pytest.skip("INCIDENT.md does not exist yet")
        # The compromised node is sdc-iron-web-2
        has_node = bool(re.search(r"sdc-iron-web-2|web-2|iron-web-2", content, re.IGNORECASE))
        assert has_node, (
            "ARIA: INCIDENT.md does not identify the correct compromised node."
        )

    def test_compromised_node_remediated_ssh(self):
        """Compromised node must have SSH re-hardened"""
        # Check if incident has been triggered (marker file exists)
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "test -f /opt/.compromised && echo INCIDENT || echo CLEAN",
        )
        if "INCIDENT" not in result.stdout:
            pytest.skip("Incident not yet triggered — run 'make incident' first")
        # Now check SSH is hardened
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "grep -E '^PermitRootLogin\\s+no' /etc/ssh/sshd_config",
        )
        assert result.returncode == 0, (
            "ARIA: Compromised node sdc-iron-web-2 still has SSH misconfigured. "
            "Re-apply your hardening role."
        )

    def test_compromised_node_rogue_user_removed(self):
        """Rogue user must be removed from compromised node"""
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "test -f /opt/.compromised && echo INCIDENT || echo CLEAN",
        )
        if "INCIDENT" not in result.stdout:
            pytest.skip("Incident not yet triggered")
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "id intruder 2>/dev/null && echo EXISTS || echo GONE",
        )
        assert "EXISTS" not in result.stdout, (
            "ARIA: Rogue user 'intruder' still exists on sdc-iron-web-2. "
            "Remove unauthorised accounts."
        )

    def test_compromised_node_cron_cleaned(self):
        """Suspicious cron job must be removed"""
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "test -f /opt/.compromised && echo INCIDENT || echo CLEAN",
        )
        if "INCIDENT" not in result.stdout:
            pytest.skip("Incident not yet triggered")
        result = _run_ansible(
            "ansible", "sdc-iron-web-2", "-m", "shell",
            "-a", "test -f /etc/cron.d/voidborn-beacon && echo FOUND || echo CLEAN",
        )
        assert "FOUND" not in result.stdout, (
            "ARIA: Suspicious cron job still present at /etc/cron.d/voidborn-beacon. "
            "Remove all Voidborn persistence mechanisms."
        )
