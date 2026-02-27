# Filename: core/server/thread.py
# Module name: core.server.thread
# Description: Thread for running the async server (no Qt dependencies)

from __future__ import annotations

# Built-ins
import logging
import asyncio
import threading

# Climact Module(s): core.server.server
from core.server.server import ClimactServer


class ServerThread(threading.Thread):

    _logger = logging.getLogger("ServerThread")

    def __init__(self, host: str = "localhost", port: int = 6000):

        super().__init__(daemon=True)

        self._host = host
        self._port = port
        self._server: ClimactServer | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    def run(self) -> None:

        try:
            # Create a new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            self._server = ClimactServer(host=self._host, port=self._port)
            self._logger.info(f"Starting server on {self._host}:{self._port}")
            self._server.run()

        except Exception as e:
            self._logger.error(f"Server error: {e}")

        finally:
            if self._loop:
                self._loop.close()

    def stop(self) -> None:

        if self._server and self._loop:

            try:
                self._logger.info("Stopping server...")
                asyncio.run_coroutine_threadsafe(
                    self._server.kill(), self._loop
                ).result(timeout=5)

            except Exception as e:
                self._logger.error(f"Error stopping server: {e}")
