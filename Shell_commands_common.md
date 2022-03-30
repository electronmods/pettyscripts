# Very common, very useful shell commands
## File manipulation
### Split huge text file into 1M records files, compressed
```sh
pigz -dc /data/100_million_records.csv.gz | \
  parallel --header : --pipe -N999999 'pigz -9c > 100_million_records_part_{#}.gz'
```
