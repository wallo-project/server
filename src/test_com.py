import asyncio
import time
from bleak import BleakClient
from random import randint

async def main():
    arduino = BleakClient("C8:FD:19:66:E9:8F")
    await arduino.connect()
    while True:
        random = randint(0, 100)
        data = await arduino.read_gatt_char('0000ffe1-0000-1000-8000-00805f9b34fb')
        print(data)
        await arduino.write_gatt_char('0000ffe1-0000-1000-8000-00805f9b34fb', f"{random};{random}\n".encode("utf-8"))

asyncio.run(main())