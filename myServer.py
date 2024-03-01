import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())  # Host IP address
PORT = 9090
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
VIEW_CONNECTIONS_MSG = "connections"
VISIBILITY_MSG = "visibility"
# Array list to store the connections
connections = []
visibility = []
for i in connections:
    visibility.append(True)


def handle_client(com_socket, addr):
    print(f"[NEW CONNECTION] The server is connected to {addr} ")
    connections.append(addr)  # Add new connection ADDR to the list
    visibility.append(True)
    connected = True
    while connected:
        msg = com_socket.recv(SIZE).decode(FORMAT).lower()  # Convert received message to lowercase
        # message received from the communication client socket
        if msg.lower() == DISCONNECT_MSG:
            connected = False
            print(f"[DISCONNECTION] The server is disconnected from {addr}")

        elif msg.lower() == VIEW_CONNECTIONS_MSG:
            print(f"[REQUEST] msg from client {ADDR}")
            response = "Connections active: \n"
            count = 1
            for i in range(0, len(connections)):
                if visibility[i]:
                    response = f"{response} {count}. {connections[i]}\n"
                count += 1
            com_socket.send(response.encode(FORMAT))
        elif msg.lower() == VISIBILITY_MSG :
            visibility_prompt = com_socket.recv(SIZE).decode(FORMAT).lower()  # Receive visibility preference from client
            if visibility_prompt.lower() == "No":
                index = connections.index(addr)
                connections.remove(addr) #New line added
                print(addr)
                visibility[index] = False

            else:
                index = connections.index(addr)
                print(index)
                visibility[index] = True

        else:
            response = "[ERROR] request message not understood by server!!!"
            com_socket.send(response.encode(FORMAT))
    print(visibility)
    com_socket.close()
    connections.remove(addr)  # Remove the connection ADDR from the list after disconnection


def main():
    """starting a TCP socket"""
    print("[STARTING] the server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating server socket for accepting connections
    server.bind(ADDR)  # bind/associate the server socket with the ADDR for identification
    server.listen()   # listen for any client trying to connect to server
    print(f"[LISTENING] the server is listening on {HOST}:{PORT} \n")

    while True:
        com_socket, addr = server.accept()  # server accept connection from communication socket.

        # create a separate thread for the server to handle the accepted client.
        thread = threading.Thread(target=handle_client, args=(com_socket, addr))
        thread.start()
        # print the number of active connections/ number of threads
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # minus the main thread
        print(f"Current connections: {connections}")


if __name__ == "__main__":
    main()
