import pymupdf
from pathlib import Path

output_path = Path("sample_docs/EMPTY_TEST.pdf")

document = pymupdf.open()
document.new_page()

document.save(output_path)
document.close()

print(f"Empty PDF created: {output_path}")