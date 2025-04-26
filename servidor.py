import socket
import threading
import datetime
from utils import verificar_msg_enviada, verificar_msg_recebida, comandos, clientes_info

# Server configuration
ip = '127.0.0.1'
port = 3000

# Locks for thread safety
print_lock = threading.Lock()
clientes_lock = threading.Lock()

def chat_log(username, mensagem):
    with open("chat.txt", "a") as f:
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{data}]{username}:{mensagem}\n")
    

# Send a message to all connected clients except the sender
def broadcast(message, sender):
    with clientes_lock:
        desconectados = []
        for client in list(clientes_info.keys()):
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    desconectados.append(client)
        for client in desconectados:
            del clientes_info[client]

# Function to receive messages from a specific client
def receive_client_messages(conn, addr):
    nome_definido = False
    while True:
        try:
            received_message = conn.recv(1024).decode()
            if verificar_msg_recebida(received_message):
                print(f"🔌 Connection closed by the client {addr}.")
                break

            # Primeira mensagem: nome do usuário
            if not nome_definido:
                if received_message.startswith("<username>:"):
                    nome = received_message.split(":", 1)[1].strip()
                    with clientes_lock:
                        clientes_info[conn] = nome
                    nome_definido = True
                    continue
                else:
                    conn.send("❌ Invalid username format. Use <username>:your_name\n")
                    continue

            # Comandos especiais
            if received_message.lower() in ("<service>", "<help>"):
                comandos(received_message, conn)
                continue

            comandos(received_message, conn)

            # Mostrar no servidor
            with print_lock:
                print(f"\n🟢 {clientes_info.get(conn, addr)}: {received_message}")
                print("You/Server: ", end="", flush=True)

            
            # Enviar para os outros clientes
            username = clientes_info.get(conn)
            
            if username:
                mensagem_other_cl = f"@{username} says: {received_message}"
            else:
                mensagem_other_cl = f"\n Unknown says: {received_message}"
                print(clientes_info)
            broadcast(mensagem_other_cl, conn)

        except ConnectionResetError:
            print(f"\n⚠️ Client {addr} disconnected unexpectedly.")
            break
        except:
            break

    with clientes_lock:
        if conn in clientes_info:
            del clientes_info[conn]
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
        clientes_info[conn] = f"{addr[0]}:{addr[1]}"  # Placeholder, será substituído

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
