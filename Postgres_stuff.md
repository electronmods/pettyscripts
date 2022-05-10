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
WHERE table_name = 'phone_list'
	AND table_schema = 'distribution'
ORDER BY ordinal_position
```
## Load table from command line in parallel
```sh
ls data_tables_??.gz | parallel -j6 \
	"pigz -dc {} | psql -d homedata -h dataserver.lan -c \
		'COPY distribution.new_table
		 FROM STDIN WITH (FORMAT CSV, HEADER true)'"
```
