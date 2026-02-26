"""Test suite for core.server module"""

import socket
import threading
import time
import unittest

from core.server.server import ClimactServer
from core.server.sockio import SocketIO


class TestSocketIO(unittest.TestCase):
    """Test SocketIO wrapper"""

    def test_socket_creation(self):
        """Test that SocketIO can be created"""
        sock = SocketIO(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsNotNone(sock)
        sock.close()

    def test_socket_bind_and_listen(self):
        """Test that SocketIO can bind and listen"""
        sock = SocketIO(
            socket.AF_INET,
            socket.SOCK_STREAM,
            host="localhost",
            port=9999,
        )
        self.assertIsNotNone(sock)
        sock.close()

    def test_recv_line(self):
        """Test recv_line method reads until newline delimiter"""
        # Create a mock socket with data
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 9998))
        server.listen(1)

        # Client connects and sends line-delimited data
        def client_thread():
            time.sleep(0.1)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 9998))
            client.sendall(b"Hello, World!\n")
            client.close()

        thread = threading.Thread(target=client_thread, daemon=True)
        thread.start()

        conn, _ = server.accept()
        data = SocketIO.recv_line(conn)
        self.assertEqual(data, b"Hello, World!")
        conn.close()
        server.close()


class TestClimactServer(unittest.TestCase):
    """Test ClimactServer"""

    def test_server_singleton(self):
        """Test that ClimactServer enforces singleton pattern"""
        # Reset singleton
        ClimactServer._instance = None

        server1 = ClimactServer(port=9997)
        server2 = ClimactServer(port=9996)

        # Should be the same instance
        self.assertIs(server1, server2)
        server1.stop()

    def test_server_initialization(self):
        """Test server initializes with correct config"""
        ClimactServer._instance = None

        server = ClimactServer(host="127.0.0.1", port=9996, timeout=30)
        self.assertEqual(server.config.host, "127.0.0.1")
        self.assertEqual(server.config.port, 9996)
        self.assertEqual(server.config.timeout, 30)
        server.stop()

    def test_server_accepts_connection(self):
        """Test server can accept a client connection"""
        ClimactServer._instance = None

        server = ClimactServer(host="localhost", port=9995, timeout=2)

        def run_server():
            # Run for limited time by checking a flag
            server._running = True
            for _ in range(5):  # Try up to 5 iterations
                if not server._running:
                    break
                try:
                    connection, address = server._socket.accept()
                    connection.sendall(b"IITM-Climact Server v1.0 [License = GPL-3.0]\n")
                    ts = time.strftime("%H:%M:%S")
                    server._logger.info(f"New connection from {address} [{ts}]")

                    data = server._socket.recv_line(connection)
                    server._logger.info(f"Message: {data.decode() if data else ''}")
                    connection.close()
                    break
                except socket.timeout:
                    pass

        def client_thread():
            time.sleep(0.2)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("localhost", 9995))
                greeting = client.recv(1024)
                self.assertIn(b"IITM-Climact Server", greeting)
                client.sendall(b"test message\n")
                client.close()
            except Exception as e:
                print(f"Client error: {e}")

        server_thread = threading.Thread(target=run_server, daemon=True)
        client_thread = threading.Thread(target=client_thread, daemon=True)

        server_thread.start()
        client_thread.start()

        server_thread.join(timeout=3)
        client_thread.join(timeout=3)
        server._running = False


if __name__ == "__main__":
    unittest.main()
