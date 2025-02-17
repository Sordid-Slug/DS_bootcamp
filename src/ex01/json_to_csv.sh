
#!/bin/sh

input_json="../ex00/hh.json"
filter_file="filter.jq"
output_file="hh.csv"

echo "\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"" > "$output_file"

jq -r -f "$filter_file" "$input_json" >> "$output_file"