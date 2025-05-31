import timeit
import sys
from functools import reduce


def loop_approach(sq_num: int) -> int:
    sum = 0
    for i in range(1, sq_num + 1):
        sum += i * i
    
    return sum


def reduce_approach(sq_num: int) -> int:
    return reduce(lambda acc, i: acc + i * i, range(1, sq_num + 1), 0)


def benchmark(approach: str, sq_num: int, calls_num: int) -> float:
    match approach.lower():
        case 'loop':
            func = lambda: loop_approach(sq_num)
        case 'reduce':
            func = lambda: reduce_approach(sq_num)
        case _:
            raise ValueError("Invalid approach")
        
    return timeit.timeit(func, number=calls_num)
        

if __name__ == "__main__":
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    if len(sys.argv) != 4:
        print("Usage: benchmark <benchmark name> <number of calls>")
        sys.exit(1)

    approach = sys.argv[1]
    calls_num = int(sys.argv[2])
    sq_num = int(sys.argv[3])
    try:
        times = benchmark(approach, sq_num, calls_num)
        print(times)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
        