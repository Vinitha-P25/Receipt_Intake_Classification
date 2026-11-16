import re
from datetime import datetime


def extract_label_value(text, label):
    """Extract a value whether it appears on the same or next line."""

    pattern = (
        rf"(?im)^[ \t]*{re.escape(label)}[ \t]*:?[ \t]*"
        rf"(?:([^\r\n]+)|\r?\n[ \t]*([^\r\n]+))"
    )

    match = re.search(pattern, text)

    if match:
        return (match.group(1) or match.group(2)).strip()

    return ""


def extract_vendor(text):
    return extract_label_value(text, "Vendor")


def extract_date(text):
    date_patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)

        if match:
            date_value = match.group()

            formats = [
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d-%m-%Y"
            ]

            for date_format in formats:
                try:
                    parsed_date = datetime.strptime(
                        date_value, date_format
                    )
                    return parsed_date.strftime("%Y-%m-%d")

                except ValueError:
                    continue

    return ""


def extract_amount_and_currency(text):
    patterns = [
        r"\bTOTAL\s+(SGD|USD|EUR|INR)\s*([\d,]+\.\d{2})",
        r"\b(SGD|USD|EUR|INR)\s*([\d,]+\.\d{2})",
        r"\b([\d,]+\.\d{2})\s*(SGD|USD|EUR|INR)\b"
    ]

    for index, pattern in enumerate(patterns):
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            if index == 2:
                amount = match.group(1)
                currency = match.group(2)
            else:
                currency = match.group(1)
                amount = match.group(2)

            amount = float(amount.replace(",", ""))

            return f"{amount:.2f}", currency.upper()

    return "", ""


def extract_reference_number(text):
    for label in [
        "Reference",
        "Invoice Number",
        "Receipt Number"
    ]:
        value = extract_label_value(text, label)

        if value:
            return value

    return ""


def extract_fields(text):
    amount, currency = extract_amount_and_currency(text)

    return {
        "vendor": extract_vendor(text),
        "date": extract_date(text),
        "amount": amount,
        "currency": currency,
        "reference_number": extract_reference_number(text)
    }
