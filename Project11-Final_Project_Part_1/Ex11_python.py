import serial
import csv
import time

# -----------------------------
# Serial configuration
# -----------------------------
PORT = "COM4"      # Change to your Arduino COM port
BAUDRATE = 9600

# -----------------------------
# Open serial port
# -----------------------------
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)           # Wait for Arduino to reset
    print("Connected to Arduino.")
except Exception as e:
    print("Could not open serial port:", e)
    exit()

# -----------------------------
# Open CSV file
# -----------------------------
with open("log.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    # Header
    writer.writerow([
        "Time (ms)",
        "Servo Angle (deg)",
        "Buzzer"
    ])

    print("Logging started... Press Ctrl+C to stop.\n")

    try:

        while True:

            if ser.in_waiting:

                line = ser.readline().decode("utf-8").strip()

                if not line:
                    continue

                print(line)

                values = line.split(",")

                # Expect:
                # time,angle,buzzer
                if len(values) == 3:

                    writer.writerow(values)

                    # Save immediately
                    csvfile.flush()

    except KeyboardInterrupt:

        print("\nLogging stopped.")

# -----------------------------
# Cleanup
# -----------------------------
ser.close()