from backend.document_processing.pdf_parser import extract_text_from_pdf

pages = extract_text_from_pdf("sample_data/sample.pdf")

for page in pages:
    print(f"\n--- Page {page['page_number']} ---")
    print(page["text"])