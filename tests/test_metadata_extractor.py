from backend.document_processing.metadata_extractor import (
    extract_metadata_from_pdf,
)

def test_extract_metadata():
    metadata = extract_metadata_from_pdf("sample_data/sample.pdf")

    assert metadata is not None
    assert isinstance(metadata, dict)