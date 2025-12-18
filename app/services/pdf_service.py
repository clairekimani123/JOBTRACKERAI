from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path: str) -> str | None:
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip() if text.strip() else None

    except Exception as e:
        print("❌ PDF extraction error:", e)
        return None
