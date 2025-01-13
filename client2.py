from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    if not file:
        raise HTTPException(status_code=400, detail="No file part provided")
    
    if not file.filename.strip():
        raise HTTPException(status_code=400, detail="No selected file")
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"File uploaded successfully: {file.filename}")
        result = {
            "filename": file.filename,
            "status": "File uploaded successfully"
        }
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while uploading the file")
