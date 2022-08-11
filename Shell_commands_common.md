# Very common, very useful shell commands

## Data inspection

### `awk`: Sample random rows (~1%) of input data
```sh
awk 'BEGIN {srand()}; rand() <= 0.01' < input.csv
```

### `csvlook`: View headerless CSV quickly
First, estimate (or know) the number of fields (`n`). Echo `n-1` commas and output the CSV into `head` and `csvlook`.
```sh
( echo ,,,,,,,,, ; pigz -dc 'really_big_data.csv.gz')  | head -n2 | csvlook
```

### `tail`: Skip first `n` rows of input data
For example, `n=3` to begin output at line 3:
```sh
tail -n+3 input.txt
```

## Data manipulation

### `uconv`: Strip accents and non-ascii's using `uconv`
```sh
uconv -c -i -f UTF8 -t ASCII -x '::NFD; [:Nonspacing mark:] >; [:^Ascii:] >; ::Upper; ::NFC;'
```

### View hex representation of data
```sh
od -ax weird_file.exe
hexdump -C weird_file.exe
```

## File manipulation

### `file`: Determine a file's MIME type
```sh
file -b --mime-type foo.jpg
```

### `parallel`: Split huge text file into 1M records files, compressed
```sh
pigz -dc /data/100_million_records.csv.gz | \
  parallel --header : --rpl '{0#} 1 $_=sprintf("%02d",$job->seq())' --pipe -N1000000 'pigz -9c > 100_million_records_part_{0#}.gz'
```

### `rsync`: Copy files/folders
```sh
# don't forget the trailing slash on src
rsync -av src_dir/ target_dir
```

### `xargs`: Rename series of files to add dates
```sh
# Remove the final xargs's echo statement to commit the actual mv
DATE=$(date +%Y%m%d)
ls *.gz | \
    xargs -I{} bash -c 'echo "{}" ; echo "{}" | sed s/B2BP/B2BP_$(date +%Y%m%d)/g' | \
    xargs -d"\n" -n2 mv -v
```
### `xargs`: Use more than one input variable as an argument
```sh
ls *.gz | xargs -d "\n" -n2 bash -c 'echo yep $0 should be $1'
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

### `dirs`: Move the directory stack by 1
```sh
pushd +1
```

### `env`: Environment variables: print and sort
```sh
env -0 | sort -z | tr '\0' '\n'
```
### `find`: List broken symlinks
```sh
find . -type l -exec test ! -e {} \; -print
```

### `find`: List packages imported in Python scripts
```sh
find . -name '*.py' | xargs -n1 grep -E -e '^(import|from)' | awk '{print $2}' | sort  | uniq > ~/python_packages.txt
```

### `time`: Time a command's system/user time
```sh
/usr/bin/time -v long_running_command
```
