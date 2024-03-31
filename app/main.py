"""Main module"""

import socket


def main():
    """
    Main program
    """
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # print(f"DEBUG: server_socket={server_socket}")
    while True:
        (connection, addr) = server_socket.accept() # wait for client
        print(f"DEBUG: After server_socket.accept(): (connection={connection}, addr={addr})")
        with connection:
            while True:
                data = connection.recv(1024)
                print(f"DEBUG: Received data={data}")
                if not data:
                    break   # Client has closed the connection.
                print("DEBUG: Sending reply: PONG")
                connection.sendall(b'+PONG\r\n')


if __name__ == "__main__":
    main()
