import socket
import threading


SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
CONNECTIONS_MSG = "connections"
VISIBILITY_MSG = "visibility"


def main():
    """ TCP """
    options = eval(input("Select the number of the end-system you would like to communicate with and hit "
                         "enter:\n1.Server\n2.Client\n>> "))

    if options == 1:
        """server option"""

        HOST = input("Enter the IP Address of the server you wish to establish a connection with: ")  # Host IP address
        PORT = eval(input("Enter the PORT # of the server: "))
        ADDR = (HOST, PORT)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # client communication socket
        try:
            client.connect(ADDR)  # connecting the client to the server
            print(f"\n[CONNECTED] Client connected to server at {HOST}:{PORT}")
        except (socket.gaierror, ConnectionRefusedError):
            print(f"[Error] Server {ADDR} can't be reached!!!")
            return

        connected = True
        '''While the client is still connected to the server'''
        while connected:

            request = input("[REQUEST] Please enter one of the following commands to interact with the server:\n1.To "
                            "disconnect from the server, type 'disconnect'.\n2.To view the list of active clients, "
                            "type 'connections'.\n3.To change visibility permissions, type 'visibility'.\n>>")
            client.send(request.encode(FORMAT))
            if request.lower() == DISCONNECT_MSG:
                connected = False  # The client disconnects from the server

            elif request.lower() == CONNECTIONS_MSG:
                print(client.recv(SIZE).decode(FORMAT))  # Displays the server's response
            elif request.lower() == VISIBILITY_MSG:
                visibility = input("[VISIBILITY] Do you want to be visible to certain clients when connected to this "
                                   "server?\n1.To be visible, Type 'yes'\n2.To be invisible, Type 'no'\n>>")
                client.send(visibility.encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))
            else:
                print(client.recv(SIZE).decode(FORMAT))

    elif options == 2:
        """client option"""
        def send_message():
            target_host = input("Enter the IP address of the client you wish to send a message to: ")
            target_port = eval(input("Enter the PORT number of the client you wish to send a message to: "))

            # Create a UDP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            active = True  # The client is active to send and receive messages
            while active:
                message = input("Enter a message (or 'exit' to quit): ")
                if message.lower() == "exit":
                    break

                # Send the message to Client 2
                client_socket.sendto(message.encode(), (target_host, target_port))

            # Close the socket
            client_socket.close()

        def receive_message():
            listen_host = 'Localhost'
            listen_port = 54321

            # Create a UDP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Bind the socket to a specific address and port
            client_socket.bind((listen_host, listen_port))

            while True:
                data, addr = client_socket.recvfrom(1024)
                message = data.decode()
                print(f"\n[MESSAGE] Received message from Client 2: {message}")

        #  Start the send and receive functions in separate threads
        send_thread = threading.Thread(target=send_message)

        receive_thread = threading.Thread(target=receive_message)

        send_thread.start()
        receive_thread.start()

    else:
        print("[ERROR] You have entered an invalid number!!!")


if __name__ == "__main__":
    main()
