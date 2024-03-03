import socket
import threading
# Author: Mnelisi Mabuza, Mzimazi Hlabe, Iviwe Booi
# DATE: 03-03-2024
# NETWORKS ASSIGNMENT (P2P CHAT APP) 


HOST = socket.gethostbyname(socket.gethostname())  # Host IP address
PORT = 9090
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
VIEW_CONNECTIONS_MSG = "connections"
VISIBILITY_MSG = "visibility"
CONTACT_MSG = "contact"
# Array list to store the connections
connections = []
visibility = []
usernames = []


def handle_client(com_socket, addr):
    print(f"[NEW CONNECTION] The server is connected to {addr} ")
    connections.append(addr)  # Add new connection ADDR to the list
    visibility.append(True)
    connected = True
    username = com_socket.recv(SIZE).decode(FORMAT).lower()
    # com_socket.send("username recieved!".encode(FORMAT))
    usernames.append(username)

    while connected:
        msg = com_socket.recv(SIZE).decode(FORMAT).lower()  # Convert received message to lowercase
        # message received from the communication client socket
        if msg.lower() == DISCONNECT_MSG:
            connected = False
            index = connections.index(addr)
            visibility.pop(index)
            usernames.pop(index)

            print(f"[DISCONNECTION] The server is disconnected from {addr}")

        elif msg.lower() == VIEW_CONNECTIONS_MSG:
            print(f"[REQUEST] msg from client {ADDR}")
            response = "Connections active: \n"
            count = 1
            for i in range(0, len(connections)):
                if visibility[i]:
                    response = f"{response} {count}. {usernames[i]} :{connections[i]}\n"
                    count += 1

            com_socket.send(response.encode(FORMAT))
            # print("This is visibility array: ", visibility)
        elif msg.lower() == VISIBILITY_MSG:
            visibility_prompt = com_socket.recv(SIZE).decode(
                FORMAT).lower()  # Receive visibility preference from client
            if visibility_prompt.lower() == "no":
                index = connections.index(addr)
                visibility[index] = False
                com_socket.send("[RESPONSE] visibility disabled!".encode(FORMAT))
            else:
                index = connections.index(addr)
                # print(index)
                visibility[index] = True
                com_socket.send("[RESPONSE] visibility enabled!".encode(FORMAT))
                # print("This is visibility array: ", visibility)
        elif msg.lower() == CONTACT_MSG:
            client_name = com_socket.recv(SIZE).decode(FORMAT).lower()
            print("Message received:", client_name)
            index = usernames.index(client_name)
            if index == -1:
                com_socket.send("[RESPONSE] Client name is not available or exist!".encode(FORMAT))
            else:
                print(f"{connections[index][0]}:{connections[index][1]}")
                com_socket.send(
                    f"{connections[index][0]}:{connections[index][1]}".encode(FORMAT))  # IP ADDRESS OF RECEIVER
        else:
            response = "[ERROR] request message not understood by server!!!"
            com_socket.send(response.encode(FORMAT))
    # print(visibility)
    com_socket.close()
    connections.remove(addr)  # Remove the connection ADDR from the list after disconnection


def main():
    """starting a TCP socket"""
    print("[STARTING] the server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating server socket for accepting connections
    server.bind(ADDR)  # bind/associate the server socket with the ADDR for identification
    server.listen()  # listen for any client trying to connect to server
    print(f"[LISTENING] the server is listening on {HOST}:{PORT} \n")

    while True:
        com_socket, addr = server.accept()  # server accept connection from communication socket.
        com_socket.send(f"{addr[0]}:{addr[1]}".encode(FORMAT))
        # create a separate thread for the server to handle the accepted client.
        thread = threading.Thread(target=handle_client, args=(com_socket, addr))
        thread.start()
        # print the number of active connections/ number of threads
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # minus the main thread
        print(f"Current connections: {connections}")


if __name__ == "__main__":
    main()