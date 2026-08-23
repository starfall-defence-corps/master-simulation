.PHONY: doctor submit help setup test incident reset destroy ssh-web-1 ssh-web-2 ssh-db-1 ssh-db-2 ssh-app ssh-comms
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

help: ## Show available commands
	@echo ""
	@echo "  STARFALL DEFENCE CORPS — Master Simulation"
	@echo "  Operation: Iron Curtain"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

doctor: ## Check your machine is mission-ready (Docker, ports, tools)
	@bash $(ROOT_DIR)/scripts/doctor.sh

setup: ## Launch Iron Curtain fleet (6 nodes)
	@bash scripts/setup-lab.sh

test: ## Run ARIA assessment verification
	@bash scripts/check-work.sh

incident: ## Trigger the surprise incident (Mission 4)
	@bash scripts/trigger-incident.sh

submit: ## Submit your work for ARIA review (branch, commit, push, PR)
	@bash $(ROOT_DIR)/scripts/submit.sh

reset: ## Destroy and rebuild all nodes
	@bash scripts/reset-lab.sh

destroy: ## Tear down everything (containers, keys, venv)
	@bash scripts/destroy-lab.sh

ssh-web-1: ## SSH into sdc-iron-web-1 (Ubuntu, port 2281)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2281

ssh-web-2: ## SSH into sdc-iron-web-2 (Ubuntu, port 2282)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2282

ssh-db-1: ## SSH into sdc-iron-db-1 (Rocky Linux, port 2283)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2283

ssh-db-2: ## SSH into sdc-iron-db-2 (Rocky Linux, port 2284)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2284

ssh-app: ## SSH into sdc-iron-app (Ubuntu, port 2285)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2285

ssh-comms: ## SSH into sdc-iron-comms (Ubuntu, port 2286)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2286
