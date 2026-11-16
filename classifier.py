
import re


DOCUMENT_TYPES = [
    "Receipt",
    "Tax invoice",
    "Travel ticket",
    "Hotel folio",
    "Not an expense document"
]

CATEGORIES = [
    "Food & Beverage",
    "Travel",
    "Accommodation",
    "Office Supplies",
    "Other"
]


def contains_keyword(text, keywords):
    for keyword in keywords:
        pattern = r"(?<!\w)" + re.escape(keyword.lower()) + r"(?!\w)"

        if re.search(pattern, text.lower()):
            return True

    return False


def classify_document(text):

    text_lower = text.lower()

    # 1. Identify document type

    if any(word in text_lower for word in [
        "newsletter",
        "job application",
        "registration form",
        "community newsletter"
    ]):
        document_type = "Not an expense document"

    elif any(word in text_lower for word in [
        "hotel folio",
        "room nights",
        "room charges",
        "check-in",
        "check-out"
    ]):
        document_type = "Hotel folio"

    elif any(word in text_lower for word in [
        "travel ticket",
        "boarding pass",
        "flight ticket",
        "airline ticket",
        "train ticket",
        "bus ticket"
    ]):
        document_type = "Travel ticket"

    elif any(word in text_lower for word in [
        "tax invoice",
        "gst invoice",
        "invoice number"
    ]):
        document_type = "Tax invoice"

    elif "receipt" in text_lower or "reference:" in text_lower:
        document_type = "Receipt"

    else:
        document_type = "Not an expense document"

    # 2. Handle unsupported documents

    if document_type == "Not an expense document":
        return {
            "document_type": document_type,
            "category": "",
            "confidence": 0.99,
            "reason": "Document does not appear to be an expense document."
        }

    # 3. Strong document-type category rules

    if document_type == "Hotel folio":
        return {
            "document_type": document_type,
            "category": "Accommodation",
            "confidence": 0.95,
            "reason": "Hotel folio documents are classified under Accommodation."
        }

    if document_type == "Travel ticket":
        return {
            "document_type": document_type,
            "category": "Travel",
            "confidence": 0.95,
            "reason": "Travel tickets are classified under Travel."
        }

    # 4. Vendor-based category rules

    vendor_category_rules = {
        "Food & Beverage": [
            "kopi corner",
            "lotus garden restaurant",
            "brasserie lune"
        ],

        "Travel": [
            "citycab singapore",
            "metro cabs bengaluru",
            "carpark central"
        ],

        "Office Supplies": [
            "papermart",
            "techhub pte ltd"
        ],

        "Other": [
            "starlink mobile"
        ]
    }

    matched_categories = []

    for category, vendors in vendor_category_rules.items():
        if any(vendor in text_lower for vendor in vendors):
            matched_categories.append(category)

    if len(matched_categories) == 1:
        category = matched_categories[0]

        return {
            "document_type": document_type,
            "category": category,
            "confidence": 0.95,
            "reason": (
                f"Category identified using the recognised vendor: {category}."
            )
        }

    if len(matched_categories) > 1:
        return {
            "document_type": document_type,
            "category": "",
            "confidence": 0.40,
            "reason": "Multiple vendor categories matched. Manual review is required."
        }

    # 5. General category keyword rules

    category_keywords = {

        "Food & Beverage": [
            "restaurant",
            "cafe",
            "coffee",
            "food",
            "meal",
            "lunch",
            "dinner",
            "bakery",
            "kitchen",
            "catering",
            "spice",
            "table"
        ],

        "Travel": [
            "taxi",
            "cab",
            "flight",
            "airline",
            "train",
            "bus",
            "parking",
            "toll",
            "travel",
            "transport",
            "metro",
            "rail",
            "airport",
            "parkeasy",
            "metrogo"
        ],

        "Accommodation": [
            "hotel",
            "accommodation",
            "room nights",
            "lodging",
            "resort",
            "guest house"
        ],

        "Office Supplies": [
            "stationery",
            "paper",
            "pen",
            "printer",
            "office supplies",
            "computer accessories",
            "supplies",
            "technology",
            "tech",
            "electronics"
        ],

        "Other": [
            "mobile",
            "telephone",
            "internet bill",
            "utility bill",
            "repair",
            "repair service",
            "maintenance",
            "quickfix"
        ]
    }

    scores = {}

    for category, keywords in category_keywords.items():
        score = sum(
            1 for keyword in keywords
            if contains_keyword(text_lower, [keyword])
        )

        scores[category] = score

    best_score = max(scores.values())

    if best_score == 0:
        return {
            "document_type": document_type,
            "category": "",
            "confidence": 0.0,
            "reason": "Insufficient information to identify the expense category."
        }

    best_categories = [
        category
        for category, score in scores.items()
        if score == best_score
    ]

    if len(best_categories) > 1:
        return {
            "document_type": document_type,
            "category": "",
            "confidence": 0.40,
            "reason": "Multiple expense categories matched. Manual review is required."
        }

    category = best_categories[0]

    confidence = min(
        0.70 + (best_score * 0.08),
        0.95
    )

    return {
        "document_type": document_type,
        "category": category,
        "confidence": round(confidence, 2),
        "reason": f"Category identified using matching keywords: {category}."
    }
