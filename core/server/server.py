# Filename: core/server.py
# Module Name: core.server
# Description: Backend server for the Climate Action Tool (CAT)


# Built-ins
import logging
import socket
import time

# Dataclass
from dataclasses import dataclass


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
    def __new__(cls):
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

    # Start listening to incoming connections
    def run(self, timelimit: int = -1) -> None:

        self._running = True
        self._logger.info(f"Server started on {self.config.host}:{self.config.port}")

        try:
            while self._running and (timelimit < 0 or time.time() < timelimit):
                connection = None
                address = None
                try:
                    connection, address = self._socket.accept()
                    connection.sendall(b"IITM-Climact Server v1.0 [License = GPL-3.0]")

                    # Receive and log the client's message
                    size = int(connection.recv(4))
                    data = self._socket.recv_exact(connection, size)
                    self._logger.info(f"Received message from {address}: {data}")

                except socket.timeout:
                    self._logger.debug("Socket timeout waiting for client connection")

                except UnicodeDecodeError as e:
                    self._logger.error(f"Failed to decode message from {address}: {e}")

                except Exception as e:
                    self._logger.error(f"Error handling client {address}: {e}")

                finally:
                    if connection:
                        connection.close()

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            self._socket.close()
            self._logger.info("Socket closed")

    def stop(self) -> None:
        self._running = False
        self._socket.close()
        self._logger.info("Server stopped")
