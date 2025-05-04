import rsa
# Function generate key
# Function cryptografy message
# Function decryptografy message
# Function serialize public key
# Function deserialize public key

def gerar_chave():
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key

def cripto_mesage(mensagem_enviada, public_key):
    return rsa.encrypt(mensagem_enviada.encode(), public_key)

def descripto_mesage(mensagem_cripto, private_key):
    return rsa.decrypt(mensagem_cripto, private_key).decode()

def serialize_public_key(public_key):
    return public_key.save_pkcs1(format='PEM')

def deserialize_public_key(key_bytes):
    return rsa.PublicKey.load_pkcs1(key_bytes, format='PEM')

