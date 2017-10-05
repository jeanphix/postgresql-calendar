PostgreSQL calendar
-------------------

Generate a perpetual calendar from a PostgreSQL query:

```sql
select generate_series(
    date_trunc('week', date_trunc('month', now())),
    date_trunc(
        'week',
        date_trunc('month', now()) +
        '1 month'::interval -
        '2 day'::interval +
        '1 week'::interval
    ) - '1 day'::interval,
    '1 day'::interval
)::date;
```

[demo](https://tranquil-ridge-96726.herokuapp.com)
