"""

Topic: Shared Data, Lock

Keyword: Lock

Description: See what happens if we use mutual exclusion for shared data when we use multithread

"""


from concurrent.futures import ThreadPoolExecutor
import time
import logging
import threading


class SharedDataWithLock:

    # Shared Data => self.value

    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increase_value(self, name):
        """
        Critical Section (Shared Data) will be accessed by only 1 thread which acquired the "Access permission".
        Moreover, if there are other threads which want to access to Critical Section 
                    while another thread is accessing to the Critical Section.
        The other threads will go into the "Queue" to wait for the releasing the "Lock"
        """

        logging.info("Thread %s started", name)

        # First Way

        # logging.info(
        #     "Thread %s wants to access to the Critical Section.", name)
        # self._lock.acquire()
        # logging.info("Thread %s accessed to the Critical Section.", name)

        # get_value = self.value
        # logging.info("Thread %s starts getting the value -> %d",
        #              name, get_value)
        # get_value += 1
        # logging.info("Thread %s starts updating the value -> %d",
        #              name, get_value)

        # # pretend context switching
        # time.sleep(0.01)

        # self.value = get_value
        # logging.info("Thread %s starts saving the value -> %d",
        #              name, self.value)
        # self._lock.release()
        # logging.info("Thread %s released the Lock", name)

        # Second Way (Recommended)

        logging.info(
            "Thread %s wants to access to the Critical Section.", name)

        with self._lock:
            logging.info("Thread %s accessed to the Critical Section.", name)

            get_value = self.value
            logging.info("Thread %s starts getting the value -> %d",
                         name, get_value)
            get_value += 1
            logging.info("Thread %s starts updating the value -> %d",
                         name, get_value)

            # pretend context switching
            time.sleep(0.01)

            self.value = get_value
            logging.info("Thread %s starts saving the value -> %d",
                         name, self.value)

        logging.info("Thread %s released the Lock", name)


def main():
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format,
                        level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main-Thread starts")

    logging.info("Creates Thread Pool")

    sharedData = SharedDataWithLock()

    with ThreadPoolExecutor(max_workers=3) as executor:
        for name in ["First", "Second", "Third"]:
            executor.submit(sharedData.increase_value, name)

    print("Final Value => ", sharedData.value)
    logging.info("Main-Thread done")


if __name__ == "__main__":
    main()
