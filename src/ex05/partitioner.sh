
#!/bin/sh

input_csv="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex03/hh_positions.csv"
output_dir="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex05/partitions"

mkdir -p "$output_dir"

tail -n +2 "$input_csv" | gawk '
BEGIN {
    header="\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\""
    FPAT = "([^,]+)|(\"[^\"]+\")"
    OFS = ","
}
{
    created_at = $2
    
    date = substr(created_at, 2, 10)

    output_file = "'"$output_dir"/'" date ".csv"

    if (!(date in files)) {
        print header > output_file
        files[date] = 1
    }
    print >> output_file
}
'