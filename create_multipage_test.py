import pymupdf
from pathlib import Path

output_folder = Path("sample_docs")
output_folder.mkdir(exist_ok=True)

pdf_path = output_folder / "MULTIPAGE_TEST.pdf"

document = pymupdf.open()

# Page 1
page1 = document.new_page()

page1.insert_text(
    (70, 80),
    "FOOD RECEIPT",
    fontsize=20
)

page1.insert_text(
    (70, 130),
    "Vendor: MultiPage Cafe\n"
    "Date: 2026-11-16\n"
    "Receipt Number: MPC-1001\n"
    "Subtotal SGD 100.00\n"
    "Tax SGD 9.00",
    fontsize=12
)

# Page 2
page2 = document.new_page()

page2.insert_text(
    (70, 80),
    "RECEIPT SUMMARY",
    fontsize=20
)

page2.insert_text(
    (70, 130),
    "Thank you for visiting!\n"
    "TOTAL SGD 109.00",
    fontsize=14
)

document.save(pdf_path)
document.close()

print(f"Test PDF created successfully: {pdf_path}")