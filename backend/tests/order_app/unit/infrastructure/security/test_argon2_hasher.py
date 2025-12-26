from order_app.infrastructure.security.argon2_hasher import Argon2PasswordHasher


def test_hash_password():
    hasher = Argon2PasswordHasher()
    password = "password123"
    hashed = hasher.hash(password)
    assert hasher.verify(password, hashed)
