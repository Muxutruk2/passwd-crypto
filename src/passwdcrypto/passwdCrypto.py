from cryptography.fernet import Fernet
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

global currentDir
currentDir = os.getcwd()

def generate_key_from_password(password: bytes) -> Fernet:
    """Generate a Fernet key derived from the provided password.

    Args:
        password (bytes): The password used to derive the key.

    Returns:
        Fernet: The Fernet key derived from the password.
    """
    # Generate a salt (random value)
    salt = b'\xf1\xdc\x96\xdf\x1eQ\xcf\xc9\x82\xe6\x84h\x1c\xfa\xe4\x8a'

    # Create a PBKDF2HMAC key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=480000,  # You can adjust the number of iterations for security
        salt=salt,
        length=32  # The length of the key
    )

    # Derive the key from the password
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))

    return key

class Passwd():
    def __init__(self, filename: str, key: bytes) -> None:
        """Initialize Passwd instance.

        Args:
            filename (str): The name of the file to store encrypted passwords.
            key (bytes): The Fernet key used for encryption and decryption.
        """
        self.filename = filename
        self.absFilename = os.path.join(currentDir, filename)
        self.key = generate_key_from_password(key)

        if not os.path.exists(self.absFilename):
            open(self.absFilename, "w").close()

    def getEncryptedPasswds(self) -> list[bytes]:
        """Retrieve encrypted passwords from the file.

        Returns:
            list[bytes]: List of encrypted passwords.
        """
        with open(self.absFilename, "rb") as file:
            lines = file.read().splitlines()

        return lines

    def read(self) -> list[list[str]]:
        """Decrypt and read the stored passwords from the file.

        Returns:
            list: List of decrypted password entries. Which are itself a list where: 
                [0]: App
                [1]: Email
                [2]: Password
        """
        encryptedLines = self.getEncryptedPasswds()
        output = []

        for line in encryptedLines:
            decrypted_line = self.key.decrypt(line).decode()
            output.append(decrypted_line.split(","))

        return output

    def encrypt(self, text: str) -> bytes:
        """Encrypt the given text using the Fernet key.

        Args:
            text (str): The text to be encrypted.

        Returns:
            bytes: The encrypted text.
        """
        return self.key.encrypt(text.encode())

    def write(self, app: str, email: str, password: str) -> None:
        """Encrypt and write a new password entry to the file.

        Args:
            app (str): The application or service name.
            email (str): The associated email address.
            password (str): The password for the application or service.
        """
        text = f"{app},{email},{password}"
        encrypted_text = self.encrypt(text)

        with open(self.absFilename, "ab") as file:
            file.write(encrypted_text + b"\n")
