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

	// building the SQL query for batch insert
	sql := "INSERT INTO covid_cases (date, city_id, region_id, cases) VALUES "
	args := make([]any, 0)
	for i, e := range batch {
		if i > 0 {
			sql += ","
		}
		// the exist checking already done in validator, so we can safely assume city and region exist
		cityID := d.cache.GetCityID(e.Payload.City)
		regionID := d.cache.GetRegionID(cityID, e.Payload.Region)

		sql += fmt.Sprintf("($%d, $%d, $%d, $%d)", i*4+1, i*4+2, i*4+3, i*4+4)
		args = append(args, e.Payload.Date, cityID, regionID, e.Payload.Cases)
	}
	sql += " ON CONFLICT (date, city_id, region_id) DO UPDATE SET cases=EXCLUDED.cases"

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
