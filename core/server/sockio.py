#  Filename: sockio.py
#  Module name: core.server
#  Description: Socket I/O utilities for Climact.

import socket
import enum



class SocketIO(socket.socket):

    class SocketStatus(enum.IntFlag):
        active = 1
        paused = 2
        stopped = 4
        listening = 8
        busy = 16

    def __init__(self, *args, **kwargs):

        # Extract custom kwargs before passing to socket
        host = kwargs.pop("host", None)
        port = kwargs.pop("port", None)
        backlog = kwargs.pop("backlog", 5)
        timeout = kwargs.pop("timeout", 60)

        # Initialize the socket with standard socket args
        super().__init__(*args, **kwargs)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.settimeout(timeout)

        if host and port:
            self.bind((host, port))
            self.listen(backlog)

    @staticmethod
    def recv_line(connection: socket.socket, max_size: int = 33554432) -> bytes:
        """
        Read a line from the socket until a newline delimiter.

        Args:
            connection: The socket connection
            max_size: Maximum line size in bytes (default 32MB)

        Returns:
            Bytes up to (but not including) the newline character
        """

        data = b""
        while len(data) < max_size:
            chunk = connection.recv(4096)
            if not chunk:
                return data  # Connection closed
            data += chunk
            if b"\n" in data:
                return data.split(b"\n")[0]  # Return without the newline

        # Line exceeded max size
        raise OverflowError(f"Line exceeds max size of {max_size} bytes")

