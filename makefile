SERVICE_NAMES := CovidDataIngestor CovidDataSimulator SafeZoneAnalyticsAPI SafeZoneDashboard


# Per-service commands
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
		echo " Running tests for: $*"; \
		echo "#######################################################\n"; \
		bash scripts/$*/build.sh; \
		echo "\n[INFO] Tests completed for: $*"; \
		echo "--------------------------------------------------------\n\n"; \
	fi

manual-test-ui:
	bash scripts/SafeZoneDashboard/manual-test.sh

# Global commands
test-all: $(addprefix test-, $(SERVICE_NAMES))
	@echo "[INFO] ALL TESTS PASSED!"
	
build-all: $(addprefix build-, $(SERVICE_NAMES))
	@echo "[INFO] ALL IMAGE BUILT!"

clean:
	rm -rf build/ dist/ *.log

format:
	black services/*/

ci-test:
	make test-all ENV=test

ci-build:
	make build-all ENV=prod

# Help
help:
	@echo "Available targets:"
	@echo "  test-<service>       Run tests for a specific service"
	@echo "  build-<service>      Build a specific service"
	@echo "  docker-build-<service> Build Docker image for a specific service"
	@echo "  test-all             Run tests for all services"
	@echo "  build-all            Build all services"
	@echo "  clean                Remove temporary files"
	@echo "  format               Format codebase"
