package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"

	"safezone.service.worker-golang/app/config"
	"safezone.service.worker-golang/app/pkg/logger"
	"safezone.service.worker-golang/app/service"
)

func main() {
	cfx, err := config.Load()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: Failed to load configuration: %v\n", err)
		os.Exit(1)
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	logger := logger.NewContextLogger(cfx.ServiceName, cfx.ServiceVersion, cfx.Environment)

	logger.Info(ctx, "Worker-golang service started")

	workers := make([]*service.Worker, 0, cfx.WorkerCount)

	factory := &service.WorkerFactory{Logger: logger, Config: cfx}
	for i := 0; i < cfx.WorkerCount; i++ {
		workers = append(workers, factory.CreateWorker(i))
	}

	orchestrator := &service.Orchestrator{
		Workers: workers,
	}
	orchestrator.RunParallel(ctx, cfx.ParallelN)

	logger.Info(ctx, "Worker-golang service completed")
}
