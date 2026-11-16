# Receipt Intake & Classification

## Overview

A Streamlit-based application that accepts multiple PDF expense documents, detects digital text or scanned images, extracts text using PyMuPDF or Tesseract OCR, classifies documents, and extracts key expense information.

The application displays results in a reviewable table with filtering, sorting, category totals grouped by currency, detailed extracted text, and CSV export.

## Features

- Multiple PDF uploads.
- Digital text detection and extraction.
- Automatic OCR fallback for scanned PDFs.
- Document classification:
  - Receipt
  - Tax invoice
  - Travel ticket
  - Hotel folio
  - Not an expense document
- Expense categorization:
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
- Detailed extracted-text review.
- CSV export.

## Technology Stack

- Python
- Streamlit
- Pandas
- PyMuPDF
- Tesseract OCR
- pytesseract
- Pillow

## Processing Workflow

1. The user uploads one or multiple PDF documents.
2. Each PDF is processed independently.
3. PyMuPDF checks whether the PDF contains selectable digital text.
4. If meaningful digital text is unavailable, Tesseract OCR extracts text from scanned pages.
5. The extracted text is passed to the classification module.
6. The application identifies the document type and expense category.
7. The extraction module retrieves vendor, date, amount, currency, and reference number.
8. Required fields and classification confidence determine the processing status.
9. Results are displayed in the Streamlit interface for review and CSV export.

Multipage PDFs are treated as a single document, and the document-stated total is used for amount extraction.

PDF contents are treated strictly as document data and never as instructions to the application.

## Processing Status

| Status | Description |
|---|---|
| Done | Required fields are available with sufficient classification confidence. |
| Needs review | One or more required fields are missing or uncertain. |
| Unsupported | The document is not an expense document. |
| Failed | The PDF is corrupt, password-protected, empty, or unreadable. |

Missing or uncertain values are left blank rather than guessed.

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/Vinitha-P25/Receipt_Intake_Classification.git
cd Receipt_Intake_Classification
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 5. Install Tesseract OCR

Install the Tesseract OCR application separately on Windows and ensure its installation directory is added to the system PATH.

Verify the installation:

```powershell
tesseract --version
```

### 6. Run the application

```powershell
streamlit run app.py
```

The application will open in your browser.

## Evaluation

Run the evaluation against the 12 supplied assessment PDFs:

```powershell
python evaluate.py
```

The evaluation report is saved in:

`outputs/evaluation_report.txt`

See [docs/TESTING.md](docs/TESTING.md) for the detailed assessment testing and robustness verification report.

### Assessment Sample Results

| Evaluation Field | Accuracy |
|---|---:|
| Source Detection | 100% |
| Document Type | 100% |
| Expense Category | 100% |
| Vendor | 100% |
| Date | 100% |
| Amount | 100% |
| Currency | 100% |
| Reference Number | 100% |
| Processing Status | 100% |

- Documents processed: 12
- Total mismatches: 0

These results apply only to the 12 supplied assessment documents and do not guarantee the same accuracy on unseen documents.

## AI Tools Used

ChatGPT was used as a development assistant for coding guidance, debugging, and understanding the application workflow.

The application uses rule-based classification and extraction. No external LLM API is used during document processing.

## Known Weaknesses

1. Rule-based classification may not reliably recognize every unseen document layout or unfamiliar vendor.
2. OCR accuracy can decrease with low-resolution, blurred, rotated, or handwritten documents.
3. Field extraction depends on recognizable labels and formats. Unusual date, amount, or reference-number layouts may require manual review.
4. The confidence score is based on classification rules and is not a calibrated probability of extraction accuracy.

## Project Structure

```text
Receipt_Intake_Classification/
│
├── app.py
├── processor.py
├── ocr_engine.py
├── classifier.py
├── extractor.py
├── evaluate.py
├── evaluator.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
│   └── TESTING.md
│
├── sample_docs/
│   ├── R01.pdf
│   ├── R02.pdf
│   ├── ...
│   ├── R12.pdf
│   └── expected_results.csv
│
└── outputs/
    └── evaluation_report.txt
