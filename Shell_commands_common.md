# Very common, very useful shell commands
## File manipulation
### `parallel` Split huge text file into 1M records files, compressed
```sh
pigz -dc /data/100_million_records.csv.gz | \
  parallel --header : --pipe -N999999 'pigz -9c > 100_million_records_part_{#}.gz'
```
### `rsync` to copy files/folders
```sh
# don't forget the trailing slash on src
rsync -av src_dir/ target_dir
```
