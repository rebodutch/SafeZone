package service

import (
	"context"
	"time"

	"github.com/jmoiron/sqlx"
	"go.uber.org/zap"
	"safezone.service.worker-golang/app/adapter"
	"safezone.service.worker-golang/app/config"
	"safezone.service.worker-golang/app/pkg/cache"
	"safezone.service.worker-golang/app/schema"
	"safezone.service.worker-golang/app/strategy"
)

type Worker struct {
	DB        *sqlx.DB               // database connection, if needed
	Cache     *cache.Cache           // cache for city and region mappings
	Validator *schema.CovidValidator // validator for events
	Source    adapter.EventSource
	Sink      strategy.EventSink
	Config    *config.Config
	Logger    *zap.Logger
	ID        int // worker ID for logging and identification
}

func (w *Worker) Run(ctx context.Context) error {
	buffer := make([]schema.CovidEvent, 0, w.Config.BatchSize)

	lastFlush := time.Now()

	for {
		idleCtx, cancel := context.WithTimeout(ctx, w.Config.IdleTimeout)

		event, err := w.Source.GetEvent(idleCtx)

		if err == context.Canceled {
			w.Logger.Info("Event source context canceled, stopping worker",
				zap.Int("worker_id", w.ID))
			w.Source.Close()
			cancel()
			return nil
		} else if err == context.DeadlineExceeded {
			w.Logger.Info("Event source context deadline exceeded, stopping worker",
				zap.Int("worker_id", w.ID))
			w.Source.Close()
			cancel()
			return nil
		} else if err != nil {
			w.Logger.Error("Failed to get event from source", zap.Error(err),
				zap.Int("worker_id", w.ID))
			w.Source.Close()
			cancel()
			return err
		}

		// if the event can't pass validation, skip it
		// future: we add the bad event to a dead-letter queue
		if w.Validator != nil && !w.Validator.Validate(*event) {
			continue
		}

		buffer = append(buffer, *event)
		// two conditions to flush:
		// 1. buffer size reaches BatchSize
		// 2. the time since last flush exceeds FlushInterval
		if len(buffer) >= w.Config.BatchSize || time.Since(lastFlush) > w.Config.FlushInterval {
			err = w.Sink.Flush(idleCtx, buffer)

			w.Logger.Debug("Worker flushing events",
				zap.Int("worker_id", w.ID),
				zap.Int("buffer_size", len(buffer)),
				zap.String("trace_id", buffer[0].TraceID),
				zap.String("hint", "The trace_id is the first event in the batch"))

			if err == context.Canceled {
				w.Logger.Info("Event sink context canceled, stopping worker",
					zap.Int("worker_id", w.ID))
				// flush the remaining events
				if len(buffer) > 0 {
					_ = w.Sink.Flush(ctx, buffer)
				}
				cancel()
				return nil
			} else if err == context.DeadlineExceeded {
				w.Logger.Info("Event sink context deadline exceeded, stopping worker",
					zap.Int("worker_id", w.ID))
				// flush the remaining events
				if len(buffer) > 0 {
					_ = w.Sink.Flush(ctx, buffer)
				}
				cancel()
				return nil
			} else if err != nil {
				w.Logger.Error("Failed to flush events", zap.Error(err),
					zap.Int("worker_id", w.ID))
				cancel()
				return err
			}
			buffer = buffer[:0]
			lastFlush = time.Now()
		}
	}
}

func (w *Worker) Close() {
	if err := w.Source.Close(); err != nil {
		w.Logger.Error("Failed to close event source", zap.Error(err),
			zap.Int("worker_id", w.ID))
	}
	if err := w.Sink.Close(); err != nil {
		w.Logger.Error("Failed to close event sink", zap.Error(err),
			zap.Int("worker_id", w.ID))
	}
	if w.DB != nil {
		if err := w.DB.Close(); err != nil {
			w.Logger.Error("Failed to close database connection", zap.Error(err),
				zap.Int("worker_id", w.ID))
		}
	}
	w.Logger.Info("Closing worker", zap.Int("worker_id", w.ID))
}
