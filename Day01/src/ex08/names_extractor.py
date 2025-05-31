#!/usr/bin/python3

import sys


def correctness_input() -> None:
    if len(sys.argv) != 2:
        print("Usage: names_extractor.py <input file>")
        sys.exit()


def read_email_from_file() -> None:
    try:
        with open(sys.argv[1], 'r') as file:
            emails = file.read().splitlines()

            employees = []
            for email in emails:
                name_part = email.split('@')[0]
                name, surname = name_part.split('.')

                name = name.capitalize()
                surname = surname.capitalize()
                employees.append((name, surname, email))
            
        with open("employees.tsv", 'w') as file:
            file.write("Name\tSurname\tEmail\n")

            for emp in employees:
                file.write(f'{emp[0]}\t{emp[1]}\t{emp[2]}\n')

    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    correctness_input()
    read_email_from_file()