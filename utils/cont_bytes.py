def enviar_dados_tamanho(dados, s):
    # Convert the length of the data to 4 bytes in big-endian order
    tamanho = len(dados).to_bytes(4, byteorder="big")
    # Send the length followed by the actual data
    s.sendall(tamanho + dados)
    
def receber_dados_tamanho(s):
    # Receive the first 4 bytes which contain the size of the data
    tamanho_bytes = s.recv(4)
    
    # If less than 4 bytes are received, raise an error
    if len(tamanho_bytes) < 4:
        raise ValueError("VALUE ERROR")
    
    # Convert the 4 bytes to an integer to get the data size
    tamanho = int.from_bytes(tamanho_bytes, byteorder="big")
    
    dado = b''  # Initialize an empty byte object to hold the received data
    
    # Keep receiving data until the full size is received
    while len(dado) < tamanho:
        res = s.recv(tamanho - len(dado))  # Receive remaining data
        if not res:
            # If no data is received, raise an error
            raise ValueError("VALUE ERROR")
        dado += res  # Add the received data to the 'dado' variable
    
    # Return the complete data
    return dado
