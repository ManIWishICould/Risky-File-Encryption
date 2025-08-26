import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend


def derive_key(passphrase: str, salt_file: str = "salt.bin") -> bytes:
    """Derive a 256-bit key from ``passphrase``.

    A 16-byte salt is stored in ``salt_file`` so the same passphrase
    produces the same key between runs.
    """
    if os.path.exists(salt_file):
        with open(salt_file, "rb") as fh:
            salt = fh.read()
    else:
        salt = os.urandom(16)
        with open(salt_file, "wb") as fh:
            fh.write(salt)

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
        backend=default_backend(),
    )
    return kdf.derive(passphrase.encode("utf-8"))