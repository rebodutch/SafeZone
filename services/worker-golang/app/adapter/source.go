package adapter

import (
	"context"

	"safezone.service.worker-golang/app/schema"
)

type EventSource interface {
	GetEvent(ctx context.Context) (*schema.CovidEvent, error) // GetEvent retrieves the next event from the source, blocking until an event is available or context is canceled
	Close(ctx context.Context) error                          // Close the event source gracefully, releasing any resources
}
