package service

import (
	"context"
	"errors"
	"time"

	"github.com/jmoiron/sqlx"
	"go.uber.org/zap"
	"safezone.service.worker-golang/app/adapter"
	"safezone.service.worker-golang/app/config"
	"safezone.service.worker-golang/app/pkg/cache"
	"safezone.service.worker-golang/app/pkg/logger"
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
	Logger    *logger.ContextLogger // logger for logging events
	ID        int                   // worker ID for logging and identification
}

func (w *Worker) Run(ctx context.Context) error {
	buffer := make([]schema.CovidEvent, 0, w.Config.BatchSize)
	lastFlush := time.Now()

	w.Logger.Info(ctx, "Starting worker", zap.String("event", "Worker started"))

	for {

		readCtx, cancel := context.WithTimeout(ctx, w.Config.FlushInterval)
		defer cancel()

		event, err := w.Source.GetEvent(readCtx)

		if err == nil {
			// if the event can't pass validation, skip it
			// future: we add the bad event to a dead-letter queue
			if w.Validator != nil && !w.Validator.Validate(ctx, *event) {
				w.Logger.Warn(ctx, "An event validation failed, skipping event",
					zap.String("event", "Event validation failed"))
				continue
			}
			// if the event is valid, add trace to the context for logging
			ctx = context.WithValue(ctx, "trace_id", event.TraceID)

			w.Logger.Info(ctx, "Received event from source",
				zap.String("event", "Event received"))

			buffer = append(buffer, *event)

		} else if errors.Is(err, context.DeadlineExceeded) {
			w.Logger.Info(ctx, "Event source read timeout, flushing buffer")

		} else if errors.Is(err, context.Canceled) {
			w.Logger.Info(ctx, "Event source context canceled, stopping worker")
			w.Source.Close(ctx)

			return nil
		} else {
			w.Logger.Error(ctx, "Failed to get event from source", zap.Error(err))
			w.Source.Close(ctx)

			return err
		}

		// two conditions to flush:
		// 1. buffer size reaches BatchSize
		// 2. the time since last flush exceeds FlushInterval
		if len(buffer) >= w.Config.BatchSize || (len(buffer) > 0 && time.Since(lastFlush) > w.Config.FlushInterval) {
			err = w.Sink.Flush(ctx, buffer)

			w.Logger.Info(ctx, "Worker flushing events",
				zap.Int("buffer_size", len(buffer)),
				zap.String("event", "Events flushed"))

			if errors.Is(err, context.Canceled) {
				w.Logger.Info(ctx, "Event sink context canceled, stopping worker")
				// flush the remaining events
				if len(buffer) > 0 {
					_ = w.Sink.Flush(ctx, buffer)
				}

				return nil
			} else if err != nil {
				w.Logger.Error(ctx, "Failed to flush events", zap.Error(err))

				return err
			}
			buffer = buffer[:0]
			lastFlush = time.Now()
		}
	}
}

func (w *Worker) Close(ctx context.Context) {

	if err := w.Source.Close(ctx); err != nil {
		w.Logger.Error(ctx, "Failed to close event source", zap.Error(err))
	}
	if err := w.Sink.Close(ctx); err != nil {
		w.Logger.Error(ctx, "Failed to close event sink", zap.Error(err))
	}
	if w.DB != nil {
		if err := w.DB.Close(); err != nil {
			w.Logger.Error(ctx, "Failed to close database connection", zap.Error(err))
		}
	}
	w.Logger.Info(ctx, "Closing worker", zap.String("event", "Worker closed"))

}
