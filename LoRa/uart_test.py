import serial
import time
import threading

# Configure serial port
port = "/dev/ttyUSB0"
baud_rate = 115200
ser = serial.Serial(port, baud_rate, timeout=1)

# clsoer channel number sent by ESP32 Serial
closer_to_channel = 0

# Check if the serial port is successfully opened
if ser.is_open:
    print(f"Serial port {port} is opened")
else:
    print("Failed to open serial port")
    exit()

# Flag to track if "Joined" has been received
joined_flag = False

# Function to read from serial port in a separate thread
def read_from_serial():
    # Initialize the global variables(especially for closer_to_channel)
    global joined_flag, closer_to_channel

    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"Received from ESP32: {data}")

                if data:
                    joined_flag = True

                # Extract channel and light status (if data matches the pattern)
                if "ch" in data and "light" in data:
                    parts = data.split(';')
                    channel_part = parts[0]  # "Closer to ch2"
                    light_part = parts[1]    # "light:1"

                    # Extract channel number (2)
                    channel = int(channel_part.replace('Closer to ch', '').strip())
                    
                    # Extract light status (1)
                    light = int(light_part.split(':')[1].strip())

                    print(f"Channel: {channel}, Light status: {light}")
                    closer_to_channel = channel  # Update global variable

        except Exception as e:
            print(f"Error reading from serial: {e}")
            break

# Start the serial reading thread
serial_thread = threading.Thread(target=read_from_serial, daemon=True)
serial_thread.start()

try:
    # Wait for "Joined" message before allowing user input
    while not joined_flag:
        time.sleep(0.1)  # Avoid busy-waiting by adding a small delay

    # Now that "Joined" is received, start accepting user input
    while True:
        # Wait for user input to send a message
        message = input("Enter a message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        # Send the message
        ser.write((message + '\n').encode('utf-8'))
        print(f"Sent: {message}")
        time.sleep(5)
        

except KeyboardInterrupt:
    print("\nProgram interrupted by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Ensure the serial port is closed
    ser.close()
    print("Serial port closed")