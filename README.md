# CAN Transmitter Module for EMG and Heart Rate (Cometa Picoblue)

This Python module performs the following functions:

- Searches for and connects to Cometa's PicoBlue module  
- Acquires heart rate and EMG signals  
- Sends the measured information via CAN using a Kvaser USB CAN Pro device

## Installation

First, download the **PicoBlue SDK** from Cometa's official website.  
This SDK is a DLL library and can be called from any programming language.

👉 [Download SDK](https://www.cometasystems.com/picoblue/)  
You'll need to register to access Cometa’s Dropbox.

## How to Use

1. Place `PicoBlue.DaqSys.dll` in the same directory as the Python source code.  
2. Edit the serial number in `sensor_interface.py` to match your device.  
3. Connect the Kvaser CAN module to your PC, and run `main.py`.  
4. Use a CAN receiver or logging tool such as CANalyzer to receive the data.

## License

MIT
