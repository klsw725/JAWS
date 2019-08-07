import sys
import socket

import cv2
import numpy as np
import video



def image_process(cv2_img):
    # For fun, we play with the image
    cv2_img = 255 - cv2_img
    return cv2_img

def recv_data(sock, torecv):
    msg = b''
    while torecv > 0:
        chunk = sock.recv(torecv)
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        msg += chunk
        torecv -= len(chunk)
    return msg

def recv_data_into(sock, buf_view, torecv):
    while torecv > 0:
        numrecv = sock.recv_into(buf_view[-torecv:], torecv)
        if numrecv == 0:
            raise RuntimeError("Socket connection broken")
        torecv -= numrecv

host = '127.0.0.1'
port = 9009

# jpeg_encode_func = lambda img: video.incode_video(img)
# jpeg_decode_func = lambda buf: video.decode_video(buf)

# A temporary buffer in which the received data will be copied
# this prevents creating a new buffer all the time
tmp_buf = bytearray(7)
tmp_view = memoryview(tmp_buf)  # this allows to get a reference to a slice of tmp_buf

# Creates a temporary buffer which can hold the largest image we can transmit
img_buf = bytearray(9999999)
img_view = memoryview(img_buf)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            recv_data_into(conn, tmp_view[:5], 5)
            cmd = tmp_buf[:5].decode('ascii')
            if (cmd == 'image'):
                # Read the image buffer size
                recv_data_into(conn, tmp_view, 7)
                img_size = int(tmp_buf.decode('ascii'))

                # Read the buffer content
                recv_data_into(conn, img_view[:img_size], img_size)

                # Decode the image
                img = video.decode_video(img_view[:img_size])

                # Process it
                # res = image_process(img)

                # Encode the image
                # res_buffer = video.incode_video(res)

                # # Make the reply
                # reply = bytes("image{:07}".format(len(res_buffer)), "ascii")
                # utils.send_data(conn, reply)
                # utils.send_data(conn, res_buffer)
                # utils.send_data(conn, bytes('enod!', 'ascii'))
            elif cmd == 'quit!':
                break
            else:
                print("Got something else")
        print("Quitting")
