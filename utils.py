import threading

print_lock = threading.Lock()
encerrando = False
nome_clientes = []
nomes_proibidos = ["", "Server".lower()]

# Verifica se o cliente enviou o comando para encerrar o chat
def verificar_msg_recebida(mensagem_recebida):
    return mensagem_recebida.strip().lower() == "exit chat"

# Verifica se o servidor quer encerrar e confirma com o usuário
def verificar_msg_enviada(s, mensagem_enviada):
    global encerrando
    if mensagem_enviada.strip().lower() == "exit chat":
        verifi = input("Are you sure you want to end this chat? To confirm type: <yes> ").strip().lower()
        if verifi == "yes":
            encerrando = True
            print("Connection closed.")
            try:
                s.send(mensagem_enviada.encode())
            except:
                pass
            return True
        else:
            print("Exit cancelled. Continuing chat...")
            return False
    return False

# Thread responsável por receber mensagens do servidor
def receber_mensagens(s):
    while True:
        try:
            mensagem_recebida = s.recv(1024).decode()
            if verificar_msg_recebida(mensagem_recebida):
                break
            with print_lock:
                print(f"\nServer: {mensagem_recebida}")
                print("You: ", end="", flush=True)
        except:
            if not encerrando:
                print("Error receiving message.")
            break
        
# Método responsável por exibir as mensagens automaticas correspondentes aos comandos utilizados no servidor
def comandos(mensagem_recebida, s):
    msg = mensagem_recebida.lower()

    if msg == "<Service>":
        resposta = "You have accessed a chat server. Soon, new clients will be added to interact with you!"
        try:
            s.send(resposta.encode())
        except:
            print("Erro ao exibir mensagem de Serviços")
            
    elif msg == "<Help>":
        with print_lock:
            print("\n📄 Available commands:")
            print("  - exit chat : ends the conversation.")
            print("  - Service   : see the current status of the chat server.")
            print("  - Help      : show this help message.\n")
            
            
def user_name (nome_usuario, nomes_proibidos, nome_clientes):
    if (nome_usuario in nomes_proibidos):
        novo_nome = input("Digite um nome de usuário válido: ")
        return user_name(novo_nome, nomes_proibidos, nome_clientes)
    elif nome_usuario in nome_clientes:
        print("Nome em uso, tente novamente.")
        novo_nome = input("Digite um nome de usuário válido: ")
        return user_name(novo_nome, nomes_proibidos, nome_clientes)
    else:
        nome_clientes.append(nome_usuario)
        return nome_usuario
           
        

# If client requests services, show a service message
#conn.send("You have accessed a chat server. Soon, new clients will be added to interact with you!".encode()) if mensagem_recebida == "Serviços" else None