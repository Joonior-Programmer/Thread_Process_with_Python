"""

Topic: Thread Pool Executor

Description: You can follow the logs to know what max_worker is, and how to manage Threads better

"""
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
import logging
import ssl
import certifi
import threading


def visit(url, timeout, context):
    with urllib.request.urlopen(url=url, timeout=timeout, context=context) as conn:
        print(f"{url}: {len(conn.read())}Bytes")


# Each Thread will Execute these function
def test_thread_func(thread_num: int, n: int) -> int:
    result = 0
    logging.info("%s-Thread : started", thread_num)
    for i in range(n):
        print(thread_num, i)
        result += i
    logging.info("%s-Thread : done", thread_num)
    return result


def main():
    # log_format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=log_format,
    #                     level=logging.INFO, datefmt="%H:%M:%S")
    # logging.info("Main-Thread starts")
    #
    # logging.info("Creates Thread Pool")
    #
    # # First way
    #
    # # executor = ThreadPoolExecutor(max_workers=3)
    #
    # # task1 = executor.submit(test_thread_func, 1, 400000)
    # # task2 = executor.submit(test_thread_func, 2, 500000)
    #
    # # print(task1.result())
    # # print(task2.result())
    #
    # # Second Way (Encouraged to use)
    #
    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     print(zip([1, 2, 3, 4], [5, 6, 7, 8]))
    #     tasks = executor.map(test_thread_func, [1, 2, 3, 4], [
    #         10, 20, 30, 40])
    #
    #     print(list(tasks))
    #
    # logging.info("Main-Thread done")

    # Example 2
    urls = ["http://bcit.ca", "http://www.ubc.ca/", "http://www.sfu.ca/", "http://www.stanford.edu/",
            "http://naver.com", "http://daum.net", "http://notion.so", "https://www.kakaocorp.com/page/"] * 3
    context = ssl.create_default_context(cafile=certifi.where())
    #
    with ThreadPoolExecutor(max_workers=20) as executor:
        start = time()
        future_to_url = {executor.submit(visit, url, 5, context): url for url in urls}

        # print(future_to_url)

        for future in as_completed(future_to_url):
            future.done()
        print(f"{time() - start} seconds to visit {len(urls)} websites")

    # # Visit websites without pool executor
    # start = time()
    # tasks = []
    # for url in urls:
    #     t = threading.Thread(target=visit, args=(url, 5, context))
    #     t.start()
    #     tasks.append(t)
    #
    # for task in tasks:
    #     task.join()
    #
    # print(f"{time() - start} seconds to visit {len(urls)} websites")


if __name__ == "__main__":
    main()
