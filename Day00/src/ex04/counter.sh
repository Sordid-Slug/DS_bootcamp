
#!/bin/sh

input_csv="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex03/hh_positions.csv"
output_file="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex04/hh_uniq_positions.csv"

header="\"name\", \"count\""
echo "$header" > "$output_file"

tail -n +2 "$input_csv" | cut -d',' -f3 | sort | uniq -c | sort -nr | awk 'BEGIN {OFS=","} {print $2, $1}' >> "$output_file"