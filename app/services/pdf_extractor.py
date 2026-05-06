import pdfplumber

def extract_text_from_pdf(file_path: str) -> str | None:
    """
    Extract text from PDF using pdfplumber.
    Works for all standard digital PDFs (resumes, job descriptions, etc.)
    """
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
        else:
            print("⚠️ PDF appears to be empty or image-based")
            return None
    except Exception as e:
        print("❌ PDF extraction failed:", e)
        return None