import serial
import time
import threading

port = "/dev/ttyUSB0"
baud_rate = 115200
ser = serial.Serial(port, baud_rate, timeout=1)

closer_to_channel = 0
joined_flag = False
light = 0

def read_from_serial():
    global joined_flag, closer_to_channel, light
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                # print(data)
                if data != "":
                    joined_flag = True
                if "ch" in data and "light" in data:
                    parts = data.split(';')
                    channel_part = parts[0]
                    light_part = parts[1]

                    # extract channel part
                    channel = int(channel_part.replace('Closer to ch', '').strip())

                    # extract light part
                    light = int(light_part.split(':')[1].strip())
                    
                    closer_to_channel = channel
        except Exception:
            break

def start_serial_thread():
    thread = threading.Thread(target=read_from_serial, daemon=True)
    thread.start()

def get_closer_to_channel():
    global closer_to_channel
    if closer_to_channel == 1:
        mapped = -1 # means left
    elif closer_to_channel == 2:
        mapped = 1 # means right
    elif closer_to_channel == 0:
        mapped = 0 # means center
    else:
        mapped = 5 # means error
    return mapped

def get_light_status():
    global light
    # print(light)
    return light

# Only run this if executed directly, not on import
if __name__ == "__main__":
    start_serial_thread()
    while not joined_flag:
        time.sleep(0.1)
    while True:
        message = input("Enter a message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        ser.write((message + '\n').encode('utf-8'))
        time.sleep(5)
    ser.close()