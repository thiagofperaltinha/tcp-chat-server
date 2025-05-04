# 💬 Chat Client-Server Python

A simple real-time chat project using Python with TCP sockets.
A secure and lightweight real-time chat system built in Python using raw TCP sockets and RSA encryption.

## ✨ Features

- End-to-end encryption using RSA for secure communication  
- Bidirectional real-time chat between server and multiple clients  
- Smart commands like `/help`, `/service` and username identification  
- Custom usernames with name validation and blacklist support  
- Chat logging to file for later reference  
- Multithreaded server — supports multiple clients simultaneously  
- Graceful disconnection using the `<exit chat>` command  
- Improved error handling to keep sessions stable

## 🔐 Security

- Public and private key pairs are generated per client and server session  
- Messages are encrypted before being sent, using the server/client public key  
- RSA-based encryption is handled with the `cryptography` library or `rsa` module

🛠 Technologies Used

- Python 3.x
- Native `socket` module
- - `rsa` library for encryption  
- `threading` module for concurrency

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
- [x] Basic encryption with SSL or `cryptography` lib
- [x] Chat log registration
- [x] `/help` command for available features
- [x] Support for custom usernames
- [x] System messages (user joined/left notifications)
- [x] Better error handling and auto-reconnection


Portuguese version

# 💬 Chat Client-Server Python

Um sistema de chat em tempo real, seguro e leve, desenvolvido em Python utilizando sockets TCP puros e criptografia RSA.

## ✨ Funcionalidades

- Criptografia ponta-a-ponta com RSA para uma comunicação segura  
- Chat bidirecional em tempo real entre servidor e múltiplos clientes  
- Comandos inteligentes como `/help`, `/service` e identificação de usuários  
- Suporte a nomes de usuário personalizados com validação e blacklist  
- Registro de logs do chat em arquivo para referência futura  
- Servidor multithread — suporta múltiplos clientes simultaneamente  
- Desconexão graciosa usando o comando `<exit chat>`  
- Tratamento de erros aprimorado para manter sessões estáveis

## 🛠 Tecnologias Utilizadas

- Python 3.x
- Módulo `socket` (nativo)

## 📦 Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/thiagofperaltinha/tcp-chat-server
   cd chat-client-server-python

2. Inicie o servidor:
   ```bash
   python servidor.py
   ```

3. Em outro/outros terminais inicie o cliente:
   ```bash
   python cliente.py
   ```

🔧 Melhorias Futuras

- [x] Permitir múltiplos clientes se conectarem ao mesmo tempo (uso de threads)
- [ ] Interface gráfica (GUI) com Tkinter ou PyQt
- [x] Criptografia básica das mensagens com SSL ou biblioteca `cryptography`
- [x] Registro de logs de conversas
- [x] Comando `/help` com lista de funcionalidades disponíveis
- [x] Suporte a nomes de usuário personalizados
- [x] Mensagens de sistema (ex: entrada/saída de usuários)
- [x] Melhor tratamento de erros e reconexão automática



