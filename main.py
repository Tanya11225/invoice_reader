from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from gemini_ocr import read_invoice
import os
import pandas as pd

app = FastAPI()

# Allow web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to save uploads
os.makedirs("uploads", exist_ok=True)

# Store results
data_log = []


from fastapi.responses import JSONResponse
from fastapi import status

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": f"Failed to save file: {str(e)}"})

    # Use Gemini to read it
    try:
        result = read_invoice(file_path)
    except Exception as e:
        # Special message for Poppler not found
        if "poppler" in str(e).lower() or "pdfinfo" in str(e).lower():
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "PDF processing failed. Please ensure Poppler is installed and added to your PATH."})
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

    # Save to log
    data_log.append({
        "Filename": file.filename,
        "Extracted Data": result
    })

    return {
        "message": "Processed successfully!",
        "filename": file.filename,
        "data": result
    }


@app.post("/export/")
async def save_to_excel():
    from fastapi.responses import JSONResponse
    from fastapi import status
    if not data_log:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "No data to export"})
    try:
        df = pd.DataFrame(data_log)
        df.to_excel("invoices.xlsx", index=False)
        return {"status": "Saved to invoices.xlsx"}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"Failed to export: {str(e)}"})