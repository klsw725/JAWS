import socketserver

HOST = ''
PORT = 9009


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = self.request


def runServer():
    server = socketserver.UDPServer((HOST, PORT), MyTcpHandler)
    server.serve_forever()


if __name__ == '__main__':
    try:
        runServer()
    except Exception as err:
        print(err)
