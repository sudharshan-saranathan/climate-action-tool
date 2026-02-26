# Filename: core/server.py
# Module Name: core.server
# Description: Backend server for the Climate Action Tool (CAT)


# Built-ins
import logging
import socket
import time
import json
import enum

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

    class ServerState(enum.Enum):
        running = "running"
        stopped = "stopped"

    class CommandVocabulary(enum.Enum):
        help = "help"
        shutdown = "shutdown"

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
        self._status = ClimactServer.ServerState.stopped
        self._active = {}

        # Initialize a target dictionary
        self._targets = {
            "graph": None,
            "optimizer": None,
        }


        # Assign to the singleton
        ClimactServer._instance = self

    # Initialize a socket and bind to the address
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

        self._status = ClimactServer.ServerState.running
        self._logger.info(f"Server started on {self.config.host}:{self.config.port}")

        try:
            while self._status == ClimactServer.ServerState.running:

                conn = None
                addr = None
                try:
                    conn, addr = self._socket.accept()
                    conn.sendall(b"IITM-Climact Server v1.0 [GPL-3.0]\n")

                    self._logger.info(f"New connection from {addr}")
                    self._active[conn] = addr

                    # Handle multiple messages from the same client
                    while self._status == ClimactServer.ServerState.running:

                        data = self._socket.recv_line(conn)
                        if not data:  # Connection closed by client
                            break

                        self._parse(data)

                except socket.timeout:
                    self._logger.debug("Socket timeout waiting for client connection")

                except UnicodeDecodeError as e:
                    self._logger.error(f"Failed to decode command from {addr}: {e}")

                except Exception as e:
                    self._logger.error(f"Error handling client {addr}: {e}")

                finally:
                    if conn:
                        conn.close()

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            if self._status == ClimactServer.ServerState.running:
                self.shutdown()

    # Register a new target
    def register_target(self, target: str, instantiator) -> None:

        if target in self._targets:
            self._logger.warning(f"Target {target} already exists")
            return

        self._targets[target] = instantiator()

    # Stop the server
    def shutdown(self) -> None:

        self._logger.info(f"Shutting down server")

        # Close all active connections
        for conn, addr in self._active.items():
            if conn:
                conn.close()

            self._logger.info(f"\t- Connection with {addr} closed")

        self._status = ClimactServer.ServerState.stopped
        self._active.clear()
        self._socket.close()

    # Parse incoming data from clients
    def _parse(self, data: bytes) -> None:

        try:
            jstr = json.loads(data.decode())
            target = jstr.get("target", None)
            command = jstr.get("action", None)
            payload = jstr.get("payload", "")

            self._execute(target, command, payload)
            self._logger.info(f"JSON data: {jstr}")

        except json.JSONDecodeError as e:
            self._handle_direct_command(data.decode())
            return

    def _execute(self, target: str, action: str, payload: str = "") -> None:
        pass

    def _handle_direct_command(self, command: str) -> None:

        if not isinstance(command, str):
            self._logger.error(f"Invalid command: {command}")
            return

        if command.strip() == self.CommandVocabulary.shutdown.value:
            self.shutdown()

        else:
            self._logger.warning(f"Unknown command: {command}")