#  Filename: sockio.py
#  Module name: core.server
#  Description: Socket I/O utilities for Climact.

import socket


class SocketIO(socket.socket):

    def __init__(self, *args, **kwargs):

        # Extract custom kwargs before passing to socket
        timeout = kwargs.pop("timeout", 60)
        host = kwargs.pop("host", None)
        port = kwargs.pop("port", None)
        backlog = kwargs.pop("backlog", 5)

        # Initialize socket with standard socket args
        super().__init__(*args, **kwargs)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.settimeout(timeout)

        if host and port:
            self.bind((host, port))
            self.listen(backlog)

    @staticmethod
    def recv_exact(connection: socket.socket, size: int) -> bytes:

        data = b""
        while len(data) < size:
            chunk = connection.recv(size - len(data))
            if not chunk:
                return b""
            data += chunk

        return data
