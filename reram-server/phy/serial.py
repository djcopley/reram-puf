import serial
from .phy import Phy


class Serial(Phy):
    def __init__(self, port: str, baudrate: int):
        super().__init__()
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.device.readline()

    def send(self):
        pass

    def receive(self) -> bytes:
        pass

    def close(self):
        pass
