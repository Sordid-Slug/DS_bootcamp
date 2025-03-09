import timeit

def loop_approach(emails: list) -> list:
    gmails = []

    for email in emails:
        if email.endswith('@gmail.com'):
            gmails.append(email)

    return gmails

def comprehension_approach(emails: list) -> list:
    gmails = [email for email in emails if email.endswith('@gmail.com')]

    return gmails

if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    n = 9_000_000
    time_loop = timeit.timeit(lambda: loop_approach(emails), number = n)
    time_compr = timeit.timeit(lambda: comprehension_approach(emails), number = n)

    if time_loop >= time_compr:
        print('it is better to use a list comprehension')
    else:
        print('it is better to use a loop')

    times = {
        'Loop' : time_loop,
        "Comprehension" : time_compr
    }
    times = sorted(times.items(), key=lambda x: x[1])
    
    print(f"{times[0][1]} vs {times[1][1]}")