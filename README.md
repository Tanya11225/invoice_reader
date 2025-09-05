# 🧾 AI Invoice Reader

An intelligent document processing system that extracts structured data from **invoices** (images and PDFs) using **Google Gemini AI** and **FastAPI**.

Upload an invoice → Extract key fields (vendor, total, date, etc.) → Export to JSON or Excel.

Perfect for automating accounting, bookkeeping, and financial data entry.

---

## ✨ Features

- ✅ Upload invoice images (PNG, JPG) or PDF files
- ✅ Extract structured data using **Google Gemini Vision AI**
- ✅ Automatic conversion of PDF to image using `PyMuPDF` (no Poppler required)
- ✅ Clean JSON output with fields:
  - Vendor Name
  - Invoice Number
  - Date Issued
  - Due Date
  - Total Amount
  - Currency
- ✅ View processing logs
- ✅ Export all extracted data to Excel
- ✅ REST API built with **FastAPI**
- ✅ Auto-generated API docs at `/docs`

---

## 📦 Tech Stack

| Tool | Purpose |
|------|--------|
| FastAPI | Backend API framework |
| Google Gemini 1.5 Flash | AI model for vision & text extraction |
| PyMuPDF (fitz) | PDF to image conversion |
| Pillow | Image handling |
| pandas | Export to Excel |
| Uvicorn | ASGI server |


## Project Structure

invoice-reader/
│
├── main.py                   # Main FastAPI app
├── gemini_ocr.py             # AI extraction logic
├── uploads/                  # Stores uploaded files
├── data_log = []             # In-memory list of results (in main.py)
├── invoices_extracted.xlsx   # Generated on export
├── requirements.txt          # (Optional) List of dependencies
└── README.md                 # This file

📎 Example Output

{
  "message": "Processed successfully!",
  "filename": "invoice.pdf",
  "data": {
    "vendor": "Tech Solutions Inc.",
    "invoice_number": "INV-2024-001",
    "date_issued": "2024-05-05",
    "due_date": "2024-05-19",
    "total_amount": "$1,931.30",
    "currency": "USD"
  }
}

