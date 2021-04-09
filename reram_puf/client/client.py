import serial
import struct
import hashlib
import time

from reram_puf.common.string_manager import group_binary_string, convert_binary_to_plaintext


class Client:
    def __init__(self, port="COM4", baudrate=115200):
        self.device = serial.Serial(port=port, baudrate=baudrate)
        # self.device.readline()
        self.group_len = 2
        self.orders = None
        self.addresses = ["00", "01", "10", "11"]
        self.current_list = [400, 300, 200, 100]
        self.client_lut = {
            400: [4.84, 4.61, 4.33, 4.33], 
            300: [4.09, 4.07, 4.09, 4.07], 
            200: [3.84, 3.81, 3.83, 3.81], 
            100: [3.59, 3.54, 3.59, 3.54] }

    def close(self):
        """Close the current connection."""
        self.orders = None

    def handshake(self, passwd: str, salt: bytes):
        """Conduct handshake with server."""
        # Hash the password with the salt
        hashed_pw = self.sha_hash(passwd, salt)
        # Generate instructions
        self.orders = hashed_pw[:len(hashed_pw) // 2]
        self.orders = bin(int(self.orders, 16))[2:]
        self.orders = group_binary_string(self.orders, self.group_len)
        self.orders = [int(num, 2) for num in self.orders]
        print(f"ORDERS: {self.orders}")

    def get_voltage_lut(self):
        return str(self.client_lut)
        voltage_lut = {}
        for addr in self.addresses:
            voltage_lut[addr] = []
            for current in self.current_list:
                voltage_lut[addr].append(self.get_voltage_at_current(addr, current))
        return voltage_lut

    def get_voltage_at_current(self, address, current):
        puf_current = self.puf_instr(address, 5)
        return puf_current * ((5 * 252 / 255) / current)

    @staticmethod
    def sha_hash(password: str, salt: bytes) -> str:
        """
        Calculated SHA-256 hash

        :param password:
        :param salt:
        :return:
        """
        digest = hashlib.sha256()
        msg = bytes(password, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()

    def decrypt(self, cipher):
        binary_message = ""

        for index in range(0, len(cipher), 4):
            addr = self.get_next_address()
            byte_group = cipher[index:index + 4]
            voltage = struct.unpack("f", byte_group)[0]
            print(f"Sending voltage to PUF INSTR: {voltage}")
            current = self.puf_instr(addr, voltage)
            binary_group = self.current_lookup(current, self.group_len)
            binary_message += binary_group
            print(f"GROUP: {binary_group}")

        print(f"BINARY MSG: {binary_message}")
        plain_text = convert_binary_to_plaintext(binary_message)

        return plain_text

    def current_lookup(self, current, group_len: int) -> str:
        """Retrieve the binary code N given the current."""
        smallest_difference = abs(self.current_list[0] - current)
        code = format(0, f"0{group_len}b")

        for index, stored_current in list(enumerate(self.current_list))[1:]:
            if abs(current - stored_current) < smallest_difference:
                smallest_difference = abs(current - stored_current)
                code = format(index, f"0{group_len}b")

        return code

    def get_next_address(self):
        """Return the next address to use for lookup table as integer."""
        try:
            next_order = self.orders.pop(0)
            self.orders.append(next_order)
            addr = int(self.addresses[next_order], 2)
            return addr
        except IndexError:
            print(f"[ERROR]: Failed to fetch address. Bad addresses/orders.")

    def puf_instr(self, addr: int, voltage: float):
        """
        Issue and instruction to the PUF and read back the calculated current

        :param addr: ReRam cell address (0-3)
        :param voltage: Floating point voltage (0-5v)
        :return: Calculated current
        """
        msg = "0000" + bin(addr)[2:]
        voltage_bin = bin(round(voltage / 5.0 * 255))[2:]
        while len(voltage_bin) < 10:
            voltage_bin = '0' + voltage_bin
        msg += voltage_bin
        print(f"PUF INSTR MSG: {msg}")
        msg_bytes = f"<{msg}>".encode("utf-8")
        self.device.write(msg_bytes)
        print("Waiting for response...")
        time.sleep(0.5)
        read = self.device.read_all()
        out = read.decode("utf-8").split("\r\n")
        #print("Response: {}".format(out))
        out = read.decode("utf-8").split("\r\n")[0]
        out = round(float(out))
        print(f"output: {out}")
        return out
        # Conver voltage to 6bit voltage
        voltage = min(round(voltage * 64 / 5), 63) 
        self.device.write(((addr << 6) | voltage).to_bytes(1, "big"))
        res, = struct.unpack("f", self.device.read(4))
        #res = self.device.read()
        return int(res)


if __name__ == '__main__':
    # port = input("Enter port: ")
    client = Client()
    print(client.puf_instr(00, 3.1))
