--question: For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), 
--how many trips had a trip_distance of less than or equal to 1 mile?

SELECT COUNT(*) AS trip_count
FROM green_taxi_data
WHERE "lpep_pickup_datetime" >= '2025-11-01'
  AND "lpep_pickup_datetime" < '2025-12-01'
  AND "trip_distance" <= 1;

--question : Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles

SELECT 
    DATE("lpep_pickup_datetime") AS pickup_day,
    MAX("trip_distance") AS max_trip_distance
FROM green_taxi_data
WHERE "trip_distance" < 100
GROUP BY DATE("lpep_pickup_datetime")
ORDER BY max_trip_distance DESC

--question : Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

SELECT 
    tz."Zone" AS pickup_zone,
    tz."Borough" AS borough,
    SUM(t."total_amount") AS total_amount_sum
FROM green_taxi_data t
INNER JOIN taxi_zone_data tz ON t."PULocationID" = tz."LocationID"
WHERE DATE(t."lpep_pickup_datetime") = '2025-11-18'
GROUP BY tz."Zone", tz."Borough", tz."LocationID"
ORDER BY total_amount_sum DESC

--question : For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

SELECT 
    dz."Zone" AS dropoff_zone,
    dz."Borough" AS dropoff_borough,
    MAX(t."tip_amount") AS largest_tip
FROM green_taxi_data t
INNER JOIN taxi_zone_data dz ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND t."lpep_pickup_datetime" >= '2025-11-01'
  AND t."lpep_pickup_datetime" < '2025-12-01'
GROUP BY dz."Zone", dz."Borough", dz."LocationID"
ORDER BY largest_tip DESC
