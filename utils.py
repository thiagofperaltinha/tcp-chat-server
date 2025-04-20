def verificar_msg_recebida(mensagem_recebida):
    if mensagem_recebida == "exit chat":
        return True
    return False

def verificar_msg_enviada(s, mensagem_enviada):
    if mensagem_enviada == "exit chat":
        verifi = input("Are you sure you want to end this chat? To confirm type: <yes>")
        if verifi == "yes":
            print("Connection closed.")
            s.send(mensagem_enviada.encode())
            return True
        else:
            print("Exit cancelled. Continuing chat...")
            return False
    return False

# If client requests services, show a service message
#conn.send("You have accessed a chat server. Soon, new clients will be added to interact with you!".encode()) if mensagem_recebida == "Serviços" else None