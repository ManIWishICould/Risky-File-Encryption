# Risky File Encryption

A minimal drag-and-drop desktop app that encrypts or decrypts files in place.
Dropping a file onto the left side encrypts it with AES-GCM, while dropping a
file on the right side attempts to decrypt it using the provided passphrase.

**Warning:** once a file is overwritten, the original content cannot be
recovered without the passphrase. Make backups before using this tool.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

The window is split into two halves: drag files onto the left to encrypt or onto
the right to decrypt. You will be prompted for a passphrase used to derive the
key; the file contents will be replaced with the resulting encrypted or
decrypted data.