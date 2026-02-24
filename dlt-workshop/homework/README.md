## Solution to the DLT Homework Questions


### Question 1
What is the start date and end date of the dataset?

```sql
select
    min(cast(trip_pickup_date_time as date)) as start_date,
    max(cast(trip_pickup_date_time as date)) as end_date
from "home-work".taxi_raw_data.taxi_records
```

Result:
```
start_date  | end_date
------------+----------
2009-06-01  | 2009-07-01
```

### Question 2
What proportion of trips are paid with credit card?

```sql
with pay_type as (
select 
  payment_type,
  count(*) as total
from "home-work".taxi_raw_data.taxi_records
group by 1
),
all_pay as (
select
  count(*) as total
from "home-work".taxi_raw_data.taxi_records
)
select
  p.payment_type,
  (p.total * 100)/a.total as percent
from pay_type p, all_pay a

```
### Optimised query

```sql
SELECT
    payment_type,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percent
FROM "home-work".taxi_raw_data.taxi_records
GROUP BY payment_type;
```

Result:
```
total_trips
--------------|--------
payment_type	percent
--------------|--------
Credit	        26.66
--------------|-------              
Cash	        0.97
--------------|-------
Dispute	        0.01
--------------|-------
No Charge	    0.01
--------------|-------
CASH	        72.35
--------------|--------

```

### Question 3
What is the total amount of money generated in tips?

```sql
SELECT
    sum(tip_amt) as total_tip_amount
FROM "home-work".taxi_raw_data.taxi_records
```

Result:
```
total_tip_amount
------------------
6063.410000000009
```

### Question 4


