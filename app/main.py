"""Main module"""

import socket
import threading


def handle_client(connection):
    print(f"DEBUG: handle_client(connection={connection})")
    with connection:
        while True:
            data = connection.recv(1024)
            print(f"DEBUG: Received data={data}")
            if not data:
                break   # Client has closed the connection.
            print("DEBUG: Sending reply: PONG")
            connection.sendall(b'+PONG\r\n')


def main():
    """
    Main program
    """
    # print("DEBUG: main() starts here")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # print(f"DEBUG: server_socket={server_socket}")
    while True:
        (connection, addr) = server_socket.accept() # wait for client
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()


if __name__ == "__main__":
    main()
