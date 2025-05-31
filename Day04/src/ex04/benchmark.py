import timeit
import sys
from collections import Counter
import random


def count_occurances(lst) -> dict:
    res_dict = {num : 0 for num in range(101)}
    for num in lst:
        res_dict[num] += 1

    return res_dict


def top_10(lst) -> list:
    count_dict = count_occurances(lst)
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:10]


def benchmark(random_list: list, calls_num: int) -> float:
    times = []
        
    times.append(timeit.timeit(lambda: count_occurances(random_list), number=calls_num))
    times.append(timeit.timeit(lambda: Counter(random_list), number=calls_num))
    times.append(timeit.timeit(lambda: top_10(random_list), number=calls_num))
    times.append(timeit.timeit(lambda: Counter(random_list).most_common(10), number=calls_num))

    return times
        

if __name__ == "__main__":
    random_list = [random.randint(0, 100) for _ in range(1_000_000)]

    try:
        times = benchmark(random_list, 10)
        print('my function: ', times[0])
        print('Counter: ', times[1])
        print('my top: ', times[2])
        print("Counter's top: ", times[3])
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
        