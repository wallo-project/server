from serial.tools import list_ports

com: str = ""

for port in list_ports.comports():
    if "arduino" in port.__str__().lower():
        com = port.device
        break

if com == '':
    print("Arduino not found")
else:
    print(com)