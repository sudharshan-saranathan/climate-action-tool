#  Filename: core/server/parser.py
#  Module Name: core.server.parser
#  Description: Parser for incoming commands from clients

import enum


class CommandVocabulary(enum.Enum):
    help = "help"
    kill = "kill"
    status = "status"
    configure = "configure"
    disconnect = "disconnect"
    controllers = "controllers"


class CommandParser:

    def __init__(self, server):

        self._server = server

    async def parse(self, writer, data: bytes) -> dict[str, str]:

        raw_input = data.decode().strip()
        raw_parts = raw_input.split(" ", maxsplit=1)

        command = raw_parts[0] if len(raw_parts) > 0 else ""
        payload = raw_parts[1] if len(raw_parts) > 1 else ""

        # Resolve namespace
        if "." not in command:
            return {
                "status": "FAILED",
                "reason": "Invalid command format",
            }

        target, action = command.split(".", 1)
        return await self.execute(writer, target, action, payload)

    async def execute(self, writer, target, action, payload: str) -> dict:

        if target == "server":
            return await self._execute_server_command(action, payload)

        elif target in self._server._controllers:
            controller = self._server._controllers[target]
            if callable(controller):
                return await controller(action, payload)
            else:
                return {
                    "status": "FAILED",
                    "reason": f"Controller '{target}' is not initialized.",
                }

        else:
            return {
                "status": "FAILED",
                "reason": f"Target '{target}' not recognized. Type 'server.controllers' for available targets.",
            }

    async def _execute_server_command(self, action: str, payload: str) -> dict:
        """Execute server-specific commands."""

        if action == CommandVocabulary.kill.value:
            await self._server.kill()
            return {"status": "OK", "response": "Server stopped"}

        elif action == CommandVocabulary.status.value:
            return {"status": "OK", "response": self._server.status.value}

        elif action == CommandVocabulary.help.value:
            return {
                "status": "OK",
                "response": {
                    "server.help": "List available commands",
                    "server.kill": "Stop the server",
                    "server.status": "Return server status",
                    "server.configure": "Configure server options",
                    "server.disconnect": "Disconnect the client",
                    "server.controllers": "List available controllers",
                },
            }

        elif action == CommandVocabulary.controllers.value:
            return {
                "status": "OK",
                "response": {
                    "server": "Server management",
                    "graph": "Graph management",
                    "optimizer": "Optimization",
                },
            }

        else:
            self._server.logger.warning(f"Command '{action}' not recognized")
            return {
                "status": "FAILED",
                "reason": f"Command '{action}' not recognized",
            }
