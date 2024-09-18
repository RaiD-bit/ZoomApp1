import redis
from cv2Util import produceDate, consumeData
import threading

def producer():
    # start producing your data
    client_A = redis.Redis()

    produceDate(0, 'ClientA', client_A)


def consumer():
    #consume data
    client = redis.Redis()

    pubsub_client = client.pubsub()

    pubsub_client.subscribe("ClientB")

    consumeData("B", pubsub_client)


# create threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for both threads to finish
producer_thread.join()
consumer_thread.join()
