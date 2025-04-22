import socket
import threading
from utils import verificar_msg_enviada, verificar_msg_recebida, comandos

# Configurações do servidor
ip = '127.0.0.1'
port = 3000

# Locks para garantir segurança em ambiente multithread
print_lock = threading.Lock()
clientes_lock = threading.Lock()

# Lista de clientes conectados
clientes = []

# Envia uma mensagem para todos os clientes, exceto o remetente
def broadcast(mensagem, remetente):
    with clientes_lock:
        for cliente in clientes:
            if cliente != remetente:
                try:
                    cliente.send(mensagem.encode())
                except:
                    cliente.close()
                    clientes.remove(cliente)

# Função para receber mensagens de um cliente específico
def receber_mensagens_clientes(conn, addr):
    while True:
        try:
            mensagem_recebida = conn.recv(1024).decode()
            if verificar_msg_recebida(mensagem_recebida):
                print(f"Connection closed by the client {addr}.")
                break

            with print_lock:
                print(f"\nClient {addr}: {mensagem_recebida}")
                print("You/Server: ", end="", flush=True)

            mensagem_broadcast = f"{addr[0]}:{addr[1]} says: {mensagem_recebida}"
            broadcast(mensagem_broadcast, conn)
            comandos(mensagem_recebida, conn)

        except ConnectionResetError:
            print(f"\nClient {addr} disconnected unexpectedly.")
            break
        except:
            break

    with clientes_lock:
        if conn in clientes:
            clientes.remove(conn)
    conn.close()

# Função para o servidor enviar mensagens para o cliente
def enviar_mensagens_clientes(conn, addr):
    while True:
        try:
            mensagem_enviada = input("You/Server: ")
            if verificar_msg_enviada(conn, mensagem_enviada):
                break
            conn.send(mensagem_enviada.encode())
        except:
            break
    conn.close()

# Função que lida com cada cliente conectado
def client(conn, addr):
    print(f"Connection from {addr[0]}:{addr[1]}")
    conn.send(b"Welcome to my TCP server, client!\n")

    with clientes_lock:
        clientes.append(conn)

    threading.Thread(target=receber_mensagens_clientes, args=(conn, addr)).start()
    threading.Thread(target=enviar_mensagens_clientes, args=(conn, addr)).start()

# Inicializa o servidor e aguarda conexões 
def main():
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen()    
    
    print(f"Servidor iniciado em {ip}:{port}...\nAguardando conexões...")
    
    while True:
        conn, addr = s.accept()  # accepts the connection, removing it from the listening queue
        thread = threading.Thread(target=client, args = (conn, addr))
        thread.start()
        
if __name__ == "__main__":
    main()  