import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
MAX_CLIENTS = 10

# List to keep track of connected clients
clients = []

def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode('utf-8')
    welcome_message = f"{client_name} has joined the chat!"
    broadcast(welcome_message, client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.startswith("@"):
                parts = message.split(" ", 2)
                if len(parts) == 2:
                    recipient_name = parts[0].replace("@", "")
                    private_message = parts[1]
                    print(f"Private message from {client_name} to {recipient_name}: {private_message}")
                    send_private_message(client_name, recipient_name, private_message, client_socket)
                else:
                    client_socket.send("Invalid private message format. Use @recipient_name message".encode('utf-8'))
            else:
                broadcast(f"{client_name}: {message}", client_socket)
                print(f"{client_name}: {message}")
        except:
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"{client_name} has left the chat.", client_socket)
            break

def send_private_message(sender_name, recipient_name, message, sender_socket):
    recipient_found = False
    clients_names = {client.getpeername()[0]: client for client in clients}
    for client in clients:
        if client.getpeername()[0] == recipient_name:
            try:
                client.send(f"Private from {sender_name}: {message}".encode('utf-8'))
                recipient_found = True
            except:
                clients.remove(client)
                client.close()
            break
    if not recipient_found:
        sender_socket.send(f"User {recipient_name} not found.".encode('utf-8'))
        sender_socket.send(f"Available users: {', '.join(clients_names.keys())}".encode('utf-8'))

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def main():
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