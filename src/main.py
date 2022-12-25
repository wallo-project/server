from bleak import BleakScanner, BleakClient
import logging
import asyncio

logging.basicConfig(level=logging.INFO)


async def get_device():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == "MLT-BT05":
            return d

logging.basicConfig(level=logging.INFO)

class BluetoothClient:
    def __init__(self, device):
        self.__device = device
        self.client = None
        self.uid = '0000ffe1-0000-1000-8000-00805f9b34fb'

    async def connect(self):
        self.client = BleakClient(self.__device, loop=asyncio.get_event_loop())
        await self.client.connect()
        print("Connected to", self.__device.address)

    async def send(self, message):
        await self.client.write_gatt_char(self.uid, message.encode())
        print("Sent message:", message)

    async def receive(self):
        data = await self.client.read_gatt_char(self.uid)
        received_message = data.decode()
        print(received_message, end='')

async def main():
    device = await get_device()
    client = BluetoothClient(device)
    await client.connect()
    await client.send("Hello from Python!\n")
    await client.receive()

asyncio.run(main())

