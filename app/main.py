"""Poor-man REDIS server in Python"""

import socket
import threading
import time


from app.helpers import milliseconds_to_seconds

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


"""Used for GET and SET commands"""
redis_keys = {}

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
            elif cmd == "set":
                assert len(command) > 2
                key = command[1]
                value = command[2]
                redis_keys[key] = value
                print(f"DEBUG: SET: value={value}, new redis_keys={redis_keys}")
                conn.sendall(b'+OK\r\n')
            elif cmd == "get":
                assert len(command) > 1
                key = command[1]
                value = redis_keys.get(key)
                print(f"DEBUG: redis_keys={redis_keys}, value={value}")
                if value is None:
                    conn.sendall(b'$-1\r\n')
                else:
                    response = f"${len(value)}\r\n{value}\r\n".encode()
                    conn.sendall(response)
                # print(f"TODO: Implement GET")
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
