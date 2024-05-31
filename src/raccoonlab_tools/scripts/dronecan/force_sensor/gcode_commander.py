import os
import socket
import threading
import time

import numpy as np
import pandas as pd
import serial
import sys
from collect_sample import TestGateOk


BAUD_RATE = 115200
host = "100.76.146.35"
port = 12345


def remove_comment(string):
    if string.find(";") == -1:
        return string
    else:
        return string[: string.index(";")]


def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()
def receive_message_and_call_function():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 8
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            
            try:
                while i<13:
                    message = client_socket.recv(1024).decode()
                    if not message:
                        break
                    # print(f"Received from {client_address}: {message}")
                    # client_socket.send(f"Server received: {message}".encode())
                    # Receive the message
                    if "Done" not in message:
                        print("Not right msg", message)
                        return
                    line = "G21\nG90\nG94\nG01 F300.00\n"
                    command = str.encode(line + "\n")
                    

                    client_socket.send(command)  # Send g-code
                    line = f"G00 Y{0}"
                    cleaned_line = remove_eol_chars(remove_comment(line))
                    if cleaned_line:  # checks if string is empty
                        # converts string to byte encoded string and append newline
                        command = str.encode(line + "\n")
                        client_socket.send(command)  # Send g-code
                            
                    for y in np.linspace(0, 1, 10):
                        line = f"G00 Y{-y}"
                        print("Sending gcode:" + str(line))

                        command = str.encode(line + "\n")
                        client_socket.send(command)  # Send g-code
                        for z in np.linspace(0, 2.6, 50):
                            message = client_socket.recv(1024).decode()
                            if "Done" not in message:
                                print("Not right msg", message)
                                
                            line = f"G00 Z{z}"
                            # cleaning up gcode from file
                            cleaned_line = remove_eol_chars(remove_comment(line))
                            if cleaned_line:  # checks if string is empty
                                print("Sending gcode:" + str(cleaned_line))
                                # converts string to byte encoded string and append newline
                                command = str.encode(line + "\n")
                                client_socket.send(command)  # Send g-code
                                get_force_measurement(name=f"{z}", dir=f"tests_data/pla_with_black_cover{i}/{y}")
                        for z in reversed(np.linspace(0, 2.6, 50)):
                            message = client_socket.recv(1024).decode()
                            if "Done" not in message:
                                print("Not right msg", message)
                          
                            line = f"G00 Z{z}"
                            # cleaning up gcode from file
                            cleaned_line = remove_eol_chars(remove_comment(line))
                            if cleaned_line:  # checks if string is empty
                                print(str(cleaned_line))
                                # converts string to byte encoded string and append newline
                                command = str.encode(line + "\n")
                                client_socket.send(command)  # Send g-code
                                get_force_measurement(name=f"{z}", dir=f"tests_data/pla_with_black_cover{i}/reversed_{y}")
                    i+=1
            except ConnectionResetError:
                print(f"Connection lost with {client_address}.")
            finally:
                client_socket.close()
                print(f"Connection with {client_address} closed.")
                
    except socket.error as e:
        print(f"Socket error: {e}")
        sys.exit(1)
    finally:
        server_socket.close()
        print("Server socket closed.")
        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # server_socket.bind((host, port))
        # server_socket.listen(5)

        # Listen for incoming connections
        # server_socket.listen(1)

        # Accept the incoming connection
        # conn, addr = server_socket.accept()



def get_force_measurement(n_mes: int = 100, name: str = "", dir=""):
    pmu = TestGateOk.pmu
    directory = os.path.dirname(dir)

    # save_dir = os.path.join(directory, dir)
    save_dir = dir
    # TestGateOk.configure_node()
    result = []
    i = 0
    j = 0
    while i < n_mes or j < n_mes:
        try:
            # for i in range(n_mes):
            recv = pmu.recv_force().message
            print(recv)
            if recv.actuator_id == 1:
                i += 1
            if recv.actuator_id == 0:
                j += 1
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
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    pd.DataFrame(results).to_csv(f"{save_dir}/{name}.csv", index=False)

if __name__ == "__main__":

    # Start a thread to receive a message and call the function
    receive_thread = threading.Thread(target=receive_message_and_call_function)
    receive_thread.start()
