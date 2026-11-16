import pymupdf
from pathlib import Path

output_path = Path("sample_docs/PASSWORD_TEST.pdf")

document = pymupdf.open()

page = document.new_page()
page.insert_text(
    (70, 100),
    "Password Protected Test Receipt\nVendor: Test Cafe\nTOTAL SGD 50.00"
)

document.save(
    output_path,
    encryption=pymupdf.PDF_ENCRYPT_AES_256,
    owner_pw="owner123",
    user_pw="test123"
)

document.close()

print(f"Password-protected PDF created: {output_path}")