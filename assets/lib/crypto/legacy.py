import base64
import hashlib
import os
try:
    from cryptography.fernet import Fernet
except:
    os.system("python3 -m pip install cryptography")
    from cryptography.fernet import Fernet

def encdec(key, inputs=str(), mode=str()):
    # Create a Fernet object with the key
    fernet = Fernet(key)
    # Convert input to bytes
    input_bytes = inputs.encode()
    if mode == "enc":
        # Encrypt input and return as a string
        encrypted = fernet.encrypt(input_bytes)
        return encrypted.decode()
    elif mode == "dec":
        # Decrypt input and return as a string
        decrypted = fernet.decrypt(input_bytes)
        return decrypted.decode()


def encdec_dict(key, dictionary=dict(), mode=str()):
    # Create a Fernet object with the key
    fernet = Fernet(key)
    # Iterate over each key-value pair in the dictionary
    result_dict = {}
    for k, v in dictionary.items():
        # Convert key and value to bytes
        k_bytes = k.encode()
        v_bytes = v.encode() if isinstance(v, str) else v
        if mode == 'enc':
            # Encrypt the key and value
            encrypted_k = fernet.encrypt(k_bytes).decode()
            encrypted_v = fernet.encrypt(v_bytes).decode()
            # Add the encrypted key-value pair to the encrypted dictionary
            result_dict[encrypted_k] = encrypted_v
        elif mode == 'dec':
            # Decrypt the key and value
            decrypted_k = fernet.decrypt(k_bytes).decode()
            decrypted_v = fernet.decrypt(v_bytes).decode()
            # Add the decrypted key-value pair to the decrypted dictionary
            result_dict[decrypted_k] = decrypted_v
    return result_dict

def GenerateKey(key_str=str()):
    # Convert the string key to bytes
    key_bytes = key_str.encode()
    # Use SHA256 to generate a 32-byte key
    key = hashlib.sha256(key_bytes).digest()
    # Encode the key using URL-safe Base64 encoding
    key_b64 = base64.urlsafe_b64encode(key)
    return key_b64