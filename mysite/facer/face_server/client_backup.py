# import socket
# import sys
#
# import cv2
# import numpy as np
#
# HOST, PORT = "127.0.0.1", 9009
#
# video_capture = cv2.VideoCapture(0)
#
# # data = " ".join(sys.argv[1:])
#
# # SOCK_DGRAM is the socket type to use for UDP sockets
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # As you can see, there is no connect() call; UDP has no connections.
# # Instead, data is directly sent to the recipient via sendto().
#
#
# ret, frame = video_capture.read()
# print(sys.getsizeof(frame))
# small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
# #print(small_frame)
# #print(small_frame.size)
# print(sys.getsizeof(small_frame))
# byte_frame = small_frame.tobytes()
# #print(byte_frame)
# recover_frame = np.frombuffer(byte_frame, dtype=np.int8)
# #print(recover_frame)
# # sock.sendto(bytes("HelloWorld","utf-8"), (HOST, PORT))
# print(byte_frame)
# sock.sendto(bytes(byte_frame), (HOST, PORT))
# # received = str(sock.recv(1024), "utf-8")
#
# # print("Sent:     {}".format(data))
# # print("Received: {}".format(received))