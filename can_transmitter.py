import ctypes
import os
import platform

class CANTransmitter:
    def __init__(self):
        self.mock = False
        self.channel = 0
        self.handle = None

    def initialize(self, mock=False):
        self.mock = mock
        if self.mock:
            print("[CAN] Initialized (mock)")
            return True

        # Load Kvaser CANlib DLL
        if platform.system() == "Windows":
            dll_name = "canlib32.dll"
        else:
            raise RuntimeError("Only Windows is supported for Kvaser CANlib")

        self.canlib = ctypes.windll.LoadLibrary(dll_name)

        self.canlib.canInitializeLibrary()
        self.handle = self.canlib.canOpenChannel(self.channel, 0)
        if self.handle < 0:
            raise RuntimeError("Failed to open CAN channel")

        self.canlib.canSetBusParams(self.handle, 500000, 0, 0, 0, 0, 0)
        self.canlib.canBusOn(self.handle)
        print("[CAN] Initialized (real)")
        return True

    def send_emg(self, data):
        if self.mock:
            print(f"[CAN] EMG: {data['emg1']}, {data['emg2']}, ts={data['timestamp']}")
            return

        msg_id = 0x100
        emg1 = int(data['emg1']) & 0xFFFF
        emg2 = int(data['emg2']) & 0xFFFF
        ts = int(data['timestamp']) & 0xFFFFFFFF
        msg = (emg1.to_bytes(2, 'little') +
               emg2.to_bytes(2, 'little') +
               ts.to_bytes(4, 'little'))
        self._send(msg_id, msg)

    def send_heart_rate(self, data):
        if self.mock:
            print(f"[CAN] HR: {data['heart_rate']}, ts={data['timestamp']}")
            return

        msg_id = 0x101
        hr = int(data['heart_rate']) & 0xFF
        ts = int(data['timestamp']) & 0xFFFFFFFF
        msg = (hr.to_bytes(1, 'little') +
               ts.to_bytes(4, 'little') +
               bytes(3))
        self._send(msg_id, msg)

    def _send(self, msg_id, msg_bytes):
        msg_data = (ctypes.c_ubyte * 8)(*msg_bytes)
        self.canlib.canWrite(self.handle, msg_id, msg_data, 8, 0)
