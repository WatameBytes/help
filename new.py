# Adjust scale factor to 0.45 (45% of original size)
scale_factor = 0.45
new_size = (int(frames[0].width * scale_factor), int(frames[0].height * scale_factor))

# Resize all frames properly to prevent ghosting
resized_frames = [frame.resize(new_size, Image.Resampling.LANCZOS) for frame in frames]

# Save the resized GIF without compression
output_path = "tetris_resized_45_no_compress.gif"
resized_frames[0].save(
    output_path,
    save_all=True,
    append_images=resized_frames[1:],
    transparency=0,  # Ensures transparency remains correct
    loop=0,  # Keeps the GIF looping
    disposal=2  # Prevents ghost frames by clearing each frame before drawing the next
)

# Return the output file path
output_path




# Reprocess GIF to fix flickering black background issue
output_path = "tetris_resized_45_fixed.gif"

# Ensure transparency is handled correctly
resized_frames[0].save(
    output_path,
    save_all=True,
    append_images=resized_frames[1:],
    transparency=0,  # Ensure transparency remains intact
    loop=0,  # Keeps the GIF looping
    disposal=3  # Use disposal method 3 to prevent flickering
)

# Return the output file path
output_path











GyTatq4qSFDN7fdlV1o366oBYbvKemFbGi4IXhchgiY


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
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

# Encryption process
def encrypt_file():
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

# Decryption process
def decrypt_file():
    try:
        with open('encoded.txt', 'rb') as f:
            # Read salt and IV from the file
            salt = f.read(16)
            iv = f.read(16)
            encrypted_data = f.read()

        # Generate the key using the same password and salt
        password = b"supersecretpassword"  # Must be the same as used in encryption
        key = generate_key(password, salt)

        # Decrypt the data
        decrypted_secret = decrypt_data(encrypted_data, key, iv)

        # Write decrypted secret to decoded.txt
        with open('decoded.txt', 'wb') as f:
            f.write(decrypted_secret)

        print("Decryption complete. The secret is written to decoded.txt.")

    except FileNotFoundError:
        print("No encoded.txt file found. Please encrypt the data first.")
    except Exception as e:
        print(f"An error occurred during decryption: {e}")

# Main function to choose between encrypting and decrypting
if __name__ == "__main__":
    choice = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()

    if choice == 'encrypt':
        encrypt_file()
    elif choice == 'decrypt':
        decrypt_file()
    else:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")
