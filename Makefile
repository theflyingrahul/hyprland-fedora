PYTHON ?= python3
TOOL := $(PYTHON) tooling/hyprwm-packaging
MOCK_CONFIG ?= mock/fedora-44-x86_64.cfg
PACKAGE ?=
REPO_DIR ?= .work/repository

.PHONY: validate test-tooling check-docs fetch srpm build build-set resume-set repo audit snapshot activate activate-unsigned rollback bundle check-updates clean

validate:
	$(TOOL) validate

test-tooling:
	$(PYTHON) -m unittest tooling/test_hyprwm_packaging.py

check-docs:
	$(PYTHON) tooling/check-doc-links.py

fetch:
	@test -n "$(PACKAGE)" || { echo "PACKAGE is required" >&2; exit 2; }
	$(TOOL) fetch "$(PACKAGE)"

srpm:
	@test -n "$(PACKAGE)" || { echo "PACKAGE is required" >&2; exit 2; }
	$(TOOL) srpm "$(PACKAGE)" --mock-config "$(MOCK_CONFIG)"

build:
	@test -n "$(PACKAGE)" || { echo "PACKAGE is required" >&2; exit 2; }
	$(TOOL) build "$(PACKAGE)" --mock-config "$(MOCK_CONFIG)" --repo "$(REPO_DIR)"

build-set:
	$(TOOL) build-set --mock-config "$(MOCK_CONFIG)" --repo "$(REPO_DIR)"

resume-set:
	$(TOOL) build-set --resume --mock-config "$(MOCK_CONFIG)" --repo "$(REPO_DIR)"

repo:
	$(TOOL) repo --input results --output "$(REPO_DIR)"

audit:
	$(TOOL) audit --config-name "$(notdir $(basename $(MOCK_CONFIG)))"

snapshot:
	$(TOOL) snapshot --input results --output repo/public

activate:
	@test -n "$(PUBLIC_KEY)" || { echo "PUBLIC_KEY is required" >&2; exit 2; }
	$(TOOL) activate --output repo/public --public-key "$(PUBLIC_KEY)"

activate-unsigned:
	$(TOOL) activate --output repo/public --allow-unsigned

rollback:
	@test -n "$(REVISION)" || { echo "REVISION is required" >&2; exit 2; }
	@test -n "$(PUBLIC_KEY)" || { echo "PUBLIC_KEY is required" >&2; exit 2; }
	$(TOOL) rollback --output repo/public --revision "$(REVISION)" --public-key "$(PUBLIC_KEY)"

bundle:
	$(TOOL) bundle

check-updates:
	$(TOOL) check-updates

clean:
	rm -rf .work results
