from backend.main import app

# Optional: mount frontend (build/) to serve HTML
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="build", html=True), name="static")
