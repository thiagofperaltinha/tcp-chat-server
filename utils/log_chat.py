import datetime
# Function chat log
def chat_log(username, mensagem):
    with open("chat.txt", "a") as f:
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{data}] {username}:{mensagem}\n")
    
    