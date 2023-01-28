"""

Topic: Producer Consumer Pattern

Description: Flow of data processing => Producer, Consumer, Pipeline(Queue)
            
             Python Event Object
             Flag: When flag is down, workers will work       => 0
                   When flag is up, workers will stop working => 1
             
             Set:   Flag to 1
             Clear: Flag to 0
             Wait:  when Flag 1 => Return
                              0 => Wait
            isSet:  Current Flag State
             

"""


from concurrent.futures import ThreadPoolExecutor
import time
import logging
import threading
import queue
import random


def producer(queue: queue.Queue, event: threading.Event):
    while not event.is_set():
        new_message = random.randint(1, 100)
        queue.put(new_message)
        logging.info("Producer produced the message %d", new_message)

    logging.info("Producer stopped producing")


def consumer(queue: queue.Queue, event: threading.Event):
    # unlike Producer, Consumer has to finish the jobs in the pipeline (Queue)
    while not event.is_set() or not queue.empty():
        new_message = queue.get()
        logging.info("Consumer got the message %d /// Queue Size = %d",
                     new_message, queue.qsize())

    logging.info("Consumer stopped Consuming")


def main():
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format,
                        level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main-Thread starts")

    logging.info("Creates Thread Pool")

    event = threading.Event()
    pipeline = queue.Queue(maxsize=100)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)

        # End
        logging.info("Event Set... Stop Working")
        event.set()

    logging.info("Main-Thread done")


if __name__ == "__main__":
    main()
