import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket):
    """
    Receives messages from the server and prints them to the console.
    Args:
        client_socket: The socket object of the client.

    Returns: None
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Connection closed by the server.")
            client_socket.close()
            break

def main():
    """
    Main function to start the client and connect to the server.
    Returns: None
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_name = input("Enter your name: ")
    client_socket.send(client_name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()