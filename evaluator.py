import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime


# File locations
EXPECTED_FILE = Path("sample_docs/expected_results.csv")
ACTUAL_FILE = Path("outputs/results.csv")


# Fields to evaluate
FIELDS_TO_EVALUATE = [
    "document_type",
    "category",
    "vendor",
    "date",
    "amount"
]


def normalize(value, field):
    """
    Normalize values before comparison.

    Handles:
    - Different date formats
    - Amounts with different decimal formatting
    - Extra spaces and capitalization
    """

    value = str(value or "").strip()

    if not value:
        return ""

    # Normalize amount
    if field == "amount":
        try:
            return f"{Decimal(value):.2f}"
        except InvalidOperation:
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

    # Normalize other text fields
    return value.casefold()


def load_csv(file_path):
    """Read CSV file and return rows as dictionaries."""

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


def evaluate():

    # Check expected file
    if not EXPECTED_FILE.exists():
        print(f"Expected file not found: {EXPECTED_FILE}")
        return

    # Check actual file
    if not ACTUAL_FILE.exists():
        print(f"Actual file not found: {ACTUAL_FILE}")
        print("\nExport your Streamlit results to outputs/results.csv")
        return

    # Load both CSV files
    expected_rows = load_csv(EXPECTED_FILE)
    actual_rows = load_csv(ACTUAL_FILE)

    # Match documents using filenames
    expected_data = {
        row["file"].strip(): row
        for row in expected_rows
    }

    actual_data = {
        row["file"].strip(): row
        for row in actual_rows
    }

    print("\n========== RECEIPT EVALUATION ==========\n")

    print(f"Expected documents: {len(expected_data)}")
    print(f"Actual documents:   {len(actual_data)}")

    # Calculate accuracy
    print("\n========== ACCURACY REPORT ==========\n")

    for field in FIELDS_TO_EVALUATE:

        correct = 0
        total = len(expected_data)

        for filename, expected in expected_data.items():

            actual = actual_data.get(filename)

            if actual is None:
                continue

            expected_value = normalize(
                expected.get(field, ""),
                field
            )

            actual_value = normalize(
                actual.get(field, ""),
                field
            )

            if expected_value == actual_value:
                correct += 1

        accuracy = (
            correct / total * 100
            if total > 0
            else 0
        )

        print(
            f"{field.replace('_', ' ').title():20}"
            f" {correct}/{total} correct"
            f" | Accuracy: {accuracy:.2f}%"
        )

    # Display mismatches
    print("\n========== MISMATCH DETAILS ==========\n")

    mismatch_count = 0

    for filename, expected in expected_data.items():

        actual = actual_data.get(filename)

        if actual is None:

            print(f"Missing document: {filename}")

            mismatch_count += 1
            continue

        for field in FIELDS_TO_EVALUATE:

            expected_value = normalize(
                expected.get(field, ""),
                field
            )

            actual_value = normalize(
                actual.get(field, ""),
                field
            )

            if expected_value != actual_value:

                print(f"File: {filename}")
                print(f"Field: {field}")
                print(f"Expected: {expected_value}")
                print(f"Actual:   {actual_value}")
                print("-" * 40)

                mismatch_count += 1

    # Display unexpected documents
    extra_files = set(actual_data) - set(expected_data)

    if extra_files:

        print("\nUnexpected documents:")

        for filename in sorted(extra_files):
            print(filename)

    # Final summary
    print("\n========== FINAL SUMMARY ==========\n")

    print(f"Total expected documents: {len(expected_data)}")
    print(f"Total actual documents:   {len(actual_data)}")
    print(f"Total mismatches:         {mismatch_count}")

    if mismatch_count == 0:
        print("\nAll evaluated fields match the expected results!")

    else:
        print("\nSome mismatches were found. Please review them.")

    print("\n========== EVALUATION COMPLETE ==========")


if __name__ == "__main__":
    evaluate()