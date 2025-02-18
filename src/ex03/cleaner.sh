
#!/bin/sh

input_json="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex00/hh.json"
output_file="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex03/hh_positions.csv"
json_filters='.items[] | [.id, .created_at, .name, .has_test, .alternate_url] | @csv'

result=$(jq -r "$json_filters" "$input_json" | gawk 'BEGIN {
    FPAT = "([^,]+)|(\"[^\"]+\")"
    OFS = ","

}
{
    match($3, /(Junior|Middle|Senior)/, level);
    $3 = level[1] ? sprintf("\"%s\"", level[1]) : "-";
    print
}')

echo "\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"" > "$output_file"
echo "$result" | sort -t ',' -k2,2 -k1,1n >> "$output_file"