#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_FILE="$ROOT_DIR/molecule/default/tests/test_iron_curtain.py"

# -- Colors ----------------------------------------------------------------
GREEN='\033[32m'
RED='\033[31m'
CYAN='\033[36m'
YELLOW='\033[33m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

echo ""
echo -e "  ${CYAN}${BOLD}=============================================="
echo -e "  ARIA — Automated Review & Intelligence Analyst"
echo -e "  Master Simulation: Operation Iron Curtain"
echo -e "  ==============================================${RESET}"

cd "$ROOT_DIR"

# Activate project venv if it exists
if [ -f "$ROOT_DIR/venv/bin/activate" ]; then
    source "$ROOT_DIR/venv/bin/activate"
fi

# Run tests.
ARIA_COLOR=1 python3 -m pytest "$TEST_FILE" --tb=no --no-header -q 2>&1 1>/dev/null \
    | grep -vE '^(assert |FAILED| *\+  where|  *\+  |[0-9]+ (passed|failed))' || true
EXIT_CODE=${PIPESTATUS[0]}

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}=============================================="
    echo -e "  ARIA: All objectives verified."
    echo -e "  Operation Iron Curtain status: COMPLETE"
    echo -e ""
    echo -e "  Lieutenant, you have replaced General"
    echo -e "  Snowflake's hand-built infrastructure with"
    echo -e "  uniform, tested, automated compliance."
    echo -e ""
    echo -e "  RANK EARNED: LT. COMMANDER"
    echo -e "  BADGE: Iron Curtain — Master Operator"
    echo -e "  The Starfall Defence Corps salutes you."
    echo -e "  ==============================================${RESET}"
    echo ""
    echo -e "  ${YELLOW}${BOLD}Performance Tiers:${RESET}"
    echo -e "  ${DIM}  Under 2.5 hrs — Outstanding"
    echo -e "    2.5–3 hrs    — Excellent"
    echo -e "    3–3.5 hrs    — Qualified"
    echo -e "    3.5–4 hrs    — Passed"
    echo -e "    4+ hrs       — Return to AIT${RESET}"
else
    echo -e "  ${RED}${BOLD}=============================================="
    echo -e "  ARIA: Deficiencies detected."
    echo -e "  General Snowflake's infrastructure persists."
    echo -e "  Review the findings above and correct."
    echo -e "  Run 'make test' again when ready."
    echo -e "  ==============================================${RESET}"
fi

echo ""
exit $EXIT_CODE
