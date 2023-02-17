import base64
import hashlib
import os
try:
    import pyaes
except:
    os.system("python3 -m pip install pyaes")
    import pyaes

def encdec_b64(inputs,mode=str()):
    if mode == "enc":
        return base64.b64encode(inputs.encode()).decode()
    elif mode == "dec":
        return base64.b64decode(inputs).decode()
    elif mode == "enc-byte":
        return base64.b64encode(inputs).decode()
    elif mode == "dec-byte":
        return base64.b64decode(inputs)

def encdec(key, inputs, mode=str()):
    # Create a aes object with the key
    aes = pyaes.AESModeOfOperationCTR(key)
    if mode == "enc":
        # Encrypt input
        encrypted = aes.encrypt(inputs)
        # Return as base64 string
        return encdec_b64(encrypted,"enc-byte")
    elif mode == "dec":
        # Convert from base64
        inputs = encdec_b64(inputs,"dec-byte")
        # Decrypt input
        decrypted = aes.decrypt(inputs)
        # Return content as string
        return decrypted.decode("latin-1").encode("utf-8").decode("utf-8")

def encdec_dict(key, dictionary=dict(), mode=str()):
    # Create a aes object with the key
    aes = pyaes.AESModeOfOperationCTR(key)
    # Iterate over each key-value pair in the dictionary
    result_dict = {}
    for dict_key, dict_value in dictionary.items():
        if mode == 'enc':
            # Encrypt the key and value
            encrypted_key = encdec(key,dict_key,"enc")
            encrypted_value = encdec(key,dict_value,"enc")
            # Handle ' in key/value
            if "'" in encrypted_key:
                encrypted_key = encrypted_key.replace("'","%sit%")
            if "'" in encrypted_value:
                encrypted_value = encrypted_value.replace("'","%sit%")
            # Add the encrypted key-value pair to the encrypted dictionary
            result_dict[encrypted_key] = encrypted_value
        elif mode == 'dec':
            # Handle ' in key/value
            if "'" in dict_key:
                dict_key = dict_key.replace("'","%sit%")
            if "'" in dict_value:
                dict_value = dict_value.replace("'","%sit%")
            # Decrypt the key and value
            decrypted_key = encdec(key,dict_key,"dec")
            decrypted_value = encdec(key,dict_value,"dec")
            # Add the decrypted key-value pair to the decrypted dictionary
            result_dict[decrypted_key] = decrypted_value
    return result_dict

def GenerateKey(key_str=str()):
    # Convert the string key to bytes
    key_bytes = key_str.encode()
    # Use SHA256 to generate a 32-byte key
    key = hashlib.sha256(key_bytes).digest()
    # Encode the key using URL-safe Base64 encoding
    key_b64 = base64.urlsafe_b64encode(key)
    return key
