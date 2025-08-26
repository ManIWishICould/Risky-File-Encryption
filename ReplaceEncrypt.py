import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_and_replace(path: str, key: bytes) -> None:
    """Encrypt ``path`` in-place with AES-GCM."""
    with open(path, "rb") as fh:
        plaintext = fh.read()

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(path, "wb") as fh:
        fh.write(nonce + ciphertext)


def decrypt_and_replace(path: str, key: bytes) -> None:
    """Decrypt ``path`` in-place assuming it holds ``nonce`` + ciphertext."""
    with open(path, "rb") as fh:
        data = fh.read()

    if len(data) < 12:
        raise ValueError("File is too small to contain a nonce")

    nonce, ciphertext = data[:12], data[12:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(path, "wb") as fh:
        fh.write(plaintext)