#  Filename: sockio.py
#  Module name: core.server
#  Description: Socket I/O utilities for Climact.

import socket


class SocketIO(socket.socket):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.settimeout(kwargs.get("timeout", 60))

        host = kwargs.get("host", None)
        port = kwargs.get("port", None)
        if host and port:
            self.bind((host, port))
            self.listen(kwargs.get("backlog", 5))

    @staticmethod
    def recv_exact(connection: socket.socket, size: int) -> str:

        data = b""
        while len(data) < size:
            chunk = connection.recv(size - len(data))
            if not chunk:
                return ""
            data += chunk

        return data.decode()
