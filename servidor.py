import socket
import threading
from utils import verificar_msg_enviada, verificar_msg_recebida, comandos

# Server configuration
ip = '127.0.0.1'
port = 3000

# Locks for thread safety
print_lock = threading.Lock()
clientes_lock = threading.Lock()

# List of connected clients
clientes = []

# Send a message to all connected clients except the sender
def broadcast(message, sender):
    with clientes_lock:
        for client in clientes:
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    clientes.remove(client)

# Function to receive messages from a specific client
def receive_client_messages(conn, addr):
    while True:
        try:
            received_message = conn.recv(1024).decode()
            if verificar_msg_recebida(received_message):
                print(f"🔌 Connection closed by the client {addr}.")
                break

            if received_message.lower() in ("<service>", "<help>"):
                comandos(received_message, conn)
                continue

            comandos(received_message, conn)

            with print_lock:
                print(f"\n🟢 Client {addr}: {received_message}")
                print("You/Server: ", end="", flush=True)

            broadcast_message = f"{addr[0]}:{addr[1]} says: {received_message}"
            broadcast(broadcast_message, conn)

        except ConnectionResetError:
            print(f"\n⚠️ Client {addr} disconnected unexpectedly.")
            break
        except:
            break

    with clientes_lock:
        if conn in clientes:
            clientes.remove(conn)
    conn.close()

# Function for the server to send messages to a client
def send_server_messages(conn, addr):
    while True:
        try:
            sent_message = input("You/Server: ")
            if verificar_msg_enviada(conn, sent_message):
                break
            conn.send(sent_message.encode())
        except:
            break
    conn.close()

# Function to handle each connected client
def handle_client(conn, addr):
    print(f"📶 New connection from {addr[0]}:{addr[1]}")
    conn.send(b"Welcome to my TCP server, client!\n")

    with clientes_lock:
        clientes.append(conn)

    threading.Thread(target=receive_client_messages, args=(conn, addr)).start()
    threading.Thread(target=send_server_messages, args=(conn, addr)).start()

# Start the server and wait for connections
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    print(f"🚀 Server started at {ip}:{port}\n📡 Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
