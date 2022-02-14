from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

test=get_password_hash("secret");
print(test)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
test2=verify_password("secret","$2b$12$WyED2UPuxMaku0NGqoEIY.BXa7nWnj3xYA7FZU24O8V5MBmcKZzuu")
print(test2)

test3=verify_password("secret","$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW")
print(test3)