
import socket
import sys

# Global variables
SERVER_HOST = "100.76.146.35"
SERVER_PORT = 12345

def start_tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            
            try:
                while True:
                    message = client_socket.recv(1024).decode()
                    if not message:
                        break
                    print(f"Received from {client_address}: {message}")
                    client_socket.send(f"Server received: {message}".encode())
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

if __name__ == "__main__":
    start_tcp_server(SERVER_HOST, SERVER_PORT)
