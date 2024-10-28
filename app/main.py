# app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Allow your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve the React app
app.mount("/static", StaticFiles(directory="data_repre/build/static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()  # Read the content of the file
    return JSONResponse(content={"filename": file.filename, "content": content.decode('utf-8')})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
