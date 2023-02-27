from multiprocessing import Process, Value, current_process
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import time


def add_one_not_sharing(v: int, process: int):
    process_name = current_process().name
    pid = os.getpid()
    for _ in range(10000):
        v += 1
        print(f"Process:{process}, PID: {pid}, PName: {process_name}, Value = {v}")
    print(f"Process:{process}, PID: {pid}, PName: {process_name} Done")


def add_one_sharing(v: Value, process: int):
    process_name = current_process().name
    pid = os.getpid()
    for _ in range(10000):
        # time.sleep(0.1)
        v.value += 1
        print(f"Process:{process}, PID: {pid}, PName: {process_name}, Value = {v.value}")
    print(f"Process:{process}, PID: {pid}, PName: {process_name} Done")


def main():
    # Shared X
    # value = 0
    #
    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(add_one_not_sharing(value, i)) for i in range(1,11)]
    #
    #     for future in as_completed(futures):
    #         future.done()
    #
    # print(f"Final Value = {value}")

    # Shared O with Lock
    # value = Value('i', 0)
    #
    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(add_one_sharing(value, i)) for i in range(1,11)]
    #
    #     for future in as_completed(futures):
    #         future.done()

    # Shared O without Lock
    """ As You can see, if there is no lock, the value might be the case as you expected"""
    value = Value('i', 0, lock=False)
    processes = []
    for i in range(1, 11):
        processes.append(Process(target=add_one_sharing, args=(value, i)))

    for process in processes:
        process.start()

        # If you want to lock, Add line below
        # process.join()

    print(f"Final Value = {value.value}")


if __name__ == "__main__":
    main()
