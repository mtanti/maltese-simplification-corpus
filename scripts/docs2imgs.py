import os
import json
import docx2pdf
import tempfile
import pdf2image


top_path = os.path.abspath(os.path.join('..', 'raw_docs'))
for domain in os.listdir(top_path):
    domain_path = os.path.join(top_path, domain)
    for identifier in os.listdir(domain_path):
        identifier_path = os.path.join(domain_path, identifier)
        with open(os.path.join(identifier_path, 'info.json'), 'r', encoding='utf-8') as f:
            info = json.loads(f.read())
        for doc in info['documents']:
            raw_doc_path = os.path.join(identifier_path, doc['fname'])
            proc_doc_path = os.path.abspath(os.path.join('..', 'proc_docs', domain, identifier, doc['type']))
            os.makedirs(proc_doc_path)
            print(raw_doc_path)
            
            with tempfile.TemporaryDirectory() as tmp:
                if raw_doc_path.endswith('.docx'):
                    pdf_path = os.path.join(tmp, 'tmp.pdf')
                    docx2pdf.convert(raw_doc_path, pdf_path)
                else:
                    pdf_path = raw_doc_path
                    
                with open(pdf_path, 'rb') as f:
                    pages = pdf2image.convert_from_bytes(f.read())
                for (page_num, page) in enumerate(pages, start=1):
                    page.save(os.path.join(proc_doc_path, '{:0>3d}.jpg'.format(page_num)), 'JPEG')
