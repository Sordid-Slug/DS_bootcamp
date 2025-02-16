
#!/bin/sh

output_file=hh.json
per_page=20
name="data scientist"
api_url="https://api.hh.ru/vacancies"

response=`curl -s -G "$api_url" \
    --data-urlencode "text=$name" \
    --data-urlencode "per_page=$per_page"`

echo "$response" | jq . > "$output_file"