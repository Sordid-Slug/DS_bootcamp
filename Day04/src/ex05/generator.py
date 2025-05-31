#!/usr/bin/env python3
import sys
import resource

def read_lines(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line

def main():
    if len(sys.argv) < 2:
        print("Usage: ordinary.py <path_to_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    start_usage = resource.getrusage(resource.RUSAGE_SELF)

    for line in read_lines(file_path):
        pass
    
    end_usage = resource.getrusage(resource.RUSAGE_SELF)
    peak_memory_gb = end_usage.ru_maxrss / (1024.0 * 1024)

    user_mode_time = end_usage.ru_utime - start_usage.ru_utime
    system_mode_time = end_usage.ru_stime - start_usage.ru_stime
    total_time = user_mode_time + system_mode_time
    
    print(f"Peak memory usage: {peak_memory_gb:.4f} GB")
    print(f"User+System time: {total_time:.4f} seconds")
    print(f"User mode time: {user_mode_time:.4f} seconds")
    print(f"System mode time: {system_mode_time:.4f} seconds")

if __name__ == "__main__":
    main()
