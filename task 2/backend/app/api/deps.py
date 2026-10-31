from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db


def get_db_dependency():
    return Depends(get_db)
