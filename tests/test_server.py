"""Test suite for core.server module with asyncio"""

import asyncio
import unittest

from core.server.server import ClimactServer


class TestClimactServer(unittest.TestCase):
    """Test ClimactServer with asyncio"""

    def test_server_singleton(self):
        """Test that ClimactServer enforces singleton pattern"""
        # Reset singleton
        ClimactServer._instance = None

        server1 = ClimactServer(port=9997)
        server2 = ClimactServer(port=9996)

        # Should be the same instance
        self.assertIs(server1, server2)

    def test_server_initialization(self):
        """Test server initializes with correct config"""
        ClimactServer._instance = None

        server = ClimactServer(host="127.0.0.1", port=9996)
        self.assertEqual(server.config.host, "127.0.0.1")
        self.assertEqual(server.config.port, 9996)

    def test_server_accepts_connection(self):
        """Test server can accept a client connection"""
        ClimactServer._instance = None

        server = ClimactServer(host="localhost", port=9995)

        async def run_test():
            """Run async test"""
            # Start server with timeout
            server_task = asyncio.create_task(
                asyncio.wait_for(server._run_async(), timeout=1.0)
            )

            # Give server time to bind
            await asyncio.sleep(0.1)

            try:
                # Connect as client
                reader, writer = await asyncio.open_connection("localhost", 9995)

                # Read greeting
                greeting = await reader.readuntil(b"\n")
                self.assertIn(b"IITM-Climact Server", greeting)

                # Send message
                writer.write(b"test message\n")
                await writer.drain()
                writer.close()
                await writer.wait_closed()

            except Exception as e:
                self.fail(f"Client error: {e}")
            finally:
                # Wait for server to finish (or timeout)
                try:
                    await server_task
                except asyncio.TimeoutError:
                    pass

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
