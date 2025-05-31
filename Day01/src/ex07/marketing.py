#!/usr/bin/python3

import sys


def get_clients_not_promoted(clients: list, recipients: list) -> list:
    not_promoted_clients = set(clients).difference(recipients)
    
    return list(not_promoted_clients)


def get_not_clients(clients: list, participants: list) -> list:
    not_clients = set(participants).difference(clients)

    return list(not_clients)


def get_clients_not_participant(clients: list, participants: list) -> None:
    clients_not_participant = set(clients).difference(participants)

    return list(clients_not_participant)


def input_corretness() -> None:
    if len(sys.argv) != 2:
        raise Exception("Incorrect quantity of input arguments")
    
    permissible = ["call_center",
                   "potential_clients",
                   "loyalty_program"]
    if sys.argv[1] not in permissible:
        raise Exception("Incorrect input argument")


if __name__ == "__main__":
    input_corretness()

    clients = [ 'andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
                'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
                'elon@paypal.com', 'jessica@gmail.com']
    
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    match sys.argv[1]:
        case "call_center":
            get_clients_not_promoted(clients, recipients)
        case "potential_clients":
            get_not_clients(clients, participants)
        case "loyalty_program":
            print(get_clients_not_participant(clients, participants))