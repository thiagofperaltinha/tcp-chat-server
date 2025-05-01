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
        desconectados = []
        for client in list(clientes_info.keys()):
            if client != sender:
                try:
                    mensagem_criptografada = rsa.encrypt(message.encode(), public_keys_clients[client])
                    client.send(mensagem_criptografada)
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
            encrypted_data = receber_dados_tamanho(conn)
            print(f"🔐 Dados recebidos do cliente: {encrypted_data}")
           
            received_message = descripto_mesage(encrypted_data, private_keys)
            
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
                    conn.send(enviar_dados_tamanho(
                        cripto_mesage("❌ Invalid username format. Use <username>:your_name", public_keys_clients[conn])
                    ))
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
                mensagem_other_cl = f"User: @{username} says: {received_message}"
            else:
                mensagem_other_cl = f"\n Unknown says: {received_message}"
                print(clientes_info)
            broadcast(mensagem_other_cl, conn)

        except Exception as e:
            print(f"⚠️ Erro ao lidar com cliente {addr}: {e}")
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
        clientes_info[conn] = f"{addr[0]}:{addr[1]}"  # Placeholder, será substituído

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
        
        receber_tam_key = receber_dados_tamanho(conn)
        print(f"Received public key:\n{receber_tam_key.decode()}")  # Verifique se a chave é PEM
        public_keys_clients[conn] = deserialize_public_key(receber_tam_key)
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
