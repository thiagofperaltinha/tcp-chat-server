import socket
import threading
from utils import verificar_msg_enviada, receber_mensagens, user_name, nome_clientes, nomes_proibidos

# Server IP and port configuration
ip = '127.0.0.1'  # localhost
port = 3000

# Create the TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Welcome message from the server
welcome_message = s.recv(1024).decode()
print("╭────────────────────────────────────────────╮")
print(f"│ 📡 Server says: {welcome_message.strip()}")
print("╰────────────────────────────────────────────╯\n")

# Instructions for the user
print("╭────────────────────────────────────────────────────╮")
print("│ 📌 Type <help> to learn how to use the chat commands.")
print("╰────────────────────────────────────────────────────╯\n")

# Thread to receive messages from the server
thread_receber = threading.Thread(target=receber_mensagens, args=(s,))
thread_receber.start()

# Prompt for a valid username
nome_user = input("Enter a valid username: ")
verficar_nome = user_name(nome_user, nome_clientes, nomes_proibidos)

# Main message sending loop
while True:
    try:
        mensagem_enviada = input(f"{verficar_nome} (You): ")
        if verificar_msg_enviada(s, mensagem_enviada):
            break
        s.send(mensagem_enviada.encode())
    except:
        break

# Close the connection
s.close()
print("\n🔌 Disconnected from the server. Goodbye!")
