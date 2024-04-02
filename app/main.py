"""Poor-man REDIS server in Python"""

import socket
import threading


# def handle_commands(conn, request):
#     """
#     Handle RESP commands
#     Reference: <https://redis.io/docs/reference/protocol-spec>
#     """
#     print(f"DEBUG: handle_commands(conn={conn}, request={request})")
#     pass    # TODO


def parse_redis_protocol(data):
    """
    Parse RESP (Redis serialization protocol)
    Reference: <https://redis.io/docs/reference/protocol-spec>
    """
    assert data is not None
    assert len(data) > 0

    lines = data.split(b'\r\n')
    print(f"DEBUG: parse_redis_protocol: lines={lines}")
    command = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # print(f"DEBUG: parse_redis_protocol: line={line}")
        if line.startswith(b'*'):
            # The number of arguments
            pass
        elif line.startswith(b'$'):
            # The length of the next argument
            length = int(line[1:])
            i += 1 # Move to the next argument
            argument = lines[i][:length]    # Get the argument with the specified length
            command.append(argument.decode())   # Assuming UTF-8 enconding
        i += 1
    print(f"DEBUG: parse_redis_protocol: return {command}")
    return command


def handle_connection(conn, addr):
    """
    Handle REDIS connection
    """
    print(f"DEBUG: handle_connection(conn={conn}, addr={addr})")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break   # Client has closed the connection.
            print(f"DEBUG: Received data={data} from addr={addr}")
            command = parse_redis_protocol(data)
            assert len(command) > 0
            cmd = command[0].lower()
            if cmd == "ping":
                print("DEBUG: Sending reply: PONG")
                conn.sendall(b'+PONG\r\n')
            elif cmd == "echo":
                echo_response = ' '.join(command[1:])
                print(f"DEBUG: Sending reply to ECHO: {echo_response}")
                conn.sendall(b'+')
                conn.sendall(echo_response.encode())
                conn.sendall(b'\r\n')
            else:
                print(f"ERROR: Unknown command: {command}")
            # TODO


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
