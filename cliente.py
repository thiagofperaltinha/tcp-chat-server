import socket
import threading
from utils import verificar_msg_enviada, receber_mensagens, user_name, nome_clientes, nomes_proibidos

# Configuração de IP e porta
ip = '127.0.0.1'  # localhost
port = 3000

# Criação do socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Mensagem de boas-vindas do servidor
mensagem_boas_vindas = s.recv(1024).decode()
print(mensagem_boas_vindas)

# Instruções para o usuário
print("📌 Comandos disponíveis:")
print("  - <Service>: saber quais serviços o servidor oferece.")
print("  - <exit chat>: sair da sala de chat.\n")

# Thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens, args=(s,))
thread_receber.start()
nome_user = input("Digite um nome de usuário válido: ")
verficar_nome = user_name(nome_user, nome_clientes, nomes_proibidos)
    
# Loop principal para envio de mensagens
while True:
    try:
        
        mensagem_enviada = input(f"{verficar_nome}(You): ")
        if verificar_msg_enviada(s, mensagem_enviada):
            break
        s.send(mensagem_enviada.encode())
    except:
        break

# Encerramento da conexão
s.close()
