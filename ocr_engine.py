import io
import pytesseract
import pymupdf

from PIL import Image


# Tesseract executable location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_using_ocr(pdf_bytes):

    """
    Extract text from a scanned PDF using Tesseract OCR.

    Args:
        pdf_bytes: PDF file content in bytes.

    Returns:
        Extracted text from all pages.
    """

    extracted_text = []

    # Open PDF from memory
    pdf_document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    try:
        for page_number, page in enumerate(pdf_document):

            print(f"Running OCR on page {page_number + 1}")

            # Convert PDF page into an image
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False
            )

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            # Extract text using Tesseract
            page_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            extracted_text.append(page_text)

    finally:
        pdf_document.close()

    return "\n".join(extracted_text)