"""

Topic: Shared Data, Lock

Description: See what happens if we do not use mutual exclusion for shared data when we use multithread

"""


from concurrent.futures import ThreadPoolExecutor
import time
import logging


class SharedDataWithoutLock:

    # Shared Data => self.value

    def __init__(self) -> None:
        self.value = 0

    def increase_value(self, name):
        """
        Pretend how assembly code works when we change the value
        1. Get the value
        2. Update the value
        3. Save the value

        However, what if two or more threads get the value before save its value?

        Ex) Show One of the possible case when if increase the value 3 times

        value        T1                         T2                      T3
        0         Get v: 0
                  Update v: 1
                  Context Swtiching ->
                                            Get v: 0
                                            Update v: 1
        1                                   Save the value
                                            Done
                                            Context Switching ->
                                                                        Get v: 1
                                                                        Update v: 2
        2                                                               Save the value
                                                                        Done
                                                                    <-  Context Switching
        1       Save the value
                Done
        """

        logging.info("Thread %s started", name)

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


def main():
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format,
                        level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main-Thread starts")

    logging.info("Creates Thread Pool")

    sharedData = SharedDataWithoutLock()

    with ThreadPoolExecutor(max_workers=3) as executor:
        for name in ["First", "Second", "Third"]:
            executor.submit(sharedData.increase_value, name)

    print("Final Value => ", sharedData.value)
    logging.info("Main-Thread done")


if __name__ == "__main__":
    main()
