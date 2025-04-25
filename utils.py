import threading

print_lock = threading.Lock()
encerrando = False
clientes_info = {}
nomes_proibidos = ["", "server", "Server", "SERVER", "servidor", "SERVIDOR", " "]

# Checks if the client sent the exit command
def verificar_msg_recebida(mensagem_recebida):
    return mensagem_recebida.strip().lower() == "exit chat"

# Checks if the server wants to end the chat and confirms with the user
def verificar_msg_enviada(s, mensagem_enviada):
    global encerrando
    if mensagem_enviada.strip().lower() == "exit chat":
        verifi = input("❗ Are you sure you want to end this chat? To confirm, type: <yes> ").strip().lower()
        if verifi == "yes":
            encerrando = True
            print("🔒 Connection closed.")
            try:
                s.send(mensagem_enviada.encode())
            except:
                pass
            return True
        else:
            print("❌ Exit cancelled. Continuing chat...")
            return False
    return False

# Thread responsible for receiving server messages
def receber_mensagens(s):
    while True:
        try:
            mensagem_recebida = s.recv(1024).decode()
            if verificar_msg_recebida(mensagem_recebida):
                break
            with print_lock:
                print(f"{mensagem_recebida}")
                print( "(You): ", end="", flush=True)
        except:
            if not encerrando:
                print("⚠️ Error receiving message.")
            break

# Function to validate a unique and acceptable username
def user_name(nome_usuario, clientes_info, nomes_proibidos, s):
    if (nome_usuario in nomes_proibidos) or not nome_usuario.strip():
        novo_nome = input("❗ Invalid username. Please enter a valid one: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)
    if nome_usuario in clientes_info.values():
        print("⚠️ Username already in use. Try another.")
        novo_nome = input("Please enter a valid username: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)

    s.send(f"<username>:{nome_usuario}".encode())
    clientes_info[s] = nome_usuario
    return nome_usuario

# Handles automatic command responses from the server
def comandos(mensagem_recebida, conn):
    msg = mensagem_recebida.lower()

    if msg == "<service>":
        conn.send("🛠️ You have accessed a chat server. Soon, new clients will be able to interact with you!".encode())
    elif msg == "<help>":
        help_msg = """
        [ AVAILABLE COMMANDS ]
----------------------------------
<Help>        → Show this help message.
<Service>     → Display information about the server's services.
<exit chat>   → Close your connection to the chat safely.     
"""
        conn.send(help_msg.encode())
