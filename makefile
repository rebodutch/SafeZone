SERVICE_NAMES := CovidDataIngestor CovidDataSimulator SafeZoneAnalyticsAPI SafeZoneDashboard
ENV ?= dev

# Per-service commands
test-%:
	bash scripts/$*/test.sh

build-%:
	bash scripts/$*/build.sh

# Global commands
test-all: $(addprefix test-, $(SERVICE_NAMES))
build-all: $(addprefix build-, $(SERVICE_NAMES))

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
