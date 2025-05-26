SERVICE_NAMES := CovidDataIngestor CovidDataSimulator SafeZoneAnalyticsAPI SafeZoneDashboard
TOOL_NAMES := CLI TimeServer


# test doesnt coverage the toolkit, so we need to test them manually
test-%:
	@if [ "$*" != "all" ]; then \
		echo "#######################################################"; \
		echo " Running tests for: $*"; \
		echo "#######################################################\n"; \
		bash scripts/$*/test.sh; \
		echo "\n[INFO] Tests completed for: $*"; \
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
	@echo "[INFO] ALL IMAGE BUILT!"


# Help
help:
	@echo "Available targets:"
	@echo "  test-<service>       Run tests for a specific service"
	@echo "  build-<service>      Build a specific service"
	@echo "  build-tool-<tool>    Build a specific tool"
	@echo "  test-all             Run tests for all services"
	@echo "  build-all            Build all services/tools"
	