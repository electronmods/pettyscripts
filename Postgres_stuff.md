# PostgreSQL Useful Snippets
## Add commas to long integers
```sql
SELECT regexp_replace('3.25266E+11'::numeric::bigint::varchar, '(?![[:>:]]|[[:<:]])(?=(\d{3})+(?!\d))', ',', 'g')
```

## Get list of columns from table
```sql
SELECT
	column_name,
	ordinal_position,
	data_type
FROM information_schema.columns
WHERE table_name = 'company'
	AND table_schema = 'b2b'
ORDER BY ordinal_position
```
