import redis
from cv2Util import produce_data, consume_data
import threading

def producer():
    # start producing your data
    client_B = redis.Redis()

    produce_data("catvids/orange_cat.mp4", 'ClientB', client_B)


def consumer():
    #consume data
    client = redis.Redis()

    pubsub_client = client.pubsub()

    pubsub_client.subscribe("ClientA")

    consume_data('A', pubsub_client)



if __name__ == '__main__':
    # create threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    # Start the threads
    producer_thread.start()
    consumer_thread.start()

    # Wait for both threads to finish
    producer_thread.join()
    consumer_thread.join()