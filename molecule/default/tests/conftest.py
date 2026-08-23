"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for Operation Iron Curtain verification.

Writes all output to stderr so check-work.sh can discard pytest's
default stdout while preserving our formatted display.
"""
import os
import pytest
import sys

# -- Phase and test name mappings -------------------------------------------

PHASES = {
    "TestAssessment":   ("1", "Assessment"),
    "TestRemediation":  ("2", "Remediation"),
    "TestAutomation":   ("3", "Automation"),
    "TestIncident":     ("4", "Incident"),
}

FRIENDLY = {
    # Mission 1
    "test_inventory_exists":            "Inventory file exists",
    "test_inventory_has_groups":        "Inventory has debian/redhat groups",
    "test_inventory_has_six_hosts":     "Inventory includes all 6 nodes",
    "test_group_vars_exist":            "group_vars files exist",
    "test_assessment_md_exists":        "ASSESSMENT.md has Lynis scores",
    "test_connectivity":                "All 6 nodes reachable",
    # Mission 2
    "test_role_exists":                 "Role directory exists",
    "test_tasks_have_content":          "tasks/main.yml has 8+ CIS tasks",
    "test_tasks_have_tags":             "CIS tasks are tagged",
    "test_handlers_exist":              "handlers/main.yml has handlers",
    "test_defaults_have_variables":     "defaults/ has variable definitions",
    "test_templates_exist":             "templates/ has .j2 files",
    "test_site_yml_uses_serial":        "site.yml uses serial deployment",
    "test_site_yml_references_role":    "site.yml references iron_curtain role",
    "test_vault_encrypted":             "vault.yml is encrypted",
    "test_vault_pass_exists":           ".vault-pass file exists",
    "test_ssh_hardened":                "SSH hardened on all nodes",
    "test_shadow_permissions":          "/etc/shadow permissions correct",
    "test_molecule_config_exists":      "Molecule configuration exists",
    "test_testinfra_tests_exist":       "Testinfra tests (8+ functions)",
    # Mission 3
    "test_ci_workflow_exists":          "CI workflow exists",
    "test_ci_workflow_has_stages":      "CI has lint/test stages with needs",
    "test_ci_workflow_has_matrix":      "CI uses matrix strategy",
    "test_drift_workflow_exists":       "Drift detection workflow exists",
    "test_drift_workflow_has_schedule": "Drift workflow has schedule trigger",
    "test_drift_workflow_has_notification": "Drift workflow creates issue on failure",
    "test_makefile_exists":             "Makefile has lint/test/scan targets",
    "test_ansible_lint_config":         ".ansible-lint config exists",
    "test_pipeline_md_completed":       "PIPELINE.md completed",
    # Mission 4
    "test_incident_md_exists":          "INCIDENT.md has findings",
    "test_incident_identifies_node":    "Compromised node identified",
    "test_compromised_node_remediated_ssh": "Compromised node SSH re-hardened",
    "test_compromised_node_rogue_user_removed": "Rogue user removed",
    "test_compromised_node_cron_cleaned": "Suspicious cron job removed",
}

# -- Reporter ---------------------------------------------------------------

# The phase-oriented summary is rendered by the shared `aria-reporter`
# pytest plugin (installed via requirements.txt); this file only declares
# the mission's phases + friendly objective names.
from aria_reporter import configure  # noqa: E402

configure(
    phases=PHASES, friendly=FRIENDLY,
    mission_id="master", unit="Mission",
)
