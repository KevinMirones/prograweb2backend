# database.py
from dataclasses import dataclass
from typing import Annotated
from fastapi.params import Depends
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL for MySQL
HOST_DB = os.getenv("HOST_DB")
PORT_DB = os.getenv("PORT_DB")
NAME_DB = os.getenv("NAME_DB")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")

if not all([HOST_DB, PORT_DB, NAME_DB, USER_DB, PASSWORD_DB]):
    missing = [var for var in ["HOST_DB", "PORT_DB", "NAME_DB", "USER_DB", "PASSWORD_DB"] if not os.getenv(var)]
    raise ValueError(f"Missing environment variables: {', '.join(missing)}")

DATABASE_URL = f"postgresql+psycopg2://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

# Contexto de request
@dataclass
class RequestContext:
    current_session: Session

# Dependencia para obtener el contexto
def get_context(current_session: Session = Depends(get_db)) -> RequestContext:
    return RequestContext(current_session=current_session)

# Alias para usar como dependencia en rutas
CurrentContext = Annotated[RequestContext, Depends(get_context)]