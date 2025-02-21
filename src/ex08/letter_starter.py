#!/usr/bin/python3

import sys


def correctness_input() -> None:
    if len(sys.argv) != 2:
        print("Usage: letter_starter.py <email>")
        sys.exit()


def find_employee(email) -> str:
    name = "There is not employye with that email"

    with open("employees.tsv", 'r') as file:
        employees = file.read().splitlines()

        for emp in employees[1:]:
            emp = emp.split('\t')
            if emp[2] == email:
                name = emp[0]
        
    return name

def send_letter(name: str) -> None:
    print(f'Dear {name}, welcome to our team.\n' 
          f'We are sure that it will be a pleasure to work with you.\n'
          f'That’s a precondition for the professionals that our company hires.')


if __name__ == '__main__':
    correctness_input()
    email = sys.argv[1]
    name = find_employee(email)
    send_letter(name)