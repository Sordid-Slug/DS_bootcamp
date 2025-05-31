import timeit
import sys

def loop_approach(emails: list) -> list:
    gmails = []

    for email in emails:
        if email.endswith('@gmail.com'):
            gmails.append(email)

    return gmails

def comprehension_approach(emails: list) -> list:
    gmails = [email for email in emails if email.endswith('@gmail.com')]

    return gmails

def map_approach(emails: list) -> list:
    gmails = list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))

    return gmails

def filter_approach(emails: list) -> list:
    gmails = list(filter(lambda email: email.endswith('@gmail.com'), emails))

    return gmails

def benchmark(approach: str, emails: list, calls_num: int) -> float:
    match approach.lower():
        case 'loop':
            func = lambda: loop_approach(emails)
        case 'list_comprehension':
            func = lambda: comprehension_approach(emails)
        case 'map':
            func = lambda: map_approach(emails)
        case 'filter':
            func = timeit.timeit(lambda: filter_approach(emails), number=calls_num)
        case _:
            raise ValueError("Invalid approach")
    
    return timeit.timeit(func, number=calls_num)
        

if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    if len(sys.argv) != 3:
        print("Usage: benchmark <benchmark name> <number of calls>")
        sys.exit(1)

    approach = sys.argv[1]
    calls_num = int(sys.argv[2])
    try:
        times = benchmark(approach, emails, calls_num)
        print(times)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
        