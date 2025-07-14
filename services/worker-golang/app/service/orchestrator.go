package service

import (
	"context"
	"sync"

	"go.uber.org/zap"
)

type Orchestrator struct {
	Logger  *zap.Logger
	Workers []*Worker
}

func (o *Orchestrator) Run(ctx context.Context) error {
	return o.RunParallel(ctx, 1)
}

func (o *Orchestrator) RunParallel(ctx context.Context, parallelN int) error {
	sem := make(chan struct{}, parallelN)
	var wg sync.WaitGroup

	for _, w := range o.Workers {
		wg.Add(1)
		sem <- struct{}{}
		go func(worker *Worker) {
			defer wg.Done()
			defer func() { <-sem }()
			err := worker.Run(ctx)
			if err != nil {
				o.Logger.Error("Worker run failed", zap.Error(err), zap.Int("worker_id", worker.ID))
				return
			}
			worker.Close()
		}(w)
	}
	wg.Wait()
	return nil
}
