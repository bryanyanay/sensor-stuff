import sys
import serial
import time

def calcChecksum(bytes):
  sum = 0
  for i in range(1, 8): # don't sum the start bit or the checksum bit
    sum += bytes[i]
  sum = (~sum & 0xFF) + 1
  return sum

"""
0-10 ppm = 0-10000 ppb

"""

def read_serial(port):
  try:
    ser = serial.Serial(port, timeout=0, baudrate=9600)
    print(f"Reading from {ser.name}...")
    while True:
      if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        # data = b'\xff*\x03\x01\x01\x90\x03\xe8V'
        hex_data = ' '.join([f'{byte:02X}' for byte in data])
        print(f"Received: {hex_data}")

        if len(data) == 9:
          sum = calcChecksum(data)
          print(f"Calculated checksum: {sum:02X}")
      
          print(f"Supposed ppm (ppb?) value: { data[4] * 256 + data[5]}") # multiply by 0.1??
          print(f"Supposed full range value: { data[6] * 256 + data[7]}") # multiply by 0.1??

        print()
      time.sleep(1)  

  except serial.SerialException as e:
    print(f"Serial port error: {e}")
  except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
  finally:
    if ser.is_open:
      ser.close()


if __name__ == '__main__':
  port = 'COM11'  # Specify your serial port here
  read_serial(port)
