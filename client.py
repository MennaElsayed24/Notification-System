import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:8765") as ws:
        print("Connected to server.")
        while True:
            email = input("Enter email (or leave empty to quit): ").strip()
            if not email:
                break
            await ws.send(email)
            reply = await ws.recv()
            print("Server>", reply)

if __name__ == "__main__":
    asyncio.run(main())


