from backend.document_processing.metadata_extractor import (
    extract_metadata_from_pdf,
)

metadata = extract_metadata_from_pdf("sample_data/sample.pdf")

print(metadata)