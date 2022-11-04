import asyncio
import os
from tunnel import open_tunnel
from client_connector import ClientConnector

port = 7777

async def on_connect(ws):
    print("Socket connected")

async def main():
    tunnel = open_tunnel(port)
    print(tunnel + "/ui/client.htm")

    exit = asyncio.Event()
    ui_dir = os.path.join(os.getcwd(), "ui")
    connector = ClientConnector(port, exit, ui_dir, on_connect)
    await connector.run()

if __name__ == "__main__":
    asyncio.run(main())
