from database import DbSessionHandler
from fastapi import FastAPI
handler = DbSessionHandler()
db = handler.get_db()