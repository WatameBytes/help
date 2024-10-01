from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
import os

# Generate a secure key using a password and salt
def generate_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    return kdf.derive(password)

# Function to encrypt data using AES
def encrypt_data(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    return encryptor.update(padded_data) + encryptor.finalize()

# Function to decrypt data using AES
def decrypt_data(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()

# Create decoded.txt if it doesn't exist and write a secret
if not os.path.exists('decoded.txt'):
    with open('decoded.txt', 'w') as f:
        f.write('This is a top secret message!')

# Read the secret from decoded.txt
with open('decoded.txt', 'rb') as f:
    secret = f.read()

# Set up encryption parameters
password = b"supersecretpassword"  # Use a strong password
salt = os.urandom(16)  # Random salt
key = generate_key(password, salt)
iv = os.urandom(16)  # Initialization vector

# Encrypt the secret
encrypted_secret = encrypt_data(secret, key, iv)

# Write encrypted data to encoded.txt
with open('encoded.txt', 'wb') as f:
    f.write(salt + iv + encrypted_secret)

print("Encryption complete. The secret is written to encoded.txt.")