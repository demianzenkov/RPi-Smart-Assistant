import serial
import pynmea2
import time
import sys
import os

modules_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(modules_dir)

from globals import set_longitude, get_longitude, set_latitude, get_latitude

# Replace with the correct serial port and baud rate for your GPS module
# serial_port = "/dev/ttyUSB0"
serial_port = "/dev/ttyS3"
baud_rate = 9600


def read_gps_data(events):
    # Open the serial port
    last_latitude = -1
    last_longitude = -1
    
    nmea_gga_counter = 0;

    attempt_counter = 0
    MAX_SERIAL_ATTEMPTS = 5

    while True:
        try:
            with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
                while True:
                    try:
                        line = ser.readline().decode('ascii', errors='replace').strip()

                        # Attempt to parse the NMEA sentence
                        if line.startswith("$"):
                            msg = pynmea2.parse(line)

                            # Check if the message is a GGA type (Global Positioning System Fix Data)
                            if isinstance(msg, pynmea2.types.talker.GGA):
                                nmea_gga_counter += 1
                                latitude = msg.latitude
                                longitude = msg.longitude

                                if last_latitude != latitude and last_longitude != longitude:
                                    set_latitude(latitude)
                                    set_longitude(longitude)

                                    last_latitude = latitude
                                    last_longitude = longitude
                                    if not (nmea_gga_counter % 10):
                                        print(f"Latitude: {latitude}, Longitude: {longitude}")

                    except pynmea2.ParseError as e:
                        # Handle parse errors (e.g., for incomplete or corrupted data)
                        print(f"Parse error: {e}")
                    except UnicodeDecodeError as e:
                        # Handle character decoding errors
                        print(f"Decode error: {e}")
        except FileNotFoundError:
            print(f"Serial port {serial_port} not found. Please check the connection.")
            time.sleep(1)
        except serial.SerialException as e:
            attempt_counter += 1
            if attempt_counter > MAX_SERIAL_ATTEMPTS:
                break
            time.sleep(1)
            print(f"Serial error: {e}")


