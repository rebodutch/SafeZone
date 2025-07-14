package service

import (
	"go.uber.org/zap"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/jmoiron/sqlx"
	"safezone.service.worker-golang/app/adapter"
	"safezone.service.worker-golang/app/config"
	"safezone.service.worker-golang/app/pkg/cache"
	"safezone.service.worker-golang/app/schema"
	"safezone.service.worker-golang/app/strategy"
)

type WorkerFactory struct {
	Logger *zap.Logger
	Config *config.Config
}

func (f *WorkerFactory) CreateWorker(id int) *Worker {
	var db *sqlx.DB
	var cache *cache.Cache
	var src adapter.EventSource
	var validator *schema.CovidValidator
	var sink strategy.EventSink

	switch f.Config.Environment {
	case "TEST":
		src = &adapter.MockSource{Count: 10, Logger: f.Logger}
		sink = &strategy.MockSink{Logger: f.Logger}
	default:
		db = sqlx.MustConnect("pgx", f.Config.DBUrl)
		cache = cache.NewCache(db)
		src = adapter.NewKafkaSource(f.Logger, f.Config.KafkaBroker, f.Config.KafkaGroupID, f.Config.KafkaTopic)
		validator = schema.NewCovidValidator(f.Logger, cache)
		sink = strategy.NewDBSink(f.Logger, db, cache)
	}

	return &Worker{
		DB:        db,
		Cache:     cache,
		Source:    src,
		Validator: validator,
		Sink:      sink,
		Config:    f.Config,
		Logger:    f.Logger,
		ID:        id,
	}
}
