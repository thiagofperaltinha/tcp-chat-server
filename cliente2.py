import socket
import threading
from utils import verificar_msg_enviada, receber_mensagens, user_name, clientes_info, nomes_proibidos
from servidor import chat_log

# Server configuration
ip = '127.0.0.1'
port = 3000

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Welcome message from server
welcome_message = s.recv(1024).decode()
print("╭────────────────────────────────────────────╮")
print(f"│ 📡 Server says: {welcome_message.strip()}")
print("╰────────────────────────────────────────────╯\n")

# User instructions
print("╭──────────────────────────────────────────────────────╮")
print("│ 📌 Type <help> to view available chat commands.")
print("╰──────────────────────────────────────────────────────╯\n")

# Thread to receive messages
thread_receber = threading.Thread(target=receber_mensagens, args=(s,))
thread_receber.start()

# Request a username
nome_user = input("Enter a valid username: ")
verifi_nome = user_name(nome_user, clientes_info, nomes_proibidos, s)

# Main loop to send messages
while True:
    try:
        mensagem_enviada = input() 
        msg_verifi = verificar_msg_enviada(s, mensagem_enviada)
        if msg_verifi:
            break
        
        s.send(mensagem_enviada.encode())
        chat_log(verifi_nome, mensagem_enviada )
        
    except Exception as e:
        print(f" ERROR {e}")
        break
# Closing connection
s.close()
print("\n🔌 Disconnected from the server. Goodbye!")
