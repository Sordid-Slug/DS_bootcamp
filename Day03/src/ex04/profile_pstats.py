#!/usr/bin/python3

import pstats

with open('pstats-cumulative.txt', 'w') as f:
    p = pstats.Stats('profiling-http', stream=f)
    p.sort_stats('cumulative').print_stats(5)