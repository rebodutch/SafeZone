
#!/bin/bash
set -e

echo "Seeding SafeZone default data..."

#--- time management ---
# szcli system time set --mock=false --acceleration=1

# # 2. Retrieve system time status.
# # Output example:
# #   mock = true
# #   current_date = 2023-03-23    # if mock = true, it's the mock date
# #   accelerate = 2
# # We need to parse these values to determine simulation base date.
# TIME_STATUS=$(szcli system time status)

# # 3. Extract the "mock" flag and current date.
# MOCK=$(echo "$TIME_STATUS" | grep mock | cut -d'=' -f2 | xargs)
# CURRENT_DATE=$(echo "$TIME_STATUS" | grep current_date | cut -d'=' -f2 | xargs)

# # 4. Decide simulation base:
# if [ "$MOCK" = "true" ]; then
#   echo "Simulating based on mock date: $CURRENT_DATE"
# else
#   echo "Simulating based on current date: $CURRENT_DATE"
# fi

# # 5. Calculate simulation interval:
# #   - START_DATE = CURRENT_DATE
# #   - END_DATE = START_DATE minus 33 days
# #   - Dashboard requires at least 30 days, so we set 33 days for safety.
# START_DATE="$CURRENT_DATE"
# END_DATE=$(date -d "$START_DATE - 33 days" +%Y-%m-%d)

# echo "Simulation range: $START_DATE ~ $END_DATE"

START_DATE=2023-03-23
END_DATE=$(date -d "$START_DATE + 33 days" +%Y-%m-%d)
# 6. Run the dataflow simulation for the computed interval.
szcli dataflow simulate "$START_DATE" --enddate="$END_DATE"


echo "Seeding default data completed."