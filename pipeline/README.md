HW 1.

Question 1.

```bash
docker run -it --entrypoint=bash python 3.13 
pip --version
```

Question 2.

pgadmin can connect to postgres database in two different ways:
a) Connect postgres thru the network, by using hostname as postgres services name db and the port of postgres container itself. (db:5432)
b) Connect postgres thru the host machine, by using hostname as localhost and the mapping port 5433. (localhost:5433)

Question 3.

```bash
select count(1)
from green_taxi_data
where lpep_pickup_datetime::date >= '2025-11-01'
and lpep_pickup_datetime::date < '2025-12-01'
and trip_distance <= 1
```

Question 4.
```bash
SELECT
	cast(lpep_pickup_datetime as date) as pu_date,
	trip_distance
FROM public.green_taxi_data
where trip_distance <= 100
order by trip_distance desc
limit 10
```

Question 5.
```bash
select
  cast(gt.lpep_pickup_datetime as date) as "pu_day",
  zpu."Zone" AS "pickup_loc",
  sum(gt.total_amount) as total_amount_sum
from public.green_taxi_data gt
join public.zone_data zpu
on gt."PULocationID" = zpu."LocationID"
where gt.lpep_pickup_datetime::date = '2025-11-18'
group by 1,2
order by 3 desc
```

Question 6.
```bash
select
  cast(gt.lpep_pickup_datetime as date) as "pu_day",
  cast(gt.lpep_dropoff_datetime as date) as "df_day",
  zpu."Zone" AS "pickup_loc",
  zdf."Zone" AS "dropoff_loc",
  (gt.tip_amount) as tip_amount
from public.green_taxi_data gt
join public.zone_data zpu on gt."PULocationID" = zpu."LocationID"
join public.zone_data zdf on gt."PULocationID" = zdf."LocationID"
where gt.lpep_pickup_datetime::date >= '2025-11-01'
and gt.lpep_pickup_datetime::date < '2025-12-01'
and zpu."Zone" = 'East Harlem North'
order by 5 desc
```

HW 3.
Question 1.
```bash
-- create a external yellow taxi 2024 table
CREATE OR REPLACE EXTERNAL TABLE `terraform-setup-485500.zoomcamp_dataset.external_yellow_taxi_2024_tbl`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://terraform-setup-485500-data-bucket/yellow_tripdata_2024-*.parquet']
);

-- create a materialized yellow taxi 2024 table from external table
CREATE OR REPLACE TABLE terraform-setup-485500.zoomcamp_dataset.yellow_tripdata__non_partitioned
AS
SELECT * FROM terraform-setup-485500.zoomcamp_dataset.external_yellow_taxi_2024_tbl;
```

Number of rows in yellow_tripdata__non_partitioned metadata is 20,332,093.

Question 2.
The estimated amount of data that will be read when this query is executed on the External Table is 0B, and materialized table is 155.12 MB.

Question 3.
```bash
-- Materialized table scan 155.12MB data
SELECT distinct(PULocationID)
FROM terraform-setup-485500.zoomcamp_dataset.yellow_tripdata__non_partitioned

-- Materialized table scan 310.24MB data
SELECT distinct(PULocationID, DOLocationID)
FROM terraform-setup-485500.zoomcamp_dataset.yellow_tripdata__non_partitioned
```

Question 4.
```bash
SELECT count(*)
FROM terraform-setup-485500.zoomcamp_dataset.yellow_tripdata__non_partitioned
WHERE fare_amount=0
```

Question 5. Partition by tpep_dropoff_datetime and Cluster on VendorID

Question 6. 
```bash
-- create a partitioned yellow taxi 2024 table from external table
CREATE OR REPLACE TABLE terraform-setup-485500.zoomcamp_dataset.yellow_tripdata_partitioned
PARTITION BY
  DATE(tpep_dropoff_datetime)
CLUSTER BY 
  VendorID
AS
SELECT * FROM terraform-setup-485500.zoomcamp_dataset.external_yellow_taxi_2024_tbl;

SELECT distinct(VendorID) From `zoomcamp_dataset.yellow_tripdata_partitioned`
WHERE DATE(tpep_dropoff_datetime)>="2024-03-01" and DATE(tpep_dropoff_datetime)<="2024-03-15"

SELECT distinct(VendorID) From terraform-setup-485500.zoomcamp_dataset.yellow_tripdata__non_partitioned
WHERE DATE(tpep_dropoff_datetime)>="2024-03-01" and DATE(tpep_dropoff_datetime)<="2024-03-15"
```

Question 7. The data stored in the External Table stored in the bucket, bigquery only store metadata of the External Table and location.

Question 8. Small table or filter condition change often, cluster does not help.