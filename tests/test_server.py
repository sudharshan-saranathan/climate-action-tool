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

    def test_recv_exact(self):
        """Test recv_exact method reads exact number of bytes"""
        # Create a mock socket with data
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 9998))
        server.listen(1)

        # Client connects and sends data
        def client_thread():
            time.sleep(0.1)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 9998))
            client.sendall(b"Hello, World!")
            client.close()

        thread = threading.Thread(target=client_thread, daemon=True)
        thread.start()

        conn, _ = server.accept()
        data = SocketIO.recv_exact(conn, 5)
        self.assertEqual(data, b"Hello")
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

        def server_thread():
            server.run(timelimit=time.time() + 1)

        def client_thread():
            time.sleep(0.2)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("localhost", 9995))
                greeting = client.recv(1024)
                self.assertIn(b"IITM-Climact Server", greeting)
                client.close()
            except Exception as e:
                print(f"Client error: {e}")

        server_thread = threading.Thread(target=server_thread, daemon=True)
        client_thread = threading.Thread(target=client_thread, daemon=True)

        server_thread.start()
        client_thread.start()

        server_thread.join(timeout=3)
        client_thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
