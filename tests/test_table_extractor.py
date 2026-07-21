from backend.document_processing.table_extractor import extract_tables_from_pdf

def test_extract_tables():
    tables = extract_tables_from_pdf("sample_data/sample.pdf")

    assert tables is not None
    assert isinstance(tables, list)