import argparse
import time
from sensor_interface import MockSensorInterface, RealSensorInterface
from can_transmitter import CANTransmitter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    args = parser.parse_args()

    if args.mock or RealSensorInterface is None:
        print("Running in MOCK mode.")
        sensor = MockSensorInterface()
        mock_mode = True
    else:
        print("Running in REAL mode.")
        sensor = RealSensorInterface()
        mock_mode = False

    sensor.initialize()
    can = CANTransmitter()
    can.initialize(mock=mock_mode)

    while True:
        data = sensor.get_next_data()
        if data:
            can.send_emg(data)
            can.send_heart_rate(data)
        time.sleep(0.0005)  # 2000Hz = 0.5ms

if __name__ == "__main__":
    main()
