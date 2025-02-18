
#!/bin/sh

input_json="../ex00/hh.json"
output_file="hh_positions.csv"
json_filters='.items[] | [.id, .created_at, .name, .has_test, .alternate_url] | @csv'

jq -r "$json_filters" "$input_json" | gawk 'BEGIN {   
    FPAT = "([^,]+)|(\"[^\"]+\")"
    OFS=","
}
{
    match($3, /(Junior|Middle|Senior)/, level);
    $3 = level[1] ? sprintf("\"%s\"", level[1]) : "-";
    print
}' > "$output_file"