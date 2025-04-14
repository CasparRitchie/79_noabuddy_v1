from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Serve frontend build
app.mount("/", StaticFiles(directory="build", html=True), name="frontend")

@app.get("/")
async def serve_index():
    return FileResponse("build/index.html")
