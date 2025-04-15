# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.main import app as backend_app

app = FastAPI()

# Mount the Flutter web build
app.mount("/", StaticFiles(directory="noabuddy_heroku_server", html=True), name="static")

# Mount the API under /api
app.mount("/api", backend_app)
