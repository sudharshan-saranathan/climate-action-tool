# Filename: core/server.py
# Module Name: core.server
# Description: Backend server for the Climate Action Tool (CAT)

# Built-ins
import logging
import asyncio
import enum
# Dataclass
from dataclasses import dataclass

# Local imports
from core.server.parser import CommandParser
from core.graph import executable as graph_executable

# Configure logging
logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)8s - (%(module)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class ServerState(enum.Enum):
    RUNNING = "running"
    STOPPED = "stopped"


# Backend server for graph management and optimizations
class ClimactServer:

    # Singleton instance and logger
    _instance = None
    _logger = logging.getLogger(__name__)

    @dataclass
    class SocketConfig:
        host: str = "localhost"
        port: int = 6000

    # Interrupt instantiation to enforce the singleton pattern
    def __new__(cls, **kwargs):
        return cls._instance if cls._instance else super().__new__(cls)

    # Initialize server configuration and attributes
    def __init__(self, **kwargs):

        # Initialize server configuration
        self.config = self.SocketConfig(
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 6000),
        )

        # Initialize asyncio server
        self._status = ServerState.STOPPED
        self._server = None
        self._active = set()
        self._kill_event = asyncio.Event()

        # Initialize controllers
        self._init_controllers()
        self._init_command_parser()

        # Make this instance the singleton
        ClimactServer._instance = self

    # Initialize controllers
    def _init_controllers(self) -> None:
        self._controllers = {
            "server": self,
            "graph": graph_executable(),
            "optimizer": None,
        }

    # Initialize command parser
    def _init_command_parser(self) -> None:
        self._parser = CommandParser(self)

    # Wait for client connections and handle them
    async def _run_async(self) -> None:

        try:
            # Create asyncio server
            self._server = await asyncio.start_server(
                self._handle_client,
                self.config.host,
                self.config.port,
            )
            self._logger.info(
                f"Server listening on {self.config.host}:{self.config.port}"
            )

            # Wait for the kill-event
            async with self._server:
                await self._kill_event.wait()

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            await self.kill()

    # Start the server asynchronously
    def run(self) -> None:

        if self._status == ServerState.RUNNING:
            return

        # Start the server
        self._active = set()
        self._kill_event = asyncio.Event()
        self._status = ServerState.RUNNING

        asyncio.run(self._run_async())

    # Method to post a response as a JSON string
    async def respond(self, writer, response: dict) -> None:

        # Convert response to JSON string
        import json

        try:
            response = json.dumps(response, indent=4) + "\n"
            writer.write(response.encode())
            await writer.drain()

        except TypeError as e:
            self._logger.warning(f"Error converting response to JSON: {e}")

    # Method to kill the server and clean up resources asynchronously
    async def kill(self) -> None:

        # If the kill flag has already been set, do nothing
        if self._kill_event.is_set():
            return

        # Trigger the kill event to notify all active clients to disconnect
        self._kill_event.set()

        # Force close remaining client connections. This must be done before closing the server socket,
        # otherwise the `await self._server.wait_closed()` will hang indefinitely.
        for writer in self._active:
            writer.close()

        # Close the server socket to ignore new connection attempts
        if self._server:
            self._server.close()
            await self._server.wait_closed()

        self._status = ServerState.STOPPED
        self._logger.info("Server stopped")

    # Method to asynchronously handle a new client connection
    async def _handle_client(self, reader, writer):

        addr = writer.get_extra_info("peername")
        self._logger.info(f"Connection established with {addr[0]}")
        self._active.add(writer)

        try:
            writer.write(b"IITM-Climact Server v1.0\n")
            writer.write(b"Type 'help' for a list of commands\n")
            await writer.drain()

            # Check BOTH the event and if the writer is actually still open
            while not self._kill_event.is_set():

                try:
                    # Short timeout to check the 'kill_event' flag periodically
                    line = await asyncio.wait_for(reader.readuntil(b"\n"), timeout=1.0)
                    if not line:
                        break

                    response = await self._parser.parse(writer, line.strip())
                    await self.respond(writer, response)

                except asyncio.TimeoutError:
                    continue  # Just loop back and check kill_event

                except (ConnectionResetError, BrokenPipeError):
                    break  # Client left on their own

        except (asyncio.IncompleteReadError, ConnectionResetError, UnicodeDecodeError):
            self._logger.warning(f"Client {addr} disconnected")

        finally:
            self._active.discard(writer)
            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()

    @property
    def status(self) -> ServerState:
        return self._status

    @property
    def logger(self) -> logging.Logger:
        return self._logger
