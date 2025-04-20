import socket

ip = '127.0.0.1'
port = 3000

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

s.bind((ip, port))

s.listen(1)

conn, addr = s.accept()  # accepts the connection, removing it from the listening queue

print("Connection from %s: %d" %(addr[0], addr[1]))
conn.send(b"Welcome to my TCP server, client number 1!\n A")

while True:
    mensagem_recebida = conn.recv(1024).decode()  # receives what the user sends (up to 1024 bytes)
    
    if mensagem_recebida == "exit chat":  # if the received message is "sair chat", it breaks the loop and ends the chat
        print("Connection closed by the client.")
        break
    
    print("Client: ", mensagem_recebida)  # displays the message sent by the client
    
    # If client requests services, show a service message
    conn.send("You have accessed a chat server. Soon, new clients will be added to interact with you!".encode()) if mensagem_recebida == "Serviços" else None

    mensagem_enviada = input("You: ")
    if mensagem_enviada == "exit chat":
        print("Connection closed by the server.")
        break
    
    conn.send(mensagem_enviada.encode())

conn.close()
s.close()  # closing the server socket
