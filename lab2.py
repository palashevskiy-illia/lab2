import functools
import multiprocessing
import time

@functools.lru_cache(None)
def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def prefill_cache(limit):
    for i in range(limit + 1):
        if i > 0 and (i & (i - 1)) == 0:
            collatz_steps(i)

def worker(start, end, step, result_queue):
    local_sum = 0
    local_count = 0

    for num in range(start, end, step):
        if num % 2 == 0:
            local_sum += collatz_steps(num // 2) + 1
        else:
            local_sum += collatz_steps(num)
        local_count += 1

    result_queue.put((local_sum, local_count))

def main():
    NUMBERS_COUNT = 10_000_000 
    NUM_PROCESSES = 8

    start_time = time.time()

    prefill_cache(NUMBERS_COUNT)

    result_queue = multiprocessing.Queue()

    processes = []
    for i in range(NUM_PROCESSES):
        p = multiprocessing.Process(
            target=worker,
            args=(i + 1, NUMBERS_COUNT + 1, NUM_PROCESSES, result_queue)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_steps = 0
    total_count = 0
    while not result_queue.empty():
        local_sum, local_count = result_queue.get()
        total_steps += local_sum
        total_count += local_count

    end_time = time.time()

    average_steps = total_steps / total_count
    elapsed_time = end_time - start_time
    print(f"\nСередня кількість кроків: {average_steps:.2f}")
    print(f"Час виконання: {elapsed_time:.2f} секунд")

if __name__ == "__main__":
    main()
