import serial


class Client:
    def __init__(self, port: str):
        self.device = serial.Serial(port=port, baudrate=115200)
