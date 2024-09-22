from is_wire.core import Channel, Subscription, Message
from is_msgs.image_pb2 import Image
import numpy as np
import cv2
import json
import time


def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image

if __name__ == '__main__':
    print('--- Saving the image ---')
    
    channel = Channel("amqp://guest:guest@localhost:5672")
    subscription = Subscription(channel)
    subscription.subscribe(topic='Topic.Frame')

    while True:
      msg = channel.consume()
      img_unpack = msg.unpack(Image)
      imgNP = to_np(img_unpack)

      filename = 'image_rcvd.jpg'

      cv2.imwrite(filename, imgNP)
      print('Image saved')
      break


