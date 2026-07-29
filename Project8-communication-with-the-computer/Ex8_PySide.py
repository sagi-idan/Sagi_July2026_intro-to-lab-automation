import FreeSimpleGUI as sg
import serial
import threading
import time

# ----------------------------------------------------
# Serial Configuration
# ----------------------------------------------------
PORT = "COM4"          # Change to your Arduino port
BAUDRATE = 9600

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
    time.sleep(2)      # Wait for Arduino reset
except Exception as e:
    sg.popup_error(f"Could not open serial port:\n{e}")
    raise

# ----------------------------------------------------
# GUI Layout
# ----------------------------------------------------
layout = [
    [sg.Text("LED Time (ms):"),
     sg.Input(size=(12,1), key="-TIME-"),
     sg.Button("Send")],

    [sg.Text("Arduino Status:")],

    [sg.Multiline(size=(50,12),
                  key="-OUTPUT-",
                  autoscroll=True,
                  disabled=True)]
]

window = sg.Window("Arduino Serial Communication", layout)

# ----------------------------------------------------
# Thread Control
# ----------------------------------------------------
running = True

# ----------------------------------------------------
# Background thread
# Reads messages from Arduino continuously
# ----------------------------------------------------
def serial_reader():

    while running:

        try:
            if ser.in_waiting:

                message = ser.readline().decode().strip()

                if message == "0":
                    text = "LED OFF"

                elif message == "1":
                    text = "Button pressed - LED ON"

                elif message == "2":
                    text = "Button released"

                else:
                    text = "Arduino: " + message

                # Send event safely to GUI thread
                window.write_event_value("-SERIAL-", text)

        except Exception as e:
            window.write_event_value("-SERIAL-",
                                     f"Serial Error: {e}")

        time.sleep(0.01)


# Start background thread
thread = threading.Thread(target=serial_reader,
                          daemon=True)
thread.start()

# ----------------------------------------------------
# GUI Event Loop
# ----------------------------------------------------
while True:

    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED:
        break

    # ----------------------------------------------
    # Send button
    # ----------------------------------------------
    if event == "Send":

        try:
            led_time = int(values["-TIME-"])

            if led_time < 0:
                raise ValueError

            # Send number with newline
            ser.write(f"{led_time}\n".encode())

            window["-OUTPUT-"].update(
                f"Sent: {led_time} ms\n",
                append=True
            )

        except ValueError:
            window["-OUTPUT-"].update(
                "Please enter a valid positive integer.\n",
                append=True
            )

        except Exception as e:
            window["-OUTPUT-"].update(
                f"Send Error: {e}\n",
                append=True
            )

    # ----------------------------------------------
    # Message from Arduino
    # ----------------------------------------------
    elif event == "-SERIAL-":

        window["-OUTPUT-"].update(
            values["-SERIAL-"] + "\n",
            append=True
        )

# ----------------------------------------------------
# Cleanup
# ----------------------------------------------------
running = False
thread.join(timeout=1)

ser.close()
window.close()