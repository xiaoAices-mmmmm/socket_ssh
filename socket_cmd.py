import json
import os.path
import socket
import sys
import time
"""
varsion:1.0.1
"""


class FtpClinet:
    def __init__(self,username,password,host="locathost",port=9090):
        self.username = username
        self.password = password
        self.host = (host,port)
        self.clint = socket.socket()
        self.clint.connect(self.host)
        self.interaction()
        self.clint.close()

    def interaction(self):
        while True:
            cmd_input = input(">>{%s}:"%self.username).strip()
            if len(cmd_input) == 0:continue;
            cmd_str = cmd_input.strip()[0]
            if hasattr(self,"cmd_%s"%cmd_str):  # put filename
                func = getattr(self,cmd_str)
                func(cmd_input)
            else:
                print(self.help)
            self.clint.send(cmd_input.encode("utf-8"))

        pass

    def cmd_put(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                fileinfo = {
                    "filename":filename,
                    "size":filesize,
                    "overridden":True  # 传输状态
                }
                self.clint.send(json.dumps(fileinfo).encode("utf-8")) # 将文件大小发送过去
                # 防止粘包
                server_reponse = self.clint.recv(1024)
                if server_reponse.decode("utf-8") == "200":
                    with open(filename,"rb") as fp:
                        for line in fp:
                            self.clint.send(line)
                else:
                    print(server_reponse.decode("utf-8"))
            else:
                print(filename,"is not exist")

    def cmd_dow(self,*args):
        filepath = os.path.dirname(__file__)
        cmd_split = args[0].split()
        temp_size = 0

        if len(cmd_split) > 1:
            filename = cmd_split[1]
            self.clint.send(filename.encode("utf-8"))
            if not os.path.isfile(filename):
                server_reponse = self.clint.recv(1024).decode("utf-8")
                # 返回文件的大小
                # TODO
                if server_reponse == "200":
                    self.clint.send(filepath.encode("utf-8")) # 如果状态可发送，文件存在当前的文件夹
                    with open(os.path.join(filepath,filename),"wb") as fp:
                        pass
            else:
                print("%s 文件存在",filename)
        pass

    def help(self):
        return """
        cmd put filepath
        cmd dow filepath
        """

