import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
MAX_CLIENTS = 10

# List to keep track of connected clients
clients = []

def handle_client(client_socket):
    """
    Handles a client connection by receiving messages from the client and broadcasting them to all connected clients.
    Args:
        client_socket: The socket object of the connected client

    Returns: None
    """
    client_name = client_socket.recv(1024).decode('utf-8')
    welcome_message = f"{client_name} has joined the chat!"
    broadcast(welcome_message, client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{client_name}: {message}", client_socket)
            print(f"{client_name}: {message}")
        except:
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"{client_name} has left the chat.", client_socket)
            break

def broadcast(message, sender_socket):
    """
    Broadcasts a message to all connected clients except the sender.
    Args:
        message: The message to broadcast.
        sender_socket: The socket of the client who sent the message.

    Returns: None
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def main():
    """
    Main function to start the server and listen for incoming connections.

    Returns: None
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    print(f'Server started on {HOST}:{PORT}')

    while True:
        client_socket, addr = server.accept()
        print(f'Client connected from {addr}')
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()