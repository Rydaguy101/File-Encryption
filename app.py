from cryptography.fernet import Fernet
import os
import sys

# Files to skip during encryption/decryption
# These files are either the script itself or configuration files that should not be encrypted
skip = ["app.py", "key.txt",".gitignore","README.md"]

def generate_key():
    return Fernet.generate_key()

#  Load the encryption key from a file, or generate a new one if it doesn't exist
def load_key():
    if not os.path.exists("key.txt"):
        key = generate_key()
        with open("key.txt", "wb") as key_file:
            key_file.write(key)
        print("[INFO] New encryption key generated and saved to key.txt.")
    else:
        print("[INFO] key.txt already exists. Using existing key.")
    with open("key.txt", "rb") as key_file:
        return key_file.read()

# Encrypts a single file
def encrypt_file(filename, key):
    try:
        with open(filename, "rb") as file:
            data = file.read()
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        print(f"[SUCCESS] {filename} encrypted.")
    except Exception as e:
        print(f"[ERROR] Failed to encrypt {filename}: {e}")

# Decrypts a single file
def decrypt_file(filename, key):
    try:
        with open(filename, "rb") as file:
            data = file.read()
        f = Fernet(key)
        decrypted_data = f.decrypt(data)
        with open(filename, "wb") as file:
            file.write(decrypted_data)
        print(f"[SUCCESS] {filename} decrypted.")
    except Exception as e:
        print(f"[ERROR] Failed to decrypt {filename}: {e}")

# Encrypts all files in current and subdirectories
def process_all_files(key, action):
    processed = 0
    for fname in os.listdir():
        if fname not in skip and os.path.isfile(fname):
            if action == "encrypt":
                encrypt_file(fname, key)
            elif action == "decrypt":
                decrypt_file(fname, key)
            processed += 1
        elif os.path.isdir(fname):
            for root, dirs, files in os.walk(fname):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.basename(file_path) not in skip:
                        if action == "encrypt":
                            encrypt_file(file_path, key)
                        elif action == "decrypt":
                            decrypt_file(file_path, key)
                        processed += 1
    if processed == 0:
        print("[INFO] No files found to process.")
    else:
        print(f"[INFO] {processed} file(s) processed.")

# Handles command line arguements 
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python app.py [encrypt|decrypt] [A|S] [filename (if S)]")
        sys.exit(1)

    action = sys.argv[1].lower()
    mode = sys.argv[2].upper()
    key = load_key()

    if action not in ["encrypt", "decrypt"]:
        print("[ERROR] Invalid action. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)

    if mode == "A":
        print(f"[INFO] Processing all files in directory and subdirectories with action '{action}'.")
        process_all_files(key, action)
    elif mode == "S":
        if len(sys.argv) < 4:
            print("[ERROR] Please provide at least one filename for specific mode.")
            sys.exit(1)
        filenames = sys.argv[3:]
        missing_files = [f for f in filenames if not os.path.exists(f)]
        if missing_files:
            for f in missing_files:
                print(f"[ERROR] File '{f}' does not exist.")
        for filename in filenames:
            if action == "encrypt":
                encrypt_file(filename, key)
            elif action == "decrypt":
                decrypt_file(filename, key)
        print(f"[INFO] {len(filenames)} file(s) processed in specific mode.")
    else:
        print("[ERROR] Invalid mode. Use 'A' for all or 'S' for specific file(s).")