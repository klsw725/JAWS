from threading import Thread, Lock
import time
import cv2
import numpy as np
import base64
import re

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def incode_video(img):
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    result, incode_img = cv2.imencode('.jpg', img, encode_params)
    return incode_img.tobytes()


def decode_video(bimg):
    decodeImg = decode_base64(bimg)
    img_array = np.frombuffer(decodeImg, dtype=np.dtype('uint8'))
    # Decode a colored image
    return  cv2.imdecode(img_array, flags=cv2.IMREAD_UNCHANGED)

class Video(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.buff = None # 공유 자원
        self.lock = Lock()

    def get_buffer(self):
        if self.buff is not None:
            self.lock.acquire()
            cbuff = self.buff
            self.lock.release()
            return cbuff

    def run(self):
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue
            self.lock.acquire()
            self.buff = incode_video(img)
            self.lock.release()

    def stop(self):
        self.running = False