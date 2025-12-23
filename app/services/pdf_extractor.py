import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def extract_text_from_pdf(file_path: str) -> str | None:
    """
    1. Try normal text extraction (fast)
    2. If empty → fallback to OCR (slow but reliable)
    """

    # ---------- 1️⃣ Try pdfplumber ----------
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            print("✅ Text extracted using pdfplumber")
            return text.strip()

    except Exception as e:
        print("❌ pdfplumber failed:", e)

    # ---------- 2️⃣ OCR Fallback ----------
    try:
        print("🔍 Falling back to OCR...")

        images = convert_from_path(file_path)
        ocr_text = ""

        for img in images:
            ocr_text += pytesseract.image_to_string(img) + "\n"

        return ocr_text.strip() if ocr_text.strip() else None

    except Exception as e:
        print("❌ OCR extraction failed:", e)
        return None
