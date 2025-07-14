package logger

import (
	"fmt"
	"os"

	"go.uber.org/zap"
)

// Init initializes the logger with the given service name, version, and environment.
func Init(serviceName, serviceVersion, env string) *zap.Logger {
	var err error
	var baseLogger *zap.Logger

	if env == "staging" || env == "prod" {
		baseLogger, err = zap.NewProduction()
	} else {
		baseLogger, err = zap.NewDevelopment()
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: Failed to load configuration: %v\n", err)
		os.Exit(1)
	}

	baseLogger = baseLogger.With(
		zap.String("service", serviceName),
		zap.String("service_version", serviceVersion),
	)
	return baseLogger
}
