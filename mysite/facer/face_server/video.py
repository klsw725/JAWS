from threading import Thread, Lock
import time
import cv2
import numpy as np

def incode_video(img):
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    result, incode_img = cv2.imencode('.jpg', img, encode_params)
    return incode_img.tobytes()


def decode_video(bimg):
    img_array = np.frombuffer(bimg, dtype=np.dtype('uint8'))
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