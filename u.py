import threading
from utils.crypto import descripto_mesage, cripto_mesage
from utils.cont_bytes import receber_dados_tamanho, enviar_dados_tamanho

print_lock = threading.Lock()
encerrando = False
clientes_info = {}
nomes_proibidos = ["", "server", "Server", "SERVER", "servidor", "SERVIDOR", " "]

# Checks if the client sent the exit command
def verificar_msg_recebida(mensagem_recebida):    
    return mensagem_recebida.lower() == "<exit chat>"

# Checks if the server wants to end the chat and confirms with the user
def verificar_msg_enviada(s, mensagem_enviada, public_key_server):
    global encerrando
    if mensagem_enviada.lower().strip() == "<exit chat>":
        encerrando = True
        print("🔒 Connection closed.")
        try:
            msg_enviada = cripto_mesage(mensagem_enviada, public_key_server)
            enviar_dados_tamanho(msg_enviada, s)
        except:
            pass
        return True
    return False 

# Thread responsible for receiving server messages
def receber_mensagens(s, private_key):
    while True:
        try:
            tam_dados = receber_dados_tamanho(s)
            mensagem_recebida = descripto_mesage(tam_dados, private_key)
            if verificar_msg_recebida(mensagem_recebida):
                break
            with print_lock:
               print(f"✉️ {mensagem_recebida}")
        except Exception as e:
            if not encerrando:
                print(f"⚠️ Error receiving message: {e}")
            break

# Function to validate a unique and acceptable username
def user_name(nome_usuario, clientes_info, nomes_proibidos, s, server_p_key):
    if (nome_usuario in nomes_proibidos) or not nome_usuario.strip():
        novo_nome = input("❗ Invalid username. Please enter a valid one: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)
    if nome_usuario in clientes_info.values():
        print("⚠️ Username already in use. Try another.")
        novo_nome = input("Please enter a valid username: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)

    mensagem_crip = cripto_mesage(f"<username>:{nome_usuario}", server_p_key)
    enviar_dados_tamanho(mensagem_crip, s)
    clientes_info[s] = nome_usuario
    return nome_usuario

# Handles automatic command responses from the server
def comandos(mensagem_recebida, conn, public_key):
    msg = mensagem_recebida.lower()
    
    if msg == "<service>":
       service_msg = "🛠️ You have accessed a chat server. Soon, new clients will be able to interact with you!"
       service_crip = cripto_mesage(service_msg, public_key)
       enviar_dados_tamanho(service_crip, conn)
    elif msg == "<help>":
        help_msg = """
        [ AVAILABLE COMMANDS ]
----------------------------------
<Help>        → Show this help message.
<Service>     → Display information about the server's services.
<exit chat>   → Close your connection to the chat safely.     
"""
        help_crip = cripto_mesage(help_msg, public_key)
        enviar_dados_tamanho(help_crip, conn)
