from fastapi import FastAPI, UploadFile, File
app= FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to OmniBrain API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "type": file.content_type
    }
