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

def map_approach(emails: list) -> list:
    gmails = list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))

    return gmails

if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    n = 9_000_000
    time_loop = timeit.timeit(lambda: loop_approach(emails), number=n)
    time_compr = timeit.timeit(lambda: comprehension_approach(emails), number=n)
    time_map = timeit.timeit(lambda: map_approach(emails), number=n)

    if time_compr <= time_loop and time_compr <= time_map:
        print('it is better to use a list comprehension')
    elif time_loop <= time_compr and time_loop <= time_map:
        print('it is better to use a loop')
    else:
        print('it is better to use a map')
    

    times = {
        'Loop' : time_loop,
        "Comprehension" : time_compr,
        "Map" : time_map
    }
    times = sorted(times.items(), key=lambda x: x[1])
    
    print(f"""
    {times[0][0]} vs {times[1][0]} vs {times[2][0]})
    {times[0][1]} vs {times[1][1]} vs {times[2][1]}""")