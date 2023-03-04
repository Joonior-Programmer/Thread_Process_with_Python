from multiprocessing import Process, current_process, Queue, Pipe
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import time


def count_hundred_millions_with_queue(process_id:int, q: Queue):
    pid = os.getpid()
    process_name = current_process().name
    temp = 0
    for i in range(1, 100000001):
        """ If you want to see the work-flow, uncomment it """
        print(f"Process: {process_id}, Process Name: {process_name}, PID: {pid}, Added = {i}\n", end="")
        temp += 1

    q.put(temp)
    print(f"Process: {process_id} Done")


def count_hundred_millions_with_pipe(process_id:int, p: Pipe):
    pid = os.getpid()
    process_name = current_process().name
    temp = 0
    for i in range(1, 100000001):
        """ If you want to see the work-flow, uncomment it """
        # print(f"Process: {process_id}, Process Name: {process_name}, PID: {pid}, Added = {i}\n", end="")
        temp += 1

    p.send(temp)
    p.close()

    print(f"Child Process Done")


def main():
    # Queue
    start_time = time.time()
    queue = Queue()

    processes = []

    for i in range(1, 6):
        p = Process(name=(str(i)), target=count_hundred_millions_with_queue, args=(i, queue))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    queue.put("exit")
    total = 0

    while True:
        tmp = queue.get()
        if tmp == "exit":
            break
        total += tmp

    print(f"Total = {total}, {time.time() - start_time} Seconds")

    # Pipe
    # start_time = time.time()
    # parent_conn, child_conn = Pipe()
    #
    # p = Process(name=("Child"), target=count_hundred_millions_with_pipe, args=(1, child_conn))
    # p.start()
    # p.join()
    #
    # print(f"Result = {parent_conn.recv()}, Parent Process Done, {time.time() - start_time} Seconds")


if __name__ == "__main__":
    main()