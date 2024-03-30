import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    print(f"DEBUG: server_socket={server_socket}")
    (connection, addr) = server_socket.accept() # wait for client
    print(f"DEBUG: After server_socket.accept()")
    with connection:
        connection.recv(1024)
        connection.sendall(b'+PONG\r\n')


if __name__ == "__main__":
    main()
