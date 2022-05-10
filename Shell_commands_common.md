# Very common, very useful shell commands
## Data inspection
### Sample random rows (1%) of input data
```sh
awk '{if (rand() <= 0.01) {print}}' < input.csv
```
### View headerless CSV quickly
First, estimate (or know) the number of fields (`n`). Echo `n-1` commas and output the CSV into `head` and `csvlook`.
```sh
( echo ,,,,,,,,, ; pigz -dc 'really_big_data.csv.gz')  | head -n2 | csvlook
```
## File manipulation
### `file` Determine a file's MIME type
```sh
file -b --mime-type foo.jpg
```
### `parallel` Split huge text file into 1M records files, compressed
```sh
pigz -dc /data/100_million_records.csv.gz | \
  parallel --header : --pipe -N1000000 'pigz -9c > 100_million_records_part_{#}.gz'
```
### `rsync` Copy files/folders
```sh
# don't forget the trailing slash on src
rsync -av src_dir/ target_dir
```
