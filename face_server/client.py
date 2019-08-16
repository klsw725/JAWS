import socket
import sys

import time

import cv2
import numpy as np

import video

host         = "127.0.0.1"
port         = 9009

# cv2.namedWindow("Image")

keep_running = True


jpeg_encode_func = lambda img: video.incode_video(img)
jpeg_decode_func = lambda buf: video.decode_video(buf)

def send_data(sock, msg):
    totalsent = 0
    tosend = len(msg)
    while totalsent < tosend:
        numsent = sock.send(msg[totalsent:])
        if numsent == 0:
            raise RuntimeError("Socket connection broken")
        totalsent += numsent

# A lambda function to get a cv2 image
# encoded as a JPEG compressed byte sequence


if __name__ == "__main__":
    video = video.Video()
    video.start()

    #get_buffer = lambda: utils.encode_image(cv2.imread("monarch.png",cv2.IMREAD_UNCHANGED), jpeg, jpeg_quality)

    # A temporary buffer in which the received data will be copied
    # this prevents creating a new buffer all the time
    tmp_buf = bytearray(7)
    tmp_view = memoryview(tmp_buf) # this allows to get a reference to a slice of tmp_buf

    # Creates a temporary buffer which can hold the largest image we can transmit
    img_buf = bytearray(9999999)
    img_view = memoryview(img_buf)

    idx = 0
    t0  = time.time()

    # while keep_running:
    #     img_buffer = video.get_buffer()
    #     if img_buffer is None:
    #         continue
    #     msg = bytes("image{:07}".format(len(img_buffer)), "ascii")
    #     try:
    #         requests.post(host, data={'msg':msg})
    #         requests.post(host, data={'img_buffer':img_buffer})
    #     except:
    #         print('requests.posts error')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            while keep_running:

                # Grab and encode the image
                img_buffer = video.get_buffer()
                if img_buffer is None:
                    continue

                # Prepare the message with the number of bytes going to be sent
                msg = bytes("image{:07}".format(len(img_buffer)), "ascii")

                send_data(sock, msg)

                # Send the buffer
                send_data(sock, img_buffer)

                # # Read the reply command
                # recv_data_into(sock, tmp_view[:5], 5)
                # cmd = tmp_buf[:5].decode('ascii')
                #
                # if cmd != 'image':
                #     raise RuntimeError("Unexpected server reply")
                #
                # # Read the image buffer size
                # recv_data_into(sock, tmp_view, 7)
                # img_size = int(tmp_buf.decode('ascii'))
                #
                # # Read the image buffer
                # recv_data_into(sock, img_view[:img_size], img_size)
                #
                # # Read the final handshake
                # cmd = recv_data(sock, 5).decode('ascii')
                # if cmd != 'enod!':
                #     raise RuntimeError("Unexpected server reply. Expected 'enod!', got '{}'".format(cmd))
                #
                # # Transaction is done, we now process/display the received image
                # img = jpeg_decode_func(img_view[:img_size])
                # cv2.imshow("Image", img)
                # keep_running = not(cv2.waitKey(1) & 0xFF == ord('q'))
                # if not keep_running:
                #     sock.sendall('quit!'.encode('ascii'))
                #
                idx += 1
                if idx == 30:
                    t1 = time.time()
                    # sys.stdout.write("\r {:.3} images/second ; msg size : {}    ".format(30/(t1-t0), img_size))
                    # sys.stdout.flush()
                    t0 = t1
                    idx = 0
            print()
            print("Closing the socket")
    except:
        print("Stopping the grabber")
        video.stop()

