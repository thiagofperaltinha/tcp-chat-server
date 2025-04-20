import socket

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
    
    if mensagem_enviada == "exit chat":  # exit command
        mensagem_saida = input("Are you sure you want to end this chat? To confirm type: <yes> ")
        if mensagem_saida == "yes":  # user confirmed they want to quit
            print("Connection closed.")
            break
        else:  # user chose not to quit
            continue
    else:
        s.send(mensagem_enviada.encode())  # send the message to the server
    
    mensagem_recebida = s.recv(1024).decode()  # receive response from the server
    
    if mensagem_recebida == "exit chat":  # server ended the chat
        print("Connection closed by the server.")
        break
    
    print("Server: ", mensagem_recebida)

s.close()  # close the socket connection
