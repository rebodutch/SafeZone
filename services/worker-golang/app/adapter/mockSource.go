package adapter

import (
	"context"
	"fmt"

	"time"

	"go.uber.org/zap"
	"safezone.service.worker-golang/app/pkg/logger"
	"safezone.service.worker-golang/app/schema"
)

// MockSource is a mock implementation of EventSource for testing purposes.
type MockSource struct {
	Count  int
	Curr   int
	Logger *logger.ContextLogger
}

func (m *MockSource) GetEvent(ctx context.Context) (*schema.CovidEvent, error) {
	if m.Curr < m.Count {
		time.Sleep(100 * time.Millisecond) // simulate some processing delay

		m.Logger.Debug(ctx, "Generating mock event",
			zap.Int("current_event_index", m.Curr),
			zap.Int("total_events", m.Count))

		// create a mock event
		event := &schema.CovidEvent{
			EventType: "mock_event",
			EventTime: time.Now().Unix(),
			TraceID:   fmt.Sprintf("mock_trace_%d", m.Curr),
			Version:   "0.1.0",
		}
		event.Payload.Date = fmt.Sprintf("2023-10-%02d", m.Curr+1)
		event.Payload.City = "MockCity"
		event.Payload.Region = "MockRegion"
		event.Payload.Cases = 100 + m.Curr
		m.Curr++
		return event, nil
	}
	// simulate a blocking call
	for {
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-time.After(3 * time.Second):

		}

	}
}

func (m *MockSource) Close(ctx context.Context) error {
	m.Logger.Info(ctx, "Closing mock event source",
		zap.Int("total_events_generated", m.Curr))
	return nil
}
