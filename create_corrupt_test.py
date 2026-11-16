from pathlib import Path

output_path = Path("sample_docs/CORRUPT_TEST.pdf")

output_path.write_bytes(
    b"This is not a valid PDF document."
)

print(f"Corrupt PDF created: {output_path}")