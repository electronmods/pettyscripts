** Add commas to long integers
```sql
SELECT regexp_replace('3.25266E+11'::numeric::bigint::varchar, '(?![[:>:]]|[[:<:]])(?=(\d{3})+(?!\d))', ',', 'g')
```
