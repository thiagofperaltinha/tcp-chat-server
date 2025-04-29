def enviar_dados_tamanho(dados, s):
    tamanho = len(dados).to_bytes(4, byteorder="big")
    s.sendall(tamanho + dados)
    
def receber_dados_tamanho(s):
    tamanho_bytes = s.recv(4)
    
    if len(tamanho_bytes) < 4:
        raise ValueError("ERRO DE VALOR")
    
    tamanho = int.from_bytes(tamanho_bytes, byteorder="big")
    dado = b''
    while len(dado)<tamanho:
        res = s.recv(tamanho - len(dado))
        if not res:
            raise ValueError("ERRO DE VALOR")
        
        dado += res
    return dado