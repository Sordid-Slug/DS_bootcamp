
#!/bin/sh

input_json="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex00/hh.json"
filter_file="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex01/filter.jq"
output_file="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex01/hh.csv"

echo "\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"" > "$output_file"

jq -r -f "$filter_file" "$input_json" >> "$output_file"