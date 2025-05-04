import threading
from utils.crypto import descripto_mesage, cripto_mesage
from utils.cont_bytes import receber_dados_tamanho, enviar_dados_tamanho

# Lock to prevent concurrent terminal prints
print_lock = threading.Lock()

# Flag to indicate if the client is exiting
encerrando = False

# Dictionary to store client socket and corresponding username
clientes_info = {}

# List of forbidden usernames
nomes_proibidos = ["", "server", "Server", "SERVER", "servidor", "SERVIDOR", " "]

# Checks if the client sent the command to exit the chat
def verificar_msg_recebida(mensagem_recebida):    
    return mensagem_recebida.lower() == "exit chat*"

# Handles the exit command from the client and closes the connection
def verificar_msg_enviada(s, mensagem_enviada, public_key_server):
    global encerrando
    if mensagem_enviada.lower().strip() == "exit chat*":
        encerrando = True
        print("🔒 Connection closed.")
        try:
            msg_enviada = cripto_mesage(mensagem_enviada, public_key_server)
            enviar_dados_tamanho(msg_enviada, s)
        except:
            pass
        return True
    return False 

# Thread function to receive and display messages from the server
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

# Validates the user's name, ensuring it is not forbidden or already in use
def user_name(nome_usuario, clientes_info, nomes_proibidos, s, server_p_key):
    if (nome_usuario in nomes_proibidos) or not nome_usuario.strip():
        novo_nome = input("⚠️ Invalid username. Please enter a valid one: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)
    if nome_usuario in clientes_info.values():
        print("⚠️ Username already in use. Try another.")
        novo_nome = input("Please enter a valid username: ")
        return user_name(novo_nome, nomes_proibidos, clientes_info, s)

    mensagem_crip = cripto_mesage(f"<username>:{nome_usuario}", server_p_key)
    enviar_dados_tamanho(mensagem_crip, s)
    clientes_info[s] = nome_usuario
    return nome_usuario

# Responds to basic server commands (service/help)
def comandos(mensagem_recebida, conn, public_key):
    msg = mensagem_recebida.lower()
    if msg == "service*":
        service_msg = "🛠️ This is a secure chat server. More features coming soon!"
        try:
            service_crip = cripto_mesage(service_msg, public_key)
            enviar_dados_tamanho(service_crip, conn)
        except Exception as e:
            print(f"ERROR while sending service* command: {e}")

    elif msg == "help*":
        help_msg = (
            "[Commands]\n"
            " Help*     → Show help.\n"
            " Service*  → Server info.\n"
            " exit chat*→ Disconnect."
        )
        try:
            help_crip = cripto_mesage(help_msg, public_key)
            enviar_dados_tamanho(help_crip, conn)
        except Exception as e:
            print(f"ERROR while sending help* command: {e}")
