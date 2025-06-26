import os
from datetime import datetime , timedelta
from typing import Any, Dict

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import models, schemas

load_dotenv('.env')

SECRET_KEY = os.getenv("JWT_SECRET", "123")
ALGORYTHM = os.getenv("JWT_ALGORYTHM" , "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# Hache un mot de passe en clair en utilisant bcrypt via PassLib pour le stocker de façon sécurisée
def get_password_hash(password:str)-> str:
    return pwd_context.hash(password)


# Crée un JWT signé avec l'objet `data` enrichi de la date d'expiration (‘exp’) pour authentifier l’utilisateur de façon sécurisée.
def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)
    return encoded_jwt

# Vérifie qu’un mot de passe en clair correspond au hash stocké en utilisant PassLib (renvoie True si concordance)
def verify_password(plain_password:str, password:str)->bool:
    return pwd_context.verify(plain_password, password)


 # Inscrit un nouvel utilisateur (username/email) avec mot de passe haché, gère le commit et renvoie un JWT en cas de succès
def register_user(user_in:schemas.UserCreate, db: Session):
    existing = db.query(models.User).filter(
        (models.User.username == user_in.username) | (models.User.email==user_in.email)
    ).first()
    if existing:
        raise  ValueError("Username or password already exists")
    
    user = models.User(
        username = user_in.username,
        email = user_in.email,
        password = get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return{"access_token": token, "token_type":"bearer"}
   
   
  
 # Authentifie l'utilisateur en vérifiant l'existence du username et correspondance du mot de passe, puis renvoie un JWT
def login_user(user_in:schemas.UserLogin, db:Session):
    user = db.query(models.User).filter(models.User.username== user_in.username).first()
    if not user or not verify_password(user_in.password, user.password):
        raise ValueError ("Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return{"access_token": token, "token_type":"bearer"} 