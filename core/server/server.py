# Filename: core/server.py
# Module Name: core.server
# Description: Backend server for the Climate Action Tool (CAT)

# Built-ins
import logging
import asyncio
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
        port: int = 6000

    class ServerState(enum.Enum):
        online = "online"
        killed = "killed"

    class CommandVocabulary(enum.Enum):
        help = "help"
        kill = "kill"
        status = "status"
        configure = "configure"
        disconnect = "disconnect"
        controllers = "controllers"

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

        # Define controllers
        self._controllers = {
            "graph": None,
            "optimizer": None,
        }

        self._asyncio_server = None
        self._kill_event = None
        self._clients = set()
        self._server_state = ClimactServer.ServerState.killed

        # Assign to the singleton
        ClimactServer._instance = self

    # Start listening and handle client connections
    async def _run_async(self) -> None:

        try:
            host = self.config.host
            port = self.config.port

            # Create asyncio server
            self._server = await asyncio.start_server(self._handle_client, host, port)
            self._logger.info(f"Server listening on {host}:{port}")

            # Wait for the kill-event
            async with self._server:
                await self._kill_event.wait()

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            await self._kill_async()

    # Kill the server
    async def _kill_async(self) -> None:

        # If already killed, do nothing
        if self._kill_event.is_set():
            return

        # Set the kill event
        self._kill_event.set()

        # Force close remaining client connections. This must be done before closing the server socket,
        # otherwise the `await self._server.wait_closed()` will hang indefinitely.
        for writer in self._clients:
            writer.close()

        # Close the server socket (stops accepting connections)
        if self._server:
            self._server.close()
            await self._server.wait_closed()

        self._server_state = ClimactServer.ServerState.killed
        self._logger.info("Server stopped")

    # Write a response to the client
    @staticmethod
    async def _write(writer, response: str, include_prompt: bool = True) -> None:

        formatted_response = f"{response}\n>> " if include_prompt else f"{response}\n"
        formatted_response = formatted_response.encode()

        writer.write(formatted_response)
        await writer.drain()

    async def _handle_client(self, reader, writer):

        addr = writer.get_extra_info("peername")
        self._logger.info(f"Connection established with {addr}")
        self._clients.add(writer)  # Track the writer

        try:
            await self._write(writer, "IITM-Climact Server v1.0", include_prompt=False)
            await self._write(writer, "Type 'help' for a list of commands\n")

            # Check BOTH the event and if the writer is actually still open
            while not self._kill_event.is_set():
                try:
                    # Short timeout so we check 'kill_event' frequently
                    line = await asyncio.wait_for(reader.readuntil(b"\n"), timeout=1.0)
                    if not line:
                        break

                    response = await self._handle_instructions(writer, line.strip())
                    await self._write(writer, response)

                except asyncio.TimeoutError:
                    continue  # Just loop back and check kill_event

                except (ConnectionResetError, BrokenPipeError):
                    break  # Client left on their own

        except (asyncio.IncompleteReadError, ConnectionResetError):
            self._logger.warning(f"Client {addr} disconnected")

        except UnicodeDecodeError:
            self._logger.warning(f"Client {addr} disconnected")

        finally:

            self._clients.discard(writer)
            # Check if writer is already closing/closed to avoid double-closing
            if not writer.is_closing():
                writer.close()
                try:
                    await writer.wait_closed()
                except:
                    pass

    # Parse incoming data from clients
    async def _handle_instructions(self, writer, data: bytes) -> str:

        raw_input = data.decode().strip()
        raw_parts = raw_input.split(" ", maxsplit=1)

        command = raw_parts[0] if len(raw_parts) > 0 else ""
        payload = raw_parts[1] if len(raw_parts) > 1 else ""

        # Resolve namespace
        if "." not in command:
            return f"Error: '{command}' must follow the pattern 'namespace.command'"

        target, action = command.split(".", 1)
        return await self._execute(writer, target, action, payload)

    # Execute the JSON command struct
    async def _execute(self, writer, target, action, payload: str) -> str:

        if target == "server":

            if action == ClimactServer.CommandVocabulary.kill.value:
                await self._kill_async()
                return "Server stopped"

            elif action == ClimactServer.CommandVocabulary.status.value:
                return self._server_state.value

            elif action == ClimactServer.CommandVocabulary.help.value:
                return "Available commands: kill, status, help"

            elif action == ClimactServer.CommandVocabulary.controllers.value:
                return "Available controllers: graph, optimizer"

            else:
                self._logger.warning(f"Unrecognized command: {action}")

        return "Message not recognized"

    def run(self) -> None:

        if self._server_state == ClimactServer.ServerState.online:
            return

        # Start the server
        self._clients = set()
        self._kill_event = asyncio.Event()
        self._server_state = ClimactServer.ServerState.online

        asyncio.run(self._run_async())
