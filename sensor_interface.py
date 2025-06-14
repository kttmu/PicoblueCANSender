import time
import random
import threading

#try:
import clr  # pythonnet
clr.AddReference("PicoBlue.DaqSys") # Ensure DLL is in PYTHONPATH or same dir


import System
#for t in System.AppDomain.CurrentDomain.GetAssemblies():
#    #if "PicoBlue" in t.FullName:
#    for typ in t.GetTypes():
#        print(typ.FullName)
from PicoBlue.DaqSys import PicoBlueDaq
from PicoBlue.DaqSys import IPicoBlueDaq

from PicoBlue.DaqSys.EventArgs import DataAvailableEventArgs

from System import EventHandler
SDK_AVAILABLE = True
#except Exception:
#    SDK_AVAILABLE = False

class SensorInterfaceBase:
    def initialize(self):
        raise NotImplementedError

    def get_next_data(self):
        raise NotImplementedError

class MockSensorInterface(SensorInterfaceBase):
    def initialize(self):
        pass

    def get_next_data(self):
        return {
            'emg1': random.randint(-1000, 1000),
            'emg2': random.randint(-1000, 1000),
            'heart_rate': random.randint(60, 100),
            'timestamp': int(time.time() * 1e6)
        }

if SDK_AVAILABLE:
    class RealSensorInterface(SensorInterfaceBase):
        def __init__(self):
            self.lock = threading.Lock()
            self.latest_data = None
            self.daq = PicoBlueDaq()
            #self.idaq = IPicoBlueDaq()
            #self.daq.DataAvailable += EventHandler[DataAvailableEventArgs()](self.on_data)
            self.daq.DataAvailable += EventHandler[DataAvailableEventArgs](self.on_data)

            #handler = DataAvailableEventArgs()
            #self.daq.DataAvailable += handler


        def initialize(self):
            print(dir(PicoBlueDaq))  # どんなメソッドがあるか
            print(PicoBlueDaq.SearchSensor.__doc__)  # 期待される引数情報
            self.daq.SearchSensor(1)
            #if self.daq.Sensors.Count == 0:
            #    raise RuntimeError("No sensors found")
            self.daq.ConnectSensor(0)
            self.daq.StartCapturing()

        def on_data(self, sender, args):
            with self.lock:
                samples = args.Samples
                if samples.GetLength(0) >= 2:
                    emg1 = int(samples[0, 0])
                    emg2 = int(samples[1, 0])
                else:
                    emg1 = emg2 = 0
                self.latest_data = {
                    'emg1': emg1,
                    'emg2': emg2,
                    'heart_rate': random.randint(60, 100),  # Placeholder
                    'timestamp': int(time.time() * 1e6)
                }

        def get_next_data(self):
            with self.lock:
                return self.latest_data
else:
    RealSensorInterface = None
