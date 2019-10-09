# -*- coding: utf-8 -*-

import sys
import socket
import threading
from queue import Queue

import cv2
import numpy as np
import face_recognition
import paho.mqtt.client as mqtt

import pymysql

import face
import video
import detect

from PIL import Image


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


def detectFace(core, q1, q2):
    print("create thread")
    while True:
        frame, evt = q1.get()
        evt.set()
        q1.task_done()
        result = core.run(frame)
        evt = threading.Event()
        q2.put((result, evt))
        evt.wait()


def handle_client(conn, addr):
    print('Connected by', addr)
    q1 = Queue()
    q2 = Queue()
    thread_one = threading.Thread(target=detectFace, args=(core, q1, q2))
    thread_one.start()
    try:
        while True:
            recv_data_into(conn, tmp_view, 12)
            cmd = tmp_buf.decode('ASCII')
            # cmd = conn.recv(999999999)
            if cmd[:5] == 'image':
                # Read the image buffer size
                # recv_data_into(conn, tmp_view, 7)
                #
                # img_size = int(tmp_buf.decode('ASCII'))
                img_size = int(cmd[5:])
                #
                # # # Read the buffer content

                recv_data_into(conn, img_view[:img_size], img_size)
                # #
                # # Decode the image

                img = video.decode_video(img_view[:img_size])

                # Display the resulting image
                # cv2.imshow('Video', img)
                #
                # # Hit 'q' on the keyboard to quit!
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

                evt = threading.Event()
                q1.put((img, evt))
                evt.wait()

                # total = eyedetect.run(img)
                # print(total)
                # result = core.run(img)
                result, evt = q2.get()
                evt.set()
                q2.task_done()
                print(result)

                if (result):
                    print("open")
                    mqttc.publish("jaws", "open")
                    conn.close()
                    break

            elif cmd == 'quit!':
                break
            else:
                print("Got something else")
    except:
        print("Server Close")
        conn.close()


host = '127.0.0.1'
port = 9009

conn = pymysql.connect(host='localhost', user='username', password='password', db='test', charset='utf8')
curs = conn.cursor()
curs.execute("select * from api_images")
images = curs.fetchall()

core = face.Face()
core.face_encoding(images)

eyedetect = detect.EyeDetect()

mqttc = mqtt.Client()      # MQTT Client 오브젝트 생성
mqttc.connect("ddotmotion.kr", 9883)    # MQTT 서버에 연결

# A temporary buffer in which the received data will be copied
# this prevents creating a new buffer all the time
tmp_buf = bytearray(12)
tmp_view = memoryview(tmp_buf)  # this allows to get a reference to a slice of tmp_buf

# Creates a temporary buffer which can hold the largest image we can transmit
img_buf = bytearray(9999999)
img_view = memoryview(img_buf)

if __name__ == "__main__":
    print("main server start")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                s.bind((host, port))
                s.listen(5)
                conn, addr = s.accept()
                server_t = threading.Thread(target=handle_client, args=(conn, addr))
                server_t.daemon = True
                server_t.start()

        except KeyboardInterrupt:
            print("Keyboard interrupt")
