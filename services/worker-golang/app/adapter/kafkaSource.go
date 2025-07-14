package adapter

import (
	"context"
	"encoding/json"
	"strings"

	"github.com/segmentio/kafka-go"
	"go.uber.org/zap"
	"safezone.service.worker-golang/app/schema"
)

type KafkaSource struct {
	Logger *zap.Logger
	Reader *kafka.Reader
}

func NewKafkaSource(logger *zap.Logger, brokers string, groupID string, topic string) *KafkaSource {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers: strings.Split(brokers, ","),
		GroupID: groupID,
		Topic:   topic,
	})

	return &KafkaSource{
		Logger: logger,
		Reader: reader,
	}
}

func (k *KafkaSource) GetEvent(ctx context.Context) (*schema.CovidEvent, error) {
	msg, err := k.Reader.ReadMessage(ctx)

	if err != nil {
		return nil, err
	}

	var event schema.CovidEvent

	if err = json.Unmarshal(msg.Value, &event); err != nil {
		k.Logger.Warn("json unmarshal failed", zap.Error(err))
		return nil, err
	}
	return &event, nil
}

func (k *KafkaSource) Close() error {
	if err := k.Reader.Close(); err != nil {
		k.Logger.Error("Failed to close Kafka reader", zap.Error(err))
		return err
	}
	k.Logger.Info("Kafka reader closed successfully")
	return nil
}
