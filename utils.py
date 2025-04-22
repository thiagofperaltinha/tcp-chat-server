import threading
print_lock = threading.Lock()
encerrando = False
 
def verificar_msg_recebida(mensagem_recebida):
    if mensagem_recebida == "exit chat":
        return True
    return False

def verificar_msg_enviada(s, mensagem_enviada):
    if mensagem_enviada == "exit chat":
        global encerrando
        verifi = input("Are you sure you want to end this chat? To confirm type: <yes> ")
        if verifi == "yes":
            encerrando = True
            print("Connection closed.")
            s.send(mensagem_enviada.encode())
            return True
        else:
            print("Exit cancelled. Continuing chat...")
            return False
    return False

def receber_mensagens(s):
    while True:
        try:
            mensagem_recebida = s.recv(1024).decode()
            if verificar_msg_recebida(mensagem_recebida):
                break
            with print_lock:
                print(f"\nServer: {mensagem_recebida}")
                print("You: ", end="", flush=True)
                
            if mensagem_recebida.lower() == "Service":
                s.send("You have accessed a chat server. Soon, new clients will be added to interact with you!".encode())
        except:
            if not encerrando:
                print("Error receiving message.")
            break
        

# If client requests services, show a service message
#conn.send("You have accessed a chat server. Soon, new clients will be added to interact with you!".encode()) if mensagem_recebida == "Serviços" else None