from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.base import Base
import models.garage
from routers import garages

# Създаване на таблици в базата данни
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Адресът на фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешава всички HTTP методи
    allow_headers=["*"],  # Разрешава всички HTTP хедъри
)

# Регистриране на рутерите
app.include_router(garages.router)

@app.get("/")
def read_root():
    return {"message": "Backend is running and connected to frontend!"}