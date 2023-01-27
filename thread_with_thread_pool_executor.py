"""

Topic: Thread Pool Executor

Description: You can follow the logs to know what max_worker is, and how to manage Threads better

"""


from concurrent.futures import ThreadPoolExecutor
import time
import logging

# Each Thread will Execute this function


def test_thread_func(thread_num: int, n: int) -> int:
    result = 0
    logging.info("%s-Thread : started", thread_num)
    for i in range(n):
        print(thread_num, i)
        result += i
    logging.info("%s-Thread : done", thread_num)
    return result


def main():
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format,
                        level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main-Thread starts")

    logging.info("Creates Thread Pool")

    # First way

    # executor = ThreadPoolExecutor(max_workers=3)

    # task1 = executor.submit(test_thread_func, 1, 400000)
    # task2 = executor.submit(test_thread_func, 2, 500000)

    # print(task1.result())
    # print(task2.result())

    # Second Way (Encouraged to use)

    with ThreadPoolExecutor(max_workers=3) as executor:
        print(zip([1, 2, 3, 4], [5, 6, 7, 8]))
        tasks = executor.map(test_thread_func, [1, 2, 3, 4], [
            10, 20, 30, 40])

        print(list(tasks))

    logging.info("Main-Thread done")


if __name__ == "__main__":
    main()
