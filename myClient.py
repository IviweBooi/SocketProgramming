import socket
import threading
# Author~ Mnelisi Mabuza
# Student# ~ MBZMNE001
# MESSAGING APPLICATION
# MARCH 2024

SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
CONNECTIONS_MSG = "connections"
VISIBILITY_MSG = "visibility"
CONTACT_MSG = "contact"


def main():
    """ TCP """
    if True:
        """server option"""
        print("sign in: \n")
        username = input("Enter your username: ")
        IP = input("[IP ADDRESS] | Enter the server's IP address : ")  # Host IP address
        portNumber = eval(input("[Port number] Enter the port number of your connection: "))

        ADDR = (IP, portNumber)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # client communication socket
        try:
            client.connect(ADDR)  # connecting the client to the server
            print(f"\n[CONNECTED] Client connected to server at {IP}:{portNumber}")
        except (socket.gaierror, ConnectionRefusedError):
            print(f"[Error!] | Server {ADDR} can't be reached!!!")
            return
        addressArray = (client.recv(SIZE).decode(FORMAT)).split(":")
        client.send(username.encode(FORMAT))  # send username to server
        # connected = True

        def prompter(connected):
            while connected:

                requestM =input("[PROMPT | USER] Please select an option: (only type the number of the option)\n1. Disconnect from server!\n2. View Active users.\n3. Visibility status.\n4. Contact A client\n >>")
                if requestM in ["1", "2", "3", "4"]:
                    client.send(requestM.encode(FORMAT))
                else:
                    print("Please select a valid option! from the list > [1, 2, 3, 4 ]")
                    prompter(True) #Start over
                if requestM == "1":
                    connected = False  # The client disconnects from the server

                elif requestM == "2":
                    print(client.recv(SIZE).decode(FORMAT))  # Displays the server's response
                elif requestM == "3":
                    visibility = input("[VISIBILITY STATUS] Select a number:\n1. Enable visibility. \n2. Disable Visibility.\n")
                    client.send(visibility.encode(FORMAT))
                    print(client.recv(SIZE).decode(FORMAT))
                elif requestM == "4":  # SEND TO A CLIENT
                    client_name = input("[Contact REQUEST] | Enter the client's [username] : ")
                    client.send(client_name.encode(FORMAT))
                    clientInfo = (client.recv(SIZE).decode(FORMAT)).split(":")  # client's information(we want to send to)
                    print(clientInfo)

                    def send_message(target_host, target_port):
                        # Create a UDP socket
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        active = True  # The client is active to send and receive messages
                        while active:
                            message = input("[Texting] Type a message (or 'exit' to quit): ")
                            if message.lower() == "exit":
                                prompter(True)

                            # Send the message to Client 2
                            client_socket.sendto(f"{username}~ {message}".encode(), (target_host, target_port))  # messaging
                        client_socket.close()

                    def receive_message(listen_host, listen_port):
                        # Create a UDP socket
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        # Bind the socket to a specific address and port
                        client_socket.bind((listen_host, listen_port))

                        while True:
                            data, addr = client_socket.recvfrom(1024)
                            message = data.decode()
                            print(f"\n[MESSAGE] Received message from {addr[0]}: {message}")

                            # client_socket.close()
                #  Start the send and receive functions in separate threads
                    send_thread = threading.Thread(target=send_message, args=(clientInfo[0], int(clientInfo[1]) + 1))
                    receive_thread = threading.Thread(target=receive_message, args=(addressArray[0], int(addressArray[1])+1))
                    count = 0
                    while count < 10:
                        send_thread.start()
                        receive_thread.start()
                        send_thread.join()
                        receive_thread.join()

                        count += 1
                        if count == 10:
                            p = input("session is about to time out, Do you want to continue chatting?[yes or no]\n")
                            if p == "yes":
                                count = 0
            else:
                print("Please select a valid option! from the list > [1, 2, 3, 4 ]")
        prompter(True)


if __name__ == "__main__":
    main()
