"""

Topic: Thread

Keyword: Main Thread, Child Thread, Daemon Thread, Thread.join()

"""

import threading
import time
import logging


def test_thread_func(name, n):
    logging.info("%s-Thread : started", name)
    for i in range(n):
        print(name, i, "\n", end="")
    logging.info("%s-Thread : done", name)


def main():
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format,
                        level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main-Thread starts")

    logging.info("Creates Child-Threads")

    child_thread = threading.Thread(
        target=test_thread_func, args=("Child", 5000000,))

    daemon_thread = threading.Thread(
        target=test_thread_func, args=("Daemon", 5000000,), daemon=False)

    # Starts Created Thread

    child_thread.start()
    daemon_thread.start()

# Stop Main Thread until the Child Threads finish

# child_thread.join()
# daemon_thread.join()


logging.info("Main-Thread done")


if __name__ == "__main__":
    main()
