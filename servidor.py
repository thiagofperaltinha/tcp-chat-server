import socket
import threading
import datetime
import rsa
from utils.crypto import cripto_mesage, descripto_mesage, gerar_chave, serialize_public_key, deserialize_public_key
from utils.cont_bytes import enviar_dados_tamanho, receber_dados_tamanho
from u import verificar_msg_enviada, verificar_msg_recebida, comandos, clientes_info

public_keys_clients = {}

# Server configuration
ip = '127.0.0.1'
port = 3000

public_keys, private_keys = gerar_chave()

# Locks for thread safety
print_lock = threading.Lock()
clientes_lock = threading.Lock()

# Send a message to all connected clients except the sender
def broadcast(message, sender):
    with clientes_lock:
        disconnected = []
        for client in list(clientes_info.keys()):
            if client != sender:
                try:
                    encrypted_message = rsa.encrypt(message.encode(), public_keys_clients[client])
                    enviar_dados_tamanho(encrypted_message, client)
                except Exception as e:
                    print(f"ERROR: {e}")
                    client.close()
                    disconnected.append(client)
        for client in disconnected:
            del clientes_info[client]

# Function to receive messages from a specific client
def receive_client_messages(conn, addr):
    name_set = False
    while True:
        try:
            encrypted_data = receber_dados_tamanho(conn)       
            received_message = descripto_mesage(encrypted_data, private_keys)
            
            if verificar_msg_recebida(received_message):
                print(f"🔌 Connection closed by the client {addr}.")
                break

            # First message: username
            if not name_set:
                if received_message.startswith("<username>:"):
                    name = received_message.split(":", 1)[1].strip()
                    with clientes_lock:
                        clientes_info[conn] = name
                    name_set = True
                    continue
                else:
                    conn.send(enviar_dados_tamanho(
                        cripto_mesage("❌ Invalid username format. Use <username>:your_name", public_keys_clients[conn])
                    ))
                    continue

            # Special messages
            if received_message.lower() in ("service*", "help*"):
                comandos(received_message, conn, public_keys_clients[conn])
                continue

            comandos(received_message, conn, public_keys_clients[conn])

            # Send to the server
            with print_lock:
                print(f"\n🟢 {clientes_info.get(conn, addr)}: {received_message}")
                print("You/Server: ", end="", flush=True)

            # Send to other clients
            username = clientes_info.get(conn)
           
            if username:
                message_to_others = f"@{username} says: {received_message}"
            else:
                message_to_others = f"\n Unknown says: {received_message}"
                print(clientes_info)
          
            print(f"Message to be sent to other clients: {message_to_others}")
            broadcast(message_to_others, conn)

        except Exception as e:
            print(f"⚠️ Error while handling client {addr}: {e}")
            break

    with clientes_lock:
        if conn in clientes_info:
            del clientes_info[conn]
    conn.close()

# Function to handle each connected client
def handle_client(conn, addr):
    print(f"📶 New connection from {addr[0]}:{addr[1]}")
    conn.send(b"Welcome to my TCP server, client!\n")

    with clientes_lock:
        clientes_info[conn] = f"{addr[0]}:{addr[1]}"  # Placeholder, will be replaced

    threading.Thread(target=receive_client_messages, args=(conn, addr)).start()

# Start the server and wait for connections
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    print(f"🚀 Server started at {ip}:{port}\n📡 Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        enviar_dados_tamanho(serialize_public_key(public_keys), conn)
        
        receive_key_size = receber_dados_tamanho(conn)
        public_keys_clients[conn] = deserialize_public_key(receive_key_size)
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
