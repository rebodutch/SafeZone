SERVICE_NAMES := DataIngestor CovidDataSimulator SafeZoneAnalyticsAPI SafeZoneDashboard
TOOL_NAMES := CLI TimeServer

# Tests do not cover the toolkit, so we need to test them manually
test-%:
	@if [ "$*" != "all" ]; then \
		echo "#######################################################"; \
		echo " Running tests for: $*"; \
		echo "#######################################################\n"; \
		bash scripts/$*/test.sh; \
		echo "\n[INFO] Build completed for: $*"; \
		echo "--------------------------------------------------------\n\n"; \
	fi

build-%:
	@if [ "$*" != "all" ]; then \
		echo "#######################################################"; \
		echo " Building service: $*"; \
		echo "#######################################################\n"; \
		bash scripts/$*/build.sh; \
		echo "\n[INFO] Tests completed for: $*"; \
		echo "--------------------------------------------------------\n\n"; \
	fi

build-tool-%:
	@if [ "$*" != "all" ]; then \
		echo "#######################################################"; \
		echo " Building tool: $*"; \
		echo "#######################################################\n"; \
		bash scripts/toolkit/$*/build.sh; \
		echo "\n[INFO] Build completed for tool: $*"; \
		echo "--------------------------------------------------------\n\n"; \
	fi

# Global commands
test-all: $(addprefix test-, $(SERVICE_NAMES))
	@echo "[INFO] ALL TESTS PASSED!"
	
build-all: $(addprefix build-, $(SERVICE_NAMES)) \
		   $(addprefix build-tool-, $(TOOL_NAMES))
	@echo "[INFO] ALL IMAGES BUILDED!"
 
local-ci: 
	act -W .github/workflows/dev/ci.yml 
	@echo "[INFO] LOCAL CI COMPLETED!"
	@tput cnorm

local-ci-compose: 
	act -W .github/workflows/dev/ci.yml -j compose 
	@echo "[INFO] LOCAL CI COMPLETED!"
	@tput cnorm

local-ci-down:
	COMPOSE_PROFILES=infra,core,init,ui docker compose \
					-f docker-compose/dev_compose.yml down
	@echo "[INFO] LOCAL CI DOWN COMPLETED!"
# Help
help:
	@echo "Available targets:"
	@echo "  local-ci             Run local CI tests"
	@echo "  test-<service>       Run tests for a specific service (e.g., test-CovidDataIngestor)"
	@echo "  build-<service>      Build a specific service (e.g., build-CovidDataIngestor)"
	@echo "  build-tool-<tool>    Build a specific tool"
	@echo "  test-all             Run tests for all services"
	@echo "  build-all            Build all services/tools"
	