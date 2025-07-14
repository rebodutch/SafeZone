package strategy

import (
	"context"

	"go.uber.org/zap"
	"safezone.service.worker-golang/app/schema"
)

type MockSink struct {
	Logger *zap.Logger
}

func (m *MockSink) Flush(ctx context.Context, batch []schema.CovidEvent) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	default:
		for _, evt := range batch {
			m.Logger.Debug("Flushing event",
				zap.String("event_type", evt.EventType),
				zap.String("trace_id", evt.TraceID),
				zap.String("date", evt.Payload.Date),
				zap.String("city", evt.Payload.City),
				zap.String("region", evt.Payload.Region),
				zap.Int("cases", evt.Payload.Cases))
		}
		return nil
	}
}

func (m *MockSink) Close() error {
	m.Logger.Info("MockSink closed")
	return nil
}
