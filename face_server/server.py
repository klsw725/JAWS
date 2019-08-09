import sys
import socket

import cv2
import numpy as np
import face_recognition
from PIL import Image as PIL_Image

import pymysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Images

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

engine = create_engine('mysql+pymysql://root:root@localhost/test')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# jennie_image = face_recognition.load_image_file("pics/jennie.png")
# jennie_face_encoding = face_recognition.face_encodings(jennie_image)[0]

images = session.query(Images).all()

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

for image in images:
    src = face_recognition.load_image_file(image.location)
    height, width, channel = src.shape
    matrix = cv2.getRotationMatrix2D((width/2, height/2), -90, 1)
    temp_image = cv2.warpAffine(src, matrix, (width, height))

    cv2.imshow("Moon", src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    temp_image_encoding = face_recognition.face_encodings(src)[0]

    known_face_encodings.append(temp_image_encoding)
    known_face_names.append(image.name)


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

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)

                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                        print(matches)
                        name = "Unknown"

                        # If a match was found in known_face_encodings, just use the first one.
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                        face_names.append(name)

                process_this_frame = not process_this_frame

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
