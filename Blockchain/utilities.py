import hashlib

def sha256_digest(data: bytes) -> bytes:
    #Create SHA-256 hash from byte data
    #Return bytes
    return hashlib.sha256(data).digest()

def int_to_bytes(n: int, length: int = 8) -> bytes:
    #Convert integers into byte with a fixed length of 8
    return n.to_bytes(length, byteorder='big')

def encode_hex(b: bytes) -> str:
    #Convert bytes into Hex strings
    return b.hex()

