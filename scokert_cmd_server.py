import os
import socketserver

"""固定用户密码"""

USERINFO = {
    "root": "123456",
    "zhm": "123456"}


class FtpSocketServer(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        while True:
            try:
                pass
            except:
                pass

    def put(self):
        pass

    def dow(self):
        pass


if __name__ == '__main__':
    HOST, PORT = "localhost", 9090
    run = socketserver.ThreadingTCPServer((HOST, PORT), FtpSocketServer)
    run.serve_forever()
