from backend.document_processing.table_extractor import extract_tables_from_pdf

tables = extract_tables_from_pdf("sample_data/sample.pdf")

print(tables)