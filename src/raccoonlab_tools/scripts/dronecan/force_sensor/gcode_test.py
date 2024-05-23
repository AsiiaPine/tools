"""
This is a simple script that attempts to connect to the GRBL controller at 
> /dev/tty.usbserial-A906L14X
It then reads the grbl_test.gcode and sends it to the controller

The script waits for the completion of the sent line of gcode before moving onto the next line

tested on
> MacOs Monterey arm64
> Python 3.9.5 | packaged by conda-forge | (default, Jun 19 2021, 00:24:55) 
[Clang 11.1.0 ] on darwin
> Vscode 1.62.3
> Openbuilds BlackBox GRBL controller
> GRBL 1.1

"""

import os
import numpy as np
import pandas as pd
import serial
import time
from threading import Event

# from collect_sample import TestGateOk


BAUD_RATE = 115200


def remove_comment(string):
    if string.find(";") == -1:
        return string
    else:
        return string[: string.index(";")]


def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()


def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input


def wait_for_movement_completion(ser, cleaned_line):

    Event().wait(1)

    if cleaned_line != "$X" or "$$":

        idle_counter = 0

        while True:
            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode("?" + "\n")
            ser.write(command)
            grbl_out = ser.readline()
            grbl_response = grbl_out.strip().decode("utf-8")

            if grbl_response != "ok":

                if grbl_response.find("Idle") > 0:
                    idle_counter += 1

            if idle_counter > 10:
                break
    return


def stream_gcode(GRBL_port_path, gcode_path, test_save_dir=""):
    # with contect opens file/connection and closes it if function(with) scope is left

    # test = TestGateOk()
    with serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        line = "G21\nG90\nG94\nG01 F300.00\n"
        command = str.encode(line + "\n")
        ser.write(command)  # Send g-code

        for z in np.linspace(0, 2.5, 100):
            line = f"G00 Z{z}"
            # cleaning up gcode from file
            cleaned_line = remove_eol_chars(remove_comment(line))
            if cleaned_line:  # checks if string is empty
                print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
                command = str.encode(line + "\n")
                ser.write(command)  # Send g-code

                wait_for_movement_completion(ser, cleaned_line)

                grbl_out = ser.readline()  # Wait for response with carriage return
                print(" : ", grbl_out.strip().decode("utf-8"))
                # test.get_force_measurement(n_mes=100, name=f"{z}.csv", dir=test_save_dir)

        for z in reversed(np.linspace(0, 2.5, 100)):
            line = f"G01 Z{z}"
            # cleaning up gcode from file
            cleaned_line = remove_eol_chars(remove_comment(line))
            if cleaned_line:  # checks if string is empty
                print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
                command = str.encode(line + "\n")
                ser.write(command)  # Send g-code

                wait_for_movement_completion(ser, cleaned_line)

                grbl_out = ser.readline()  # Wait for response with carriage return
                print(" : ", grbl_out.strip().decode("utf-8"))
                # test.get_force_measurement(n_mes=100, name=f"{z}.csv", dir=test_save_dir+"reverse_")
        print("End of gcode")


def get_force_measurement(self, n_mes: int = 100, name: str = "", dir=""):
    pmu = TestGateOk.pmu
    directory = os.path.dirname(os.path.realpath(__file__))

    save_dir = os.path.join(directory, dir)
    # TestGateOk.configure_node()
    result = []
    i = 0
    j = 0
    while i < n_mes or j < n_mes:
        try:

            # for i in range(n_mes):
            recv = pmu.recv_force()
            if recv.actuator_id == 1:
                i += 1
                print(f"got {i} msg {recv}")
            if recv.actuator_id == 0:
                j += 1
                print(f"got {j} msg {recv}")
            result.append(recv)
        except:
            continue
    results = []
    for i, res in enumerate(result):
        ptc = res.power_rating_pct
        force = res.force
        position = res.position
        id = res.actuator_id
        results.append(
            {
                "ptc": ptc,
                "force": force,
                "position": position,
                "actuator_id": id,
                "timestamp": time.time(),
            }
        )
    pd.DataFrame(results).to_csv(f"{save_dir}/{name}.csv", index=False)


if __name__ == "__main__":

    # GRBL_port_path = '/dev/tty.usbserial-A906L14X'
    GRBL_port_path = "/dev/ttyACM6"
    gcode_path = "grbl_test.gcode"

    print("USB Port: ", GRBL_port_path)
    print("Gcode file: ", gcode_path)
    stream_gcode(GRBL_port_path, gcode_path, test_save_dir="tests_data/new_sensor/0.0")

    print("EOF")
