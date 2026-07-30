import serial
import csv
import time
import threading
import math

import FreeSimpleGUI as sg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# -----------------------------
# Serial settings
# -----------------------------

PORT = "COM4"        # Change to your Arduino port
BAUDRATE = 9600


# -----------------------------
# Data storage
# -----------------------------

times = []
angles = []

current_angle = 65
buzzer_on = False

running = True


# -----------------------------
# CSV file
# -----------------------------

csv_file = open(
    "fan_log.csv",
    "w",
    newline=""
)

writer = csv.writer(csv_file)

writer.writerow(
    [
        "Time(ms)",
        "Angle(deg)",
        "Buzzer"
    ]
)



# -----------------------------
# Serial reader thread
# -----------------------------

def serial_reader():

    global current_angle
    global buzzer_on

    try:

        ser = serial.Serial(
            PORT,
            BAUDRATE,
            timeout=1
        )

        time.sleep(2)

        print("Arduino connected")


        while running:

            if ser.in_waiting:

                line = (
                    ser.readline()
                    .decode()
                    .strip()
                )


                values = line.split(",")


                if len(values) == 3:

                    t = int(values[0])
                    angle = int(values[1])
                    buzz = values[2]


                    current_angle = angle
                    buzzer_on = (
                        buzz == "ON"
                    )


                    times.append(t)
                    angles.append(angle)


                    # keep graph small
                    if len(times) > 100:
                        times.pop(0)
                        angles.pop(0)


                    writer.writerow(
                        [
                            t,
                            angle,
                            buzz
                        ]
                    )

                    csv_file.flush()


        ser.close()


    except Exception as e:

        print(
            "Serial error:",
            e
        )



# Start background reading
threading.Thread(
    target=serial_reader,
    daemon=True
).start()



# -----------------------------
# Matplotlib graph
# -----------------------------

fig, ax = plt.subplots(
    figsize=(5,3)
)

line, = ax.plot(
    [],
    [],
    "b-"
)

ax.set_ylim(
    30,
    100
)

ax.set_ylabel(
    "Servo Angle"
)

ax.set_xlabel(
    "Time"
)

ax.grid()



def draw_graph(canvas):

    figure_canvas = (
        FigureCanvasTkAgg(
            fig,
            canvas
        )
    )

    figure_canvas.draw()

    figure_canvas.get_tk_widget().pack(
        side="top",
        fill="both",
        expand=1
    )

    return figure_canvas



# -----------------------------
# GUI layout
# -----------------------------

layout = [

    [
        sg.Text(
            "Fan Angle Control",
            font=("Arial",18)
        )
    ],


    [
        sg.Canvas(
            key="-GRAPH-",
            size=(500,300)
        )
    ],


    [
        sg.Text(
            "Angle:"
        ),

        sg.Text(
            "65",
            key="-ANGLE-",
            font=("Arial",16)
        )
    ],


    [
        sg.Text(
            "Buzzer:"
        ),

        sg.Text(
            "●",
            key="-BUZZER-",
            text_color="green",
            font=("Arial",30)
        )
    ],


    [
        sg.Text(
            "Compass"
        )
    ],


    [
        sg.Text(
            "",
            key="-COMPASS-",
            font=("Arial",20)
        )
    ],


    [
        sg.Button("Exit")
    ]

]



window = sg.Window(
    "Grove Fan Monitor",
    layout,
    finalize=True
)



# Add graph

fig_canvas = draw_graph(
    window["-GRAPH-"].TKCanvas
)



# -----------------------------
# GUI loop
# -----------------------------

while True:


    event, values = window.read(
        timeout=100
    )


    if event == sg.WIN_CLOSED or event=="Exit":
        break



    # Update graph

    line.set_data(
        times,
        angles
    )


    if len(times)>1:

        ax.set_xlim(
            times[0],
            times[-1]+100
        )


    fig_canvas.draw()



    # Angle text

    window["-ANGLE-"].update(
        str(current_angle)
    )



    # Buzzer LED

    if buzzer_on:

        window["-BUZZER-"].update(
            "●",
            text_color="red"
        )

    else:

        window["-BUZZER-"].update(
            "●",
            text_color="green"
        )



    # Compass display

    if current_angle < 50:

        direction = "LEFT"

    elif current_angle > 80:

        direction = "RIGHT"

    else:

        direction = "CENTER"


    window["-COMPASS-"].update(
        f"{direction}  ({current_angle}°)"
    )



# -----------------------------
# Cleanup
# -----------------------------

running = False

csv_file.close()

window.close()