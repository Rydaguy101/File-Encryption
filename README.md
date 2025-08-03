# File Encryptor / Decryptor

A simple Python script to encrypt or decrypt files using `Fernet`.

## 🔐 How It Works

- Generates a symmetric encryption key and stores it in `key.txt` (excluded from Git).
- Supports encrypting or decrypting:
  - **All** files in the current directory and subdirectories
  - **Specific** files you specify

## ⚠️ WARNING

This is a **basic utility for learning or light personal use**. Do **not** use it to secure highly sensitive or production data.

Never commit your `key.txt` file. If someone gets your key, they can decrypt your data.

---

## 🚀 Usage

```bash
python app.py [encrypt|decrypt] [A|S] [filename1 filename2 ... (if S)]
