
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")

class Hash():
    def bcrypt(password):
        return pwd_cxt.hash(password)
    
    def verify(hashed_password, plain_passowrd):
        return pwd_cxt.verify(plain_passowrd, hashed_password)