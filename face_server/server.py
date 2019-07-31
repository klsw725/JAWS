import socketserver
import face_recognition
import cv2

HOST = '127.0.0.1'
PORT = 9009


class MyUdpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

def runServer():
    server = socketserver.UDPServer((HOST, PORT), MyUdpHandler)
    server.serve_forever()


if __name__ == '__main__':
    try:
        runServer()
    except Exception as err:
        print(err)
