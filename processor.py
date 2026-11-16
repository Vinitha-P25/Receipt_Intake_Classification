import pymupdf

from ocr_engine import extract_text_using_ocr
from classifier import classify_document
from extractor import extract_fields


def failed_result(message):
    return {
        "text": "",
        "source": "",
        "document_type": "",
        "category": "",
        "confidence": 0.0,
        "reason": message,
        "vendor": "",
        "date": "",
        "amount": "",
        "currency": "",
        "reference_number": "",
        "status": "Failed",
        "error": message
    }


def process_pdf(pdf_bytes):

    try:
        # 1. Open PDF

        pdf_document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        try:
            if pdf_document.needs_pass:
                raise ValueError("Password-protected PDF")

            if pdf_document.page_count == 0:
                raise ValueError("PDF contains no pages")

            # 2. Extract digital text

            digital_text = []

            for page in pdf_document:
                page_text = page.get_text("text")
                digital_text.append(page_text)

            combined_text = "\n".join(digital_text).strip()

            meaningful_chars = sum(
                character.isalnum()
                for character in combined_text
            )

            # 3. Choose Digital or OCR

            if meaningful_chars >= 10:
                extracted_text = combined_text
                source = "Digital"
            else:
                extracted_text = ""
                source = "OCR"

        finally:
            pdf_document.close()

        # 4. OCR processing

        if source == "OCR":
            extracted_text = extract_text_using_ocr(pdf_bytes)

        if not extracted_text.strip():
            raise ValueError("No readable text found in PDF")

        # 5. Classify document

        classification = classify_document(extracted_text)

        # 6. Handle unsupported documents

        if classification["document_type"] == "Not an expense document":

            return {
                "text": extracted_text,
                "source": source,
                "document_type": "Not an expense document",
                "category": "",
                "confidence": classification["confidence"],
                "reason": classification["reason"],
                "vendor": "",
                "date": "",
                "amount": "",
                "currency": "",
                "reference_number": "",
                "status": "Unsupported",
                "error": ""
            }

        # 7. Extract fields

        fields = extract_fields(extracted_text)

        # 8. Check required fields

        required_fields = [
            fields["vendor"],
            fields["date"],
            fields["amount"],
            fields["currency"],
            classification["category"]
        ]

        confidence = classification["confidence"]

        if all(required_fields) and confidence >= 0.70:

            status = "Done"
            error = ""

        else:

            status = "Needs review"
            error = "One or more required fields are missing or uncertain."

        # 9. Return complete result

        return {
            "text": extracted_text,
            "source": source,
            "document_type": classification["document_type"],
            "category": classification["category"],
            "confidence": confidence,
            "reason": classification["reason"],
            "vendor": fields["vendor"],
            "date": fields["date"],
            "amount": fields["amount"],
            "currency": fields["currency"],
            "reference_number": fields["reference_number"],
            "status": status,
            "error": error
        }

    except Exception as error:
        return failed_result(str(error))