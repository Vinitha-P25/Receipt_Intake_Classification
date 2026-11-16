# Receipt Intake & Classification

## Overview

A Streamlit application that accepts multiple PDF expense documents, detects whether each PDF contains digital text or scanned images, extracts text using PyMuPDF or Tesseract OCR, classifies the document, and extracts key expense information. Results are displayed in a reviewable table with filtering, sorting, category totals grouped by currency, detailed extracted text, and CSV export.

## Features

- Multiple PDF upload.
- Digital text extraction and scanned-document OCR.
- Document classification:
  - Receipt
  - Tax invoice
  - Travel ticket
  - Hotel folio
  - Not an expense document
- Expense categories:
  - Food & Beverage
  - Travel
  - Accommodation
  - Office Supplies
  - Other
- Extraction of vendor, date, amount, currency, and reference number.
- Confidence score and classification reason.
- Processing statuses: Done, Needs review, Unsupported, and Failed.
- Filtering and sorting of results.
- Expense totals grouped by category and currency.
- CSV export and extracted-text review.

## Technology Stack

- Python
- Streamlit
- Pandas
- PyMuPDF
- Tesseract OCR
- pytesseract
- Pillow

## Design

The application processes each uploaded PDF independently. PyMuPDF first checks for selectable digital text. If meaningful text is unavailable, the document is sent to Tesseract OCR. Multipage PDFs are treated as a single document, and the document-stated total is used for amount extraction. The extracted text is passed through rule-based classification and field-extraction logic. Required fields and classification confidence determine whether the document is marked Done or Needs review. Non-expense documents are marked Unsupported, while unreadable or invalid documents are marked Failed. PDF contents are treated strictly as document data and never as instructions to the application. The results are presented in Streamlit for review and CSV export.

## Installation and Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Install the Tesseract OCR application separately on Windows and ensure its installation directory is added to the system PATH.

Verify installation:

```powershell
tesseract --version
```

### 5. Run the application

```powershell
streamlit run app.py
```

## Evaluation

Run the evaluation against the 12 supplied assessment PDFs:

```powershell
python evaluate.py
```

The evaluation report is saved in:

`outputs/evaluation_report.txt`

### Assessment Sample Results

- Documents processed: 12
- Source accuracy: 100%
- Document type accuracy: 100%
- Category accuracy: 100%
- Vendor accuracy: 100%
- Date accuracy: 100%
- Amount accuracy: 100%
- Currency accuracy: 100%
- Reference number accuracy: 100%
- Status accuracy: 100%
- Total mismatches: 0

These results apply to the supplied 12 sample documents and do not guarantee the same accuracy on unseen documents.

## AI Tools Used

ChatGPT was used as a development assistant for coding guidance, debugging, and understanding the application workflow. The application uses rule-based classification and extraction; no external LLM API is used during document processing.

## Known Weaknesses

1. Rule-based classification may not reliably recognize every unseen document layout or unfamiliar vendor.
2. OCR accuracy can decrease with low-resolution, blurred, rotated, or handwritten documents.
3. Field extraction depends on recognizable labels and formats; unusual date, amount, or reference-number layouts may require manual review.
4. The confidence score is based on classification rules and is not a calibrated probability of extraction accuracy.

## Project Structure

- `app.py` – Streamlit user interface.
- `processor.py` – PDF processing workflow and status handling.
- `ocr_engine.py` – OCR processing.
- `classifier.py` – Document and expense category classification.
- `extractor.py` – Expense field extraction.
- `evaluate.py` – Assessment evaluation runner.
- `evaluator.py` – Evaluation and accuracy reporting.
- `requirements.txt` – Python dependencies.
- `sample_docs/` – Assessment sample PDFs and expected results.
- `outputs/evaluation_report.txt` – Saved evaluation report.