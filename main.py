# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.main import app as backend_app

app = FastAPI()

# Mount the Flutter web build
app.mount("/", StaticFiles(directory="noabuddy_heroku_server/build/web", html=True), name="static")

# Catch-all route (for SPA routing like /chat, /about, etc.)
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    return FileResponse("noabuddy_heroku_server/build/web/index.html")

# Mount the API under /api
app.mount("/api", backend_app)
