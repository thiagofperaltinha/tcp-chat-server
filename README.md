# 💬 Chat Client-Server Python

Um projeto simples de **chat em tempo real** utilizando **Python** com **sockets TCP**.

## ✨ Funcionalidades

- Comunicação bidirecional entre cliente e servidor
- Troca de mensagens em tempo real
- Comando especial `exit chat` para encerrar a conversa
- Mensagem de boas-vindas e resposta a comandos como `Serviços`

## 🛠 Tecnologias Utilizadas

- Python 3.x
- Módulo `socket` (nativo)

## 📦 Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/thiagofperaltinha/tcp-chat-server
   cd chat-client-server-python

🔧 Melhorias Futuras

- [x] Permitir múltiplos clientes se conectarem ao mesmo tempo (uso de threads)
- [ ] Interface gráfica (GUI) com Tkinter ou PyQt
- [ ] Criptografia básica das mensagens com SSL ou biblioteca `cryptography`
- [ ] Registro de logs de conversas
- [x] Comando `/help` com lista de funcionalidades disponíveis
- [x] Suporte a nomes de usuário personalizados
- [x] Mensagens de sistema (ex: entrada/saída de usuários)
- [ ] Melhor tratamento de erros e reconexão automática
- [ ] Implementação da versão UDP para fins comparativos

🇺🇸 English Version

# 💬 Chat Client-Server Python

A simple real-time chat project using Python with TCP sockets.

✨ Features

- Bidirectional communication between client and server
- Real-time message exchange
- Special command ` <exit chat> ` to end the conversation
- Welcome message and response to commands like ` <Service> `

🛠 Technologies Used

- Python 3.x
- Native `socket` module

📦 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/thiagofperaltinha/tcp-chat-server
   cd chat-client-server-python
   ```

2. Run the server:
   ```bash
   python servidor.py
   ```

3. Open another terminal and run the client:
   ```bash
   python cliente.py
   ```

🔧 Future Improvements

- [x] Allow multiple clients simultaneously (with threading)
- [ ] GUI interface using Tkinter or PyQt
- [ ] Basic encryption with SSL or `cryptography` lib
- [ ] Chat log registration
- [x] `/help` command for available features
- [x] Support for custom usernames
- [x] System messages (user joined/left notifications)
- [ ] Better error handling and auto-reconnection
- [ ] Implement a UDP version for learning comparison

