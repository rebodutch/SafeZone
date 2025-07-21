package schema

import (
	"fmt"
	"regexp"

	"go.uber.org/zap"
	"safezone.service.worker-golang/app/pkg/cache"
)

type CovidValidator struct {
	Logger      *zap.Logger
	datePattern *regexp.Regexp // YYYY-MM-DD 格式
	cache       *cache.Cache
}

func NewCovidValidator(logger *zap.Logger, cache *cache.Cache) *CovidValidator {
	return &CovidValidator{
		Logger:      logger,
		datePattern: regexp.MustCompile(`^\d{4}-\d{2}-\d{2}$`),
		cache:       cache,
	}
}

func DebugString(label, s string) {
	fmt.Printf("%s : [%s] HEX: [% x]\n", label, s, []byte(s))
}

func (v *CovidValidator) Validate(event CovidEvent) bool {
	// date is not in YYYY-MM-DD format
	if !v.datePattern.MatchString(event.Payload.Date) {
		v.Logger.Warn("Invalid date format", zap.String("date", event.Payload.Date), zap.String("trace_id", event.TraceID))
		return false
	}
	// city and region must exist in cache
	DebugString("EVENT_City", event.Payload.City)
	cityID := v.cache.GetCityID(event.Payload.City)
	regionID := v.cache.GetRegionID(cityID, event.Payload.Region)
	fmt.Println("City ID:", cityID, "Region ID:", regionID)
	if cityID < 0 || regionID < 0 {
		v.Logger.Warn("City or region not found in cache",
			zap.String("city", event.Payload.City),
			zap.String("region", event.Payload.Region),
			zap.String("trace_id", event.TraceID))
		return false
	}
	// cases must be a non-negative integer
	if event.Payload.Cases < 0 {
		v.Logger.Warn("Invalid cases count", zap.Int("cases", event.Payload.Cases),
			zap.String("trace_id", event.TraceID),
			zap.String("date", event.Payload.Date),
			zap.String("city", event.Payload.City),
			zap.String("region", event.Payload.Region))
		return false
	}
	return true
}
