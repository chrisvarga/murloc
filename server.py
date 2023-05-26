#!/usr/bin/env python3
#  A Python server model.

import os
import sys
import time
import json
import signal
import socket
import inspect
import subprocess


class Server:
    def __init__(
        self,
        version="1.0.0",
        host="127.0.0.1",
        port=8048,
        name="murloc",
        mode="default",
        url="https://github.com/",
    ):
        self.version = version
        self.host = host
        self.port = port
        self.name = name
        self.mode = mode
        self.url = url
        self.pid = os.getpid()
        self.boot = inspect.cleandoc(
            """\n
                    
                 ___
                /\  \ 
               /::\  \       %s %s
              /:/\:\  \ 
             /:/  \:\  \ 
            /:/__/ \:\__\    Running in %s mode
            \:\  \ /:/  /    Port: %-10s 
             \:\  /:/  /     PID:  %-10s 
              \:\/:/  / 
               \::/  /             %s
                \/__/ 
                    """
            % (
                self.name,
                self.version,
                self.mode,
                self.port,
                self.pid,
                self.url,
            )
        )

    def log(self, s, stdout=True):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        i = inspect.getframeinfo(inspect.stack()[1][0])
        msg = f"[{date}] [{i.filename}:{i.lineno}] [{os.getpid()}] {s}"
        if stdout:
            print(msg)
        else:
            try:
                with open(f"/var/tmp/{self.name}.log", "a") as f:
                    f.write(msg)
            except:
                print(msg)

    def is_ipv6(self, n):
        try:
            socket.inet_pton(socket.AF_INET6, n)
            return True
        except socket.error:
            return False

    def handle(self, route, args):
        method = getattr(self, route, None)
        if not callable(method) or method == None:
            return f"(error) method '{route}' is not defined"
        # return method(self.path.parent_op)
        return method(self, args)

    def parse(self, req):
        args = req.split(" ")
        route = args.pop(0)
        return self.handle(route, args)

    def recvall(self, conn):
        data = b""
        while True:
            packet = conn.recv(1024)
            data += packet
            if len(packet) < 1024:
                break
        return data

    def handle_connection(self, conn, addr):
        while True:
            try:
                data = self.recvall(conn)
            except:
                conn.close()
                break
            if not data:
                conn.close()
                break
            req = data.decode("utf-8").strip()
            res = self.parse(req) + "\n"
            conn.sendall(res.encode("utf-8"))

    def handle_sigint(self, sig, frame):
        print()
        sys.exit(0)

    def handle_sigchild(self, sig, frame):
        os.waitpid(-1, os.WNOHANG)

    def listen(self):
        self.log(self.boot)
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGCHLD, self.handle_sigchild)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen()
        self.log(f"Listening at {self.host}:{self.port}")
        while True:
            try:
                conn, addr = sock.accept()
                conn.settimeout(10)
                # Fork to handle the new connection; this allows us to use
                # os.system() etc, which is problematic within a thread.
                pid = os.fork()
                if pid == 0:
                    self.log(f"Connection from {addr}")
                    self.handle_connection(conn, addr)
                    sys.exit(0)
                else:
                    continue
            except:
                break


# Main
def set_value(self, args):
    print(self.name)
    return f"args={args}"


s = Server()
s.set = set_value
s.listen()
