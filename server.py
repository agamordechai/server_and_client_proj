import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
MAX_CLIENTS = 10

# List to keep track of connected clients
clients = []
client_names = {}  # Dictionary to map client names to socket objects

def handle_client(client_socket):
    """
    Handles a client connection.
    Args:
        client_socket: The socket object of the client.

    Returns: None
    """
    client_name = client_socket.recv(1024).decode('utf-8')
    client_names[client_name] = client_socket  # Add client name to the dictionary
    welcome_message = f"{client_name} has joined the chat!"
    broadcast(welcome_message, client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.startswith("@"):
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    recipient_name = parts[0].replace("@", "")
                    private_message = parts[1]
                    send_private_message(client_name, recipient_name, private_message, client_socket)
                    print(f"Private message from {client_name} to {recipient_name}: {private_message}")
                else:
                    client_socket.send("Invalid private message format. Use @recipient_name message".encode('utf-8'))
            else:
                broadcast(f"{client_name}: {message}", client_socket)
                print(f"{client_name}: {message}")
        except:
            clients.remove(client_socket)
            client_socket.close()
            del client_names[client_name]
            broadcast(f"{client_name} has left the chat.", client_socket)
            break

def send_private_message(sender_name, recipient_name, message, sender_socket):
    """
    Sends a private message to a specific client.
    Args:
        sender_name: The name of the sender.
        recipient_name: The name of the recipient.
        message: The message to be sent.
        sender_socket: The socket object of the sender.

    Returns: None
    """
    if sender_name == recipient_name:
        sender_socket.send("You cannot send a private message to yourself.".encode('utf-8'))
        return

    recipient_socket = client_names.get(recipient_name)
    if recipient_socket:
        try:
            recipient_socket.send(f"Private from {sender_name}: {message}".encode('utf-8'))
        except:
            clients.remove(recipient_socket)
            recipient_socket.close()
    else:
        sender_socket.send(f"User {recipient_name} not found.".encode('utf-8'))
        sender_socket.send(f"Available users: {', '.join(client_names.keys())}".encode('utf-8'))

def broadcast(message, sender_socket):
    """
    Broadcasts a message to all connected clients except the sender.
    Args:
        message: The message to be broadcast.
        sender_socket: The socket object of the sender.

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
    Main function to start the server.
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