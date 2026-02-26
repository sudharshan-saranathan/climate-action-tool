# Filename: core/server.py
# Module Name: core.server
# Description: Backend server for the Climate Action Tool (CAT)


# Built-ins
from datetime import time
import logging
import socket
import time

# Dataclass
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] - (%(module)s) %(message)s",
)


# Backend server for graph management and optimizations
class ClimactServer:

    # Singleton instance and logger
    _instance = None
    _logger = logging.getLogger(__name__)

    @dataclass
    class SocketConfig:
        host: str = "localhost"
        port: int = 8080
        timeout: int = 60
        backlog: int = 5

    # Interrupt instantiation to enforce the singleton pattern
    def __new__(cls, **kwargs):
        return cls._instance if cls._instance else super().__new__(cls)

    # Initialize server configuration and socket attributes
    def __init__(self, **kwargs):

        # Initialize server configuration
        self.config = self.SocketConfig(
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 8080),
            timeout=kwargs.get("timeout", 60),
            backlog=kwargs.get("backlog", 5),
        )

        self._init_socket()
        self._running = False
        self._runtime = 0
        self._timestamp = None

        # Assign to the singleton
        ClimactServer._instance = self

    # Initialize socket and bind to the address
    def _init_socket(self) -> None:

        # Import custom socket
        from core.server.sockio import SocketIO

        # Create and configure the socket
        self._socket = SocketIO(
            socket.AF_INET,
            socket.SOCK_STREAM,
            timeout=self.config.timeout,
            host=self.config.host,
            port=self.config.port,
            backlog=self.config.backlog,
        )

    # Start listening and handle client connections
    def run(self) -> None:

        self._running = True
        self._timestamp = time.time()
        self._logger.info(f"Server started on {self.config.host}:{self.config.port}")

        try:
            while self._running:
                conn = None
                addr = None
                try:
                    conn, addr = self._socket.accept()
                    conn.sendall(b"IITM-Climact Server v1.0 [GPL-3.0]\n")
                    self._logger.info(f"New connection from {addr}")

                    # Handle multiple messages from the same client
                    while True:

                        data = self._socket.recv_line(conn)
                        if not data:  # Connection closed by client
                            break

                        if data.decode().strip().lower() in ["exit", "quit"]:
                            self._logger.info(f"Client {addr} requested disconnect")
                            break

                        self._logger.info(f"Command from {addr}: {data.decode()}")

                except socket.timeout:
                    self._logger.debug("Socket timeout waiting for client connection")

                except UnicodeDecodeError as e:
                    self._logger.error(f"Failed to decode command from {addr}: {e}")

                except Exception as e:
                    self._logger.error(f"Error handling client {addr}: {e}")

                finally:
                    if conn:
                        conn.close()
                        self._logger.info(f"Connection closed: {addr}")

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            self._socket.close()
            self._logger.info("Socket closed")

    def stop(self) -> None:
        self._running = False
        self._socket.close()
        self._logger.info("Server stopped")

    def _fetch_command(self, data: bytes) -> str:

        # Parse command as json
        import json

        try:
            return json.loads(data.decode())

        except json.JSONDecodeError as e:
            self._logger.error(f"Failed to decode command: {data.decode()}")
            return ""
