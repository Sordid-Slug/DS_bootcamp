
#!/bin/sh

csv_to_sort="../ex01/hh.csv"
output_file="hh_sorted.csv"

head -n 1 "$csv_to_sort"> "$output_file"

tail -n +2 "$csv_to_sort" | sort -t ',' -k2,2 -k1,1n >> "$output_file"