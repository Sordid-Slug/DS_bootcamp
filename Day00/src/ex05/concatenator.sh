
#!/bin/sh

input_dir="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex05/partitions"
output_csv="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex05/concatenated.csv"
temp_file=$(mktemp)

echo "\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"" > "$output_csv"

for file in "$input_dir"/*.csv; do
    tail -n +2 "$file" >> "$temp_file"
done

tail -n +1 "$temp_file" | sort -t ',' -k2,2 -k1,1n >> "$output_csv"