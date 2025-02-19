#!/usr/bin/python3

def replace_comma(substr: str) -> None:
    with open('/home/artem/s21/DS_Bootcamp.Day01-1/src/ex01/hh_sorted.csv', 'r') as file:
        content = file.read()

    inside_quotes = False
    modified_content = []

    for line in content:
        new_line = []
        
        for char in line:
            if char == '"':
                inside_quotes = not inside_quotes
            if char == ',' and not inside_quotes:
                new_line.append(substr)
            else:
                new_line.append(char)

        modified_content.append("".join(new_line))

    with open('/home/artem/s21/DS_Bootcamp.Day01-1/src/ex01/ds.tsv', 'w') as file:
        file.writelines(modified_content)


if __name__ == '__main__':
    replace_comma('\t')