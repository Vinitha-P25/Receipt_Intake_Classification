import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime

from processor import process_pdf


# ==========================================
# PROJECT PATHS
# ==========================================

SAMPLE_DIR = Path("sample_docs")
EXPECTED_FILE = SAMPLE_DIR / "expected_results.csv"


# ==========================================
# FIELDS TO EVALUATE
# ==========================================

# Format: (display name, expected CSV column, actual result column)

FIELDS_TO_EVALUATE = [
    ("Source", "source", "source"),
    ("Document Type", "document_type", "document_type"),
    ("Category", "category", "category"),
    ("Vendor", "vendor", "vendor"),
    ("Date", "date", "date"),
    ("Amount", "amount", "amount"),
    ("Currency", "currency", "currency"),
    ("Reference Number", "document_number", "reference_number"),
    ("Status", "status", "status")
]


# ==========================================
# NORMALIZE VALUES
# ==========================================

def normalize(value, field):

    value = str(value or "").strip()

    if not value:
        return ""

    # Normalize amount
    if field == "amount":

        try:
            return f"{Decimal(value):.2f}"

        except (InvalidOperation, ValueError):
            return value

    # Normalize date
    if field == "date":

        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d"
        ]

        for date_format in date_formats:

            try:

                parsed_date = datetime.strptime(
                    value,
                    date_format
                )

                return parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                continue

        return value

    return value.casefold()


# ==========================================
# LOAD EXPECTED RESULTS
# ==========================================

def load_expected_results():

    with open(
        EXPECTED_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


# ==========================================
# PROCESS SAMPLE PDF DOCUMENTS
# ==========================================

def process_sample_documents(expected_rows):

    actual_results = []

    print("\n========== PROCESSING SAMPLE DOCUMENTS ==========\n")

    for index, expected in enumerate(expected_rows, start=1):

        filename = expected["file"].strip()

        pdf_path = SAMPLE_DIR / filename

        print(
            f"[{index}/{len(expected_rows)}] "
            f"Processing {filename}..."
        )

        if not pdf_path.exists():

            print("File not found.")

            result = {
                "file": filename,
                "source": "",
                "document_type": "",
                "category": "",
                "vendor": "",
                "date": "",
                "amount": "",
                "currency": "",
                "reference_number": "",
                "status": "Failed",
                "error": "PDF file not found"
            }

        else:

            try:

                pdf_bytes = pdf_path.read_bytes()

                # Run the actual processing pipeline
                result = process_pdf(pdf_bytes)

                result["file"] = filename

            except Exception as error:

                print(f"Processing error: {error}")

                result = {
                    "file": filename,
                    "source": "",
                    "document_type": "",
                    "category": "",
                    "vendor": "",
                    "date": "",
                    "amount": "",
                    "currency": "",
                    "reference_number": "",
                    "status": "Failed",
                    "error": str(error)
                }

        actual_results.append(result)

        print(
            f"Status: {result.get('status', 'Unknown')}"
        )

    return actual_results


# ==========================================
# EVALUATE RESULTS
# ==========================================

def evaluate(expected_rows, actual_results):

    expected_data = {
        row["file"].strip(): row
        for row in expected_rows
    }

    actual_data = {
        row["file"].strip(): row
        for row in actual_results
    }

    print("\n========== RECEIPT EVALUATION ==========\n")

    print(f"Expected documents: {len(expected_data)}")
    print(f"Processed documents: {len(actual_data)}")

    total_mismatches = 0

    # ======================================
    # FIELD-LEVEL ACCURACY
    # ======================================

    print("\n========== FIELD ACCURACY REPORT ==========\n")

    for display_name, expected_field, actual_field in FIELDS_TO_EVALUATE:

        correct = 0
        total = len(expected_data)

        for filename, expected in expected_data.items():

            actual = actual_data.get(filename)

            if actual is None:
                continue

            expected_value = normalize(
                expected.get(expected_field, ""),
                expected_field
            )

            actual_value = normalize(
                actual.get(actual_field, ""),
                actual_field
            )

            if expected_value == actual_value:
                correct += 1

        accuracy = (
            correct / total * 100
            if total else 0
        )

        print(
            f"{display_name:20}"
            f" {correct}/{total} correct"
            f" | Accuracy: {accuracy:.2f}%"
        )

    # ======================================
    # MISMATCH DETAILS
    # ======================================

    print("\n========== MISMATCH DETAILS ==========\n")

    for filename, expected in expected_data.items():

        actual = actual_data.get(filename)

        if actual is None:

            print(f"Missing result: {filename}")

            total_mismatches += 1

            continue

        for display_name, expected_field, actual_field in FIELDS_TO_EVALUATE:

            expected_value = normalize(
                expected.get(expected_field, ""),
                expected_field
            )

            actual_value = normalize(
                actual.get(actual_field, ""),
                actual_field
            )

            if expected_value != actual_value:

                print(f"File: {filename}")
                print(f"Field: {display_name}")
                print(f"Expected: {expected_value}")
                print(f"Actual: {actual_value}")
                print("-" * 45)

                total_mismatches += 1

    # ======================================
    # STATUS COMPARISON
    # ======================================

    print("\n========== STATUS SUMMARY ==========\n")

    expected_status_counts = {}
    actual_status_counts = {}

    for row in expected_rows:

        status = row.get("status", "Unknown")

        expected_status_counts[status] = (
            expected_status_counts.get(status, 0) + 1
        )

    for result in actual_results:

        status = result.get("status", "Unknown")

        actual_status_counts[status] = (
            actual_status_counts.get(status, 0) + 1
        )

    print("Expected Status Counts:")

    for status, count in sorted(expected_status_counts.items()):

        print(f"{status}: {count}")

    print("\nActual Status Counts:")

    for status, count in sorted(actual_status_counts.items()):

        print(f"{status}: {count}")

    # ======================================
    # FINAL SUMMARY
    # ======================================

    print("\n========== FINAL SUMMARY ==========\n")

    print(f"Expected documents: {len(expected_data)}")
    print(f"Processed documents: {len(actual_data)}")
    print(f"Total mismatches: {total_mismatches}")

    if len(expected_data) != len(actual_data):

        print("Warning: Expected and processed document counts differ.")

    if total_mismatches == 0:

        print("\nAll evaluated fields match expected results!")

    else:

        print("\nSome mismatches were found.")

    print("\n========== EVALUATION COMPLETE ==========")


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    if not EXPECTED_FILE.exists():

        print(
            f"Expected results file not found: {EXPECTED_FILE}"
        )

        return

    expected_rows = load_expected_results()

    if not expected_rows:

        print("Expected results CSV is empty.")

        return

    # Process PDFs automatically
    actual_results = process_sample_documents(expected_rows)

    # Compare expected and actual results
    evaluate(expected_rows, actual_results)


if __name__ == "__main__":

    main()