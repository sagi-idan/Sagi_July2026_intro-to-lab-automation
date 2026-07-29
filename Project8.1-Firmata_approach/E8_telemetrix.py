import FreeSimpleGUI as sg
from telemetrix import telemetrix
from threading import Timer

# -----------------------------
# Pin definitions
# -----------------------------
BUTTON_PIN = 2
LED_PIN = 4

# Default LED on-time (seconds)
led_time = 2.0

# Connect to Arduino
board = telemetrix.Telemetrix()

# Keep track of active timer
led_timer = None


# -----------------------------
# Turn LED off
# -----------------------------
def turn_led_off():
    board.digital_write(LED_PIN, 0)
    window.write_event_value("-LOG-", "LED OFF")


# -----------------------------
# Button callback
# -----------------------------
def button_callback(data):

    global led_timer

    value = data[2]

    # Normal input
    if value == 1:          # Button pressed

        board.digital_write(LED_PIN, 1)

        window.write_event_value("-BUTTON-", "Pressed")
        window.write_event_value("-LOG-", "Button pressed -> LED ON")

        if led_timer is not None:
            led_timer.cancel()

        led_timer = Timer(led_time, turn_led_off)
        led_timer.start()

    else:                   # Button released

        window.write_event_value("-BUTTON-", "Released")

# -----------------------------
# Configure pins
# -----------------------------
board.set_pin_mode_digital_output(LED_PIN)

board.set_pin_mode_digital_input(
    BUTTON_PIN,
    callback=button_callback
)


# -----------------------------
# GUI
# -----------------------------
layout = [

    [sg.Text("LED ON Time (seconds):"),
     sg.Input("2", size=(8, 1), key="-TIME-"),
     sg.Button("Set")],

    [sg.Text("Button State:"),
     sg.Text("Released", key="-STATE-")],

    [sg.Multiline(size=(50, 10),
                  key="-OUTPUT-",
                  disabled=True,
                  autoscroll=True)]
]

window = sg.Window(
    "Telemetrix Button Demo",
    layout,
    finalize=True
)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED:
        break

    elif event == "Set":

        try:
            t = float(values["-TIME-"])

            if t <= 0:
                raise ValueError

            led_time = t

            window["-OUTPUT-"].update(
                f"LED time set to {led_time} s\n",
                append=True
            )

        except ValueError:

            window["-OUTPUT-"].update(
                "Enter a positive number.\n",
                append=True
            )

    elif event == "-BUTTON-":

        window["-STATE-"].update(values["-BUTTON-"])

    elif event == "-LOG-":

        window["-OUTPUT-"].update(
            values["-LOG-"] + "\n",
            append=True
        )

# -----------------------------
# Cleanup
# -----------------------------
if led_timer is not None:
    led_timer.cancel()

board.shutdown()

window.close()