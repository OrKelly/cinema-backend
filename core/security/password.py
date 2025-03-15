import random
import secrets
import string

from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify(cls, hashed_password: str, password_to_verify: str) -> bool:
        return cls.pwd_context.verify(password_to_verify, hashed_password)

    @classmethod
    def generate_password(cls, length=8):
        characters = (
            string.ascii_letters + string.digits + string.ascii_uppercase
        )
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
        ]
        password += [secrets.choice(characters) for _ in range(length - 3)]
        random.shuffle(password)
        return "".join(password)
