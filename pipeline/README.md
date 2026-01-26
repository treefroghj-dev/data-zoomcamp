Question 1.

```bash
docker run -it --entrypoint=bash python 3.13 pip --version
```

Question 2.

pgadmin can connect to postgres database in two different ways:
a) Connect postgres thru the network, by using hostname as postgres services name db and the port of postgres container itself. (db:5432)
b) Connect postgres thru the host machine, by using hostname as localhost and the mapping port 5433. (localhost:5433)

Question 3.

```bash
select count(1)
from green_taxi_data
where lpep_pickup_datetime::data >= "2025-11-01"
and lpep_pickup_datetime::data < "2025-12-01"
and trip_distance <= 1
```

Question 4.
```bash

```

Question 5.
```bash

```

Question 6.
```bash
select
  cast(gt.lpep_pickup_datetime as date) as "pu_day",
  cast(gt.lpep_dropoff_datetime as date) as "df_day",
  zpu."Zone" AS "pickup_loc",
  zdf."Zone" AS "dropoff_loc",
  gt.tip_amount
from public.green_taxi_data gt
join public.zone_data zpu on gt."PULocationID" = zpu."LocationID"
join public.zone_data zdf on gt."PULocationID" = zdf."LocationID"
where gt.lpep_pickup_datetime::date >= '2025-11-01'
and gt.lpep_pickup_datetime::date < '2025-12-01'
and zpu."Zone" = 'East Harlem North'
group by 1,2,3,4
order by 5 desc
```
