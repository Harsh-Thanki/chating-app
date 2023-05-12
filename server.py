import socket
import threading

HOST = '127.0.0.1'  # Your Private Ip
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []  # List of all Clients
nicknames = []  # List of all Nicknames


def broadcast(message):
    """ To Broadcast a msg to all connected Clients """
    for client in clients:
        client.send(message)


def handle(client):
    """ Handles individual connection to the Client (comes into play after connection is established with the help of receive()) """
    while True:
        try:
            message = client.recv(1024)  # 1024 Bytes
            # the index of client and it's respective nickname will be same in their respective lists
            print(f"{nicknames[clients.index(client)]} says {message}")  # server log
            broadcast(message)  # broadcast
        except:
            # Removing client along with its nickname in case something goes wrong (i.e. system crash)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    """ Periodically checks for new Client connections and accepts them """
    while True:  # signal handling can be done

        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))  # sending a signal for nickname, using client socket
        nickname = client.recv(1024)  # 1024 Bytes

        # adding client and nickname to their respective lists
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")  # server log
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))  # broadcast
        client.send(f"Hi {nickname}, you are connected to server!".encode('utf-8'))  # msg to client when connected

        thread = threading.Thread(target=handle, args=(client,))  # due to , in args it'll be treated as tuple
        thread.start()


print("server running...")
receive()  # server started
