import socket
import threading
from u import verificar_msg_enviada, receber_mensagens, user_name, clientes_info, nomes_proibidos
from utils.crypto import cripto_mesage, serialize_public_key, deserialize_public_key, gerar_chave
from utils.log_chat import chat_log
from utils.cont_bytes import enviar_dados_tamanho, receber_dados_tamanho

# Server IP and port configuration
ip = '127.0.0.1'  # localhost
port = 3000

# Create the TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

public_key, private_key = gerar_chave()
enviar_dados_tamanho(serialize_public_key(public_key), s)

# Receber a chave pública do servidor
receber_tam_men = receber_dados_tamanho(s)
server_key = deserialize_public_key(receber_tam_men)

# Welcome message from the server
welcome_message = s.recv(1024).decode()
print("╭────────────────────────────────────────────╮")
print(f"│ 📡 Server says: {welcome_message.strip()}")
print("╰────────────────────────────────────────────╯\n")

# Instructions for the user
print("╭───────────────────────────────────────────────────────╮")
print("│ 📌 Type <help> to learn how to use the chat commands.")
print("╰───────────────────────────────────────────────────────╯\n")

# Thread to receive messages from the server
thread_receber = threading.Thread(target=receber_mensagens, args=(s, private_key))
thread_receber.start()

# Prompt for a valid username
nome_user = input("Enter a valid username: ")
verifi_nome = user_name(nome_user, clientes_info, nomes_proibidos, s)
booleano = True

# Main message sending loop
while True:
    try:
        mensagem_enviada = input()
        msg_env = verificar_msg_enviada(s, mensagem_enviada)
        if msg_env:
            break
            
        s.send(cripto_mesage(mensagem_enviada, server_key))
        chat_log(verifi_nome, mensagem_enviada)
    except EOFError:
        break

# Close the connection
s.close()
print("\n🔌 Disconnected from the server. Goodbye!")
