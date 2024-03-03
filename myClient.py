import socket
import threading


SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
CONNECTIONS_MSG = "connections"
VISIBILITY_MSG = "visibility"
CONTACT_MSG = "contact"


def main():
    
    """ TCP """
    if True:
        def send_message(target_host, target_port):
                    # Create a UDP socket
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    active = True  # The client is active to send and receive messages
                    message="exit"
                    while active:
                        message = input("Enter a message (or 'exit' to quit): ")
                        if message.lower() == "exit":
                            break

                        # Send the message to Client 2
                        client_socket.sendto(f"{username}~ {message}".encode(), (target_host, target_port))#messaging

                    # Close the socket
                    if message == "exit":
                        client_socket.close()

        def receive_message(listen_host,listen_port):
                    # Create a UDP socket
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # Bind the socket to a specific address and port
                    client_socket.bind((listen_host, listen_port))
                    while True:
                        data, addr = client_socket.recvfrom(1024)
                        message = data.decode()
                        print(f"\n[MESSAGE] Received message from {addr[0]}: {message}")
      #Sign In with username
      
        print("sign in: \n")
        username = input("Enter your username: ")
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
        addressArray = (client.recv(SIZE).decode(FORMAT)).split(":") 
        receive_thread = threading.Thread(target=receive_message, args=(addressArray[0], int(addressArray[1])+1))
        receive_thread.start()
        print("This is the current client's IP:",addressArray[0],"and PORT connected with server: ",addressArray[1])
        client.send(username.encode(FORMAT)) #send username to server
        connected = True
        '''While the client is still connected to the server'''
        while connected:

            request = input("[REQUEST] Please enter one of the following commands to interact with the server:\n1.To "
                            "disconnect from the server, type 'disconnect'.\n2.To view the list of active clients, "
                            "type 'connections'.\n3.To change visibility permissions, type 'visibility'.\n4.To contact a client, type 'contact'\n :")
            client.send(request.encode(FORMAT))
            if request.lower() == DISCONNECT_MSG:
                connected = False  # The client disconnects from the server

            elif request.lower() == CONNECTIONS_MSG:
                print(client.recv(SIZE).decode(FORMAT))  # Displays the server's response
            elif request.lower() == VISIBILITY_MSG:
                visibility = input("[VISIBILITY] Do you want to be visible to certain clients when connected to this "
                                   "server?\n1.To be visible, Type 'yes'\n2.To be invisible, Type 'no'\n :")
                client.send(visibility.encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))
            elif request.lower() == CONTACT_MSG: #SEND TO A CLIENT
                client_name = input("[CHAT_REQ] Enter the name of the client you with to contact: ")
                client.send(client_name.encode(FORMAT))
                clientInfo = (client.recv(SIZE).decode(FORMAT)).split(":") #client's information(we want to send to)
                print(clientInfo)
                

                #  Start the send and receive functions in separate threads
                
                send_thread = threading.Thread(target=send_message, args=(clientInfo[0], int(clientInfo[1])+1))
                
                
                send_thread.start()
                
                
            else:
                print(client.recv(SIZE).decode(FORMAT))
if __name__ == "__main__":
    main()
