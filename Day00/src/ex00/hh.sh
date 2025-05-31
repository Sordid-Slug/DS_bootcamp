
#!/bin/sh

output_file="/home/artem/s21/DS_Bootcamp.Day00-1/src/ex00/hh.json"
per_page=50
name=$1
api_url="https://api.hh.ru/vacancies"

response=`curl -s -G "$api_url" \
    --data-urlencode "text=$name" \
    --data-urlencode "per_page=$per_page"`

echo "$response" | jq . > "$output_file"