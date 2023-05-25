# Libhasher 1.0 by Simon Kalmi Claesson

import hashlib

# Functions for hashing files
def hashFile(filepath: str, hashType: str) -> str:
    """
    Computes the hash of a file using the specified hash type.
    Arguments:
      filepath: The path of the file to hash.
      hashType: The hash algorithm to use (e.g. 'sha256', 'md5', etc.).
    Returns:
      String containing the hash
    Algortithms:
      md5: MD5 message digest algorithm
      sha1: SHA-1 hash algorithm
      sha224: SHA-224 hash algorithm
      sha256: SHA-256 hash algorithm
      sha384: SHA-384 hash algorithm
      sha512: SHA-512 hash algorithm
      blake2b: BLAKE2b hash algorithm (512-bit)
      blake2s: BLAKE2s hash algorithm (256-bit)
      sha3_224: SHA-3 hash algorithm with 224-bit output
      sha3_256: SHA-3 hash algorithm with 256-bit output
      sha3_384: SHA-3 hash algorithm with 384-bit output
      sha3_512: SHA-3 hash algorithm with 512-bit output
    """
    with open(filepath, 'rb') as f:
        data = f.read()
        hashFunc = hashlib.new(hashType)
        hashFunc.update(data)
        return hashFunc.hexdigest()

# Function for hashing strings
def hashString(message: str, hashType: str, encoding="utf-8") -> str:
    """
    Computes the hash of a string using the specified hash type.
    Arguments:
      message: The string to hash.
      hashType: The hash algorithm to use (e.g. 'sha256', 'md5', etc.).
    Returns:
      String containing the hash
    Algortithms:
      md5: MD5 message digest algorithm
      sha1: SHA-1 hash algorithm
      sha224: SHA-224 hash algorithm
      sha256: SHA-256 hash algorithm
      sha384: SHA-384 hash algorithm
      sha512: SHA-512 hash algorithm
      blake2b: BLAKE2b hash algorithm (512-bit)
      blake2s: BLAKE2s hash algorithm (256-bit)
      sha3_224: SHA-3 hash algorithm with 224-bit output
      sha3_256: SHA-3 hash algorithm with 256-bit output
      sha3_384: SHA-3 hash algorithm with 384-bit output
      sha3_512: SHA-3 hash algorithm with 512-bit output
    """
    data = message.encode(encoding)
    hashFunc = hashlib.new(hashType)
    hashFunc.update(data)
    return hashFunc.hexdigest()