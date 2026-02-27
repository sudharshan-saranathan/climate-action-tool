# Filename: gui/client/climact.py
# Module name: gui.client.climact
# Description: Client for communicating with the Climate Action Tool server

from __future__ import annotations

import logging
import json
import asyncio
from typing import Optional, Any


class ClimactClient:

    def __init__(self, host: str = "localhost", port: int = 6000):
        """Initialize the graph client with server connection details."""
        self._host = host
        self._port = port
        self._logger = logging.getLogger("ClimactClient")
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._guid: Optional[str] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    @staticmethod
    def _run_async(coro) -> Any:
        """
        Helper to run async code from sync context.
        Creates or reuses event loop.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)

    def connect(self, guid: str) -> bool:
        """
        Connect to the server and initialize with a graph GUID.

        Args:
            guid: The unique identifier for the graph

        Returns:
            True if connection successful, False otherwise
        """
        self._guid = guid
        try:
            self._run_async(self._connect_async())
            self._logger.info(f"Connected to server at {self._host}:{self._port}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to connect to server: {e}")
            return False

    async def _connect_async(self) -> None:
        """Establish async connection to server."""
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port
        )

    def disconnect(self) -> None:
        """Disconnect from the server."""
        if self._writer:
            self._run_async(self._disconnect_async())

    async def _disconnect_async(self) -> None:
        """Close async connection."""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

    async def _send_command_async(
        self, target: str, action: str, payload: dict
    ) -> dict:
        """
        Send a command to the server and wait for response.

        Args:
            target: Command target (e.g., "graph")
            action: Command action (e.g., "create_node")
            payload: Command payload as dict

        Returns:
            Server response as dict
        """
        if not self._writer:
            raise RuntimeError("Not connected to server")

        # Prepare command
        command = f"{target}.{action}"
        payload_str = json.dumps(payload)
        request = f"{command} {payload_str}\n".encode()

        # Send command
        self._writer.write(request)
        await self._writer.drain()

        # Wait for response
        response = await self._read_response()
        return response

    async def _read_response(self) -> dict:
        """Read and parse a JSON response from the server."""
        if not self._reader:
            raise RuntimeError("Not connected to server")

        line = await self._reader.readuntil(b"\n")
        response = json.loads(line.decode().strip())
        return response

    def send_command(self, target: str, action: str, payload: dict) -> dict:
        """
        Synchronous wrapper for sending commands.

        Args:
            target: Command target (e.g., "graph")
            action: Command action (e.g., "create_node")
            payload: Command payload as dict

        Returns:
            Server response as dict
        """
        try:
            return self._run_async(self._send_command_async(target, action, payload))
        except Exception as e:
            self._logger.error(f"Error sending command {target}.{action}: {e}")
            return {
                "status": "FAILED",
                "reason": str(e),
            }

    # Graph-specific commands

    def create_node(self, data: dict) -> Optional[str]:
        """
        Create a node in the graph.

        Args:
            data: Node data (name, x, y, etc.)

        Returns:
            Node UID if successful, None otherwise
        """
        payload = {
            "guid": self._guid,
            "data": data,
        }
        response = self.send_command("graph", "create_node", payload)

        if response.get("status") == "OK":
            return response.get("response", {}).get("nuid")
        else:
            self._logger.warning(f"Failed to create node: {response.get('reason')}")
            return None

    def create_edge(self, source_uid: str, target_uid: str) -> Optional[str]:
        """
        Create an edge between two nodes.

        Args:
            source_uid: UID of source node
            target_uid: UID of target node

        Returns:
            Edge UID if successful, None otherwise
        """
        payload = {
            "guid": self._guid,
            "data": {
                "source_uid": source_uid,
                "target_uid": target_uid,
            },
        }
        response = self.send_command("graph", "create_edge", payload)

        if response.get("status") == "OK":
            return response.get("response", {}).get("euid")
        else:
            self._logger.warning(f"Failed to create edge: {response.get('reason')}")
            return None

    def get_node(self, nuid: str) -> Optional[dict]:
        """
        Get node data from the server.

        Args:
            nuid: Node UID

        Returns:
            Node data if successful, None otherwise
        """
        payload = {
            "guid": self._guid,
            "nuid": nuid,
        }
        response = self.send_command("graph", "get_node", payload)

        if response.get("status") == "OK":
            return response.get("response")
        else:
            self._logger.warning(f"Failed to get node: {response.get('reason')}")
            return None

    def get_edge(self, euid: str) -> Optional[dict]:
        """
        Get edge data from the server.

        Args:
            euid: Edge UID

        Returns:
            Edge data if successful, None otherwise
        """
        payload = {
            "guid": self._guid,
            "euid": euid,
        }
        response = self.send_command("graph", "get_edge", payload)

        if response.get("status") == "OK":
            return response.get("response")
        else:
            self._logger.warning(f"Failed to get edge: {response.get('reason')}")
            return None

    def update_node(self, nuid: str, data: dict) -> bool:
        """
        Update node data on the server.

        Args:
            nuid: Node UID
            data: Fields to update (meta, tech, etc.)

        Returns:
            True if successful, False otherwise
        """
        payload = {
            "guid": self._guid,
            "nuid": nuid,
            "data": data,
        }
        response = self.send_command("graph", "update_node", payload)

        if response.get("status") == "OK":
            return True
        else:
            self._logger.warning(f"Failed to update node: {response.get('reason')}")
            return False
