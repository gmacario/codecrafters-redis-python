"""Main module"""

import socket
import threading


def handle_commands(conn, request):
    pass    # TODO


def handle_connection(conn, addr):
    print(f"DEBUG: handle_connection(conn={conn}, addr={addr})")
    with conn:
        while True:
            data = conn.recv(1024)
            print(f"DEBUG: Received data={data} from addr={addr}")
            if not data:
                break   # Client has closed the connection.
            assert data != None
            assert len(data) > 0
            ch = data.decode('utf-8')[0]
            print(f"DEBUG: ch='{ch}'")
            if ch == '*':
                print("TODO: Handling case ch='*'")
                # TODO
            elif ch == '$':
                print("TODO: Handling case ch='$'")
                # TODO
            else:
                print(f"WARNING: Unknown ch={ch}")
            # TODO
            print("DEBUG: Sending reply: PONG")
            conn.sendall(b'+PONG\r\n')


def main():
    """
    Main program
    """
    print("DEBUG: main() starts here")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # print(f"DEBUG: server_socket={server_socket}")
    while True:
        (conn, addr) = server_socket.accept() # wait for client
        client_thread = threading.Thread(target=handle_connection, args=(conn, addr))
        client_thread.start()


if __name__ == "__main__":
    main()
