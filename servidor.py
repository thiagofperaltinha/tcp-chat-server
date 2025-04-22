import socket
import threading

from utils import verificar_msg_enviada, verificar_msg_recebida

ip = '127.0.0.1'
port = 3000
print_lock = threading.Lock()
     
def receber_mensagens_clientes(conn, addr):
    while True:
        try:
            mensagem_recebida = conn.recv(1024).decode()
            if verificar_msg_recebida(mensagem_recebida):
                print("Connection closed by the client.")
                break
            with print_lock:
                print(f"\nclient{addr}: {mensagem_recebida}")
                print("You/Server: ", end="", flush=True)
        except ConnectionResetError:
            print(f"\nClient {addr} disconnected unexpectedly.")
            break
    conn.close()
    
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
    
def client(conn, addr):
    print("Connection from %s: %d" %(addr[0], addr[1]))
    conn.send(b"Welcome to my TCP server, client number 1!\n")  
    
    threading.Thread(target=receber_mensagens_clientes, args=(conn, addr)).start()
    threading.Thread(target=enviar_mensagens_clientes, args=(conn, addr)).start()
    
    
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((ip, port))
s.listen()    

while True:
    conn, addr = s.accept()  # accepts the connection, removing it from the listening queue
    thread = threading.Thread(target=client, args = (conn, addr))
    thread.start()