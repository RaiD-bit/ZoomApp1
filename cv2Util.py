import cv2
import numpy as np
import struct


def take_video_input(device):
    cap = cv2.VideoCapture(device)
    return cap


def produce_data(input, clientId, redisObject):
    cp = take_video_input(input)

    while True:
        ret, frame = cp.read()
        if not ret:
            break

        shape = frame.shape
        shape_bytes = struct.pack('>3I', shape[0], shape[1], shape[2])  # 3 integers (height, width, channels)
        message = shape_bytes + frame.tobytes()
        redisObject.publish(clientId, message)

        cv2.imshow(clientId, frame)

        # If the user presses 'q', exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cp.release()
    cv2.destroyAllWindows()


def consume_data(callerId, pubsub_client):
    while True:
        msg = pubsub_client.get_message()
        if msg != None:
            try:
                d = np.frombuffer(msg["data"], dtype="uint8")
                shape_bytes = msg['data'][:12]
                height, width, channels = struct.unpack('>3I', shape_bytes)
                print(f"ht: {height}, width: {width}, channel : {channels}")
                frame_bytes = msg['data'][12:]
                frame = np.frombuffer(frame_bytes, dtype="uint8").reshape(height, width, channels)
            except Exception as e:
                print(e)
                pass
            # print(f"msg from my-channel: {msg}")
            try:
                cv2.imshow(callerId, frame)
            except:
                pass
        # If the user presses 'q', exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
