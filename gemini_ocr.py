import google.generativeai as genai
from PIL import Image
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found. Check your .env file.")


# Connect to Gemini
genai.configure(api_key=API_KEY)

def read_invoice(image_path):
    """
    Send image to Gemini and extract vendor, total, date
    """
    model = genai.GenerativeModel('gemini-1.5-flash')


    # Open image or PDF with error handling and convert to RGB for compatibility
    try:
        if image_path.lower().endswith('.pdf'):
            # Convert first page of PDF to image
            images = convert_from_path(image_path, first_page=1, last_page=1)
            img = images[0]
        else:
            img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        raise Exception(f"Error opening or converting file: {e}. Make sure the file is a supported image or PDF format.")

    # Ask Gemini
    prompt = """
    Look at this invoice and extract:
    - Vendor or Supplier Name
    - Total Amount (with $ or other currency)
    - Invoice Date

    Return only in this format:
    Vendor: ABC Supplies
    Total: $450.00
    Date: 2024-05-10
    """

    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# Add main block to run as script
if __name__ == "__main__":
    image_path = input("Enter the path to the invoice image: ")
    result = read_invoice(image_path)
    print("\nResult:\n", result)