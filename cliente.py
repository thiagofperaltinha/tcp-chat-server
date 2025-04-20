import socket
from utils import verificar_msg_enviada, verificar_msg_recebida

ip = '127.0.0.1'  # localhost
port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((ip, port))

# Welcome message from the server
mensage_boas_vindas = s.recv(1024).decode()
print(mensage_boas_vindas)

# Instructions for the user
print("Type <Service>: to know which services our server provides.\n", "Type <exit chat>: to leave the chat room. \n")

while True:
    mensagem_enviada = input("You: ")
    if verificar_msg_enviada(s, mensagem_enviada):
        break
    s.send(mensagem_enviada.encode())

    mensagem_recebida = s.recv(1024).decode()  # receive response from the server
    if verificar_msg_recebida(mensagem_recebida):
        print("Connection closed by the server.")
        break
    
    print("Server: ", mensagem_recebida)

s.close()  # close the socket connection
