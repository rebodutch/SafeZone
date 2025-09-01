package strategy

import (
	"context"
	"fmt"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/jmoiron/sqlx"
	"go.uber.org/zap"
	"safezone.service.worker-golang/app/pkg/cache"
	"safezone.service.worker-golang/app/pkg/logger"
	"safezone.service.worker-golang/app/schema"
)

type DBSink struct {
	DB     *sqlx.DB
	Logger *logger.ContextLogger
	cache  *cache.Cache
}

func NewDBSink(logger *logger.ContextLogger, db *sqlx.DB, cache *cache.Cache) *DBSink {
	return &DBSink{
		Logger: logger,
		DB:     db,
		cache:  cache,
	}
}

func (d *DBSink) Flush(ctx context.Context, batch []schema.CovidEvent) error {
	// Check if the context is done before proceeding
	tx, txErr := d.DB.BeginTxx(ctx, nil)
	if txErr != nil {
		d.Logger.Error(ctx, "Failed to begin transaction", zap.Error(txErr))
		return txErr
	}

	collisionCheck := make(map[string]bool)
	// keep track of valid events
	validEventCount := 0
	// building the SQL query for batch insert
	sql := "INSERT INTO covid_cases (date, city_id, region_id, cases) VALUES "
	args := make([]any, 0)
	for _, e := range batch {
		// the exist checking already done in validator, so we can safely assume city and region exist
		cityID := d.cache.GetCityID(e.Payload.City)
		regionID := d.cache.GetRegionID(cityID, e.Payload.Region)
		date := e.Payload.Date

		// check collision in batch buffer
		collisionKey := fmt.Sprintf("%s:%d:%d", date, cityID, regionID)
		if collisionCheck[collisionKey] {
			d.Logger.Warn(ctx, "Duplicate event found in batch",
				zap.String("date", date),
				zap.Int("city_id", cityID),
				zap.Int("region_id", regionID))
			continue
		}
		collisionCheck[collisionKey] = true

		if validEventCount > 0 {
			sql += ","
		}
		sql += fmt.Sprintf("($%d, $%d, $%d, $%d)", validEventCount*4+1, validEventCount*4+2, validEventCount*4+3, validEventCount*4+4)
		args = append(args, date, cityID, regionID, e.Payload.Cases)

		validEventCount++
	}
	sql += " ON CONFLICT (date, city_id, region_id) DO UPDATE SET cases=EXCLUDED.cases"

	d.Logger.Debug(ctx, "Executing batch insert", zap.String("sql", sql), zap.Any("args", args))

	// executing the batch insert
	_, execErr := tx.ExecContext(ctx, sql, args...)
	if execErr != nil {
		d.Logger.Error(ctx, "Failed to execute batch insert", zap.Error(execErr))
		tx.Rollback()
		return execErr
	}
	return tx.Commit()

}

func (d *DBSink) Close(ctx context.Context) error {
	if d.Logger != nil {
		d.Logger.Info(ctx, "DBSink closed")
	}
	return nil
}
