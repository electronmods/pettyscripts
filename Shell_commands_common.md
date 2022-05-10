# Very common, very useful shell commands

## Data inspection

### Sample random rows (1%) of input data
```sh
awk '{if (rand() <= 0.01) {print}}' < input.csv
```

### Skip first `n` rows of input data
For example, `n=3`:
```sh
tail -n+3 input.txt
```

### View headerless CSV quickly
First, estimate (or know) the number of fields (`n`). Echo `n-1` commas and output the CSV into `head` and `csvlook`.
```sh
( echo ,,,,,,,,, ; pigz -dc 'really_big_data.csv.gz')  | head -n2 | csvlook
```

## Data manipulation

### Strip accents and non-ascii's using `uconv`
```sh
uconv -c -i -f UTF8 -t ASCII -x '::NFD; [:Nonspacing mark:] >; [:^Ascii:] >; ::Upper; ::NFC;'
```

### View hex representation of data
```sh
od -ax weird_file.exe
hexdump -C weird_file.exe
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

## GNU Screen functions
|Sequence|Command|
|----|----|
|Ctrl-A, C|Create new screen|
|Ctrl-A, Ctrl-A|Return to previous screen|
|Ctrl-A, Ctrl-D|Detach and return to login shell|
|Ctrl-A, "|View list of screens and navigate|
|Ctrl-A, :|Access screen's command line|

## Shell shortcuts

### Move the `dirs` directory stack by 1
```sh
pushd +1
```

### Time a command's system/user time
```sh
/usr/bin/time -v long_running_command
```
