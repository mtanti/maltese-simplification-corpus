import os
import re


top_path = os.path.abspath(os.path.join('..', 'proc_docs'))
for domain in os.listdir(top_path):
    domain_path = os.path.join(top_path, domain)
    for identifier in os.listdir(domain_path):
        identifier_path = os.path.join(domain_path, identifier)
        for doctype in os.listdir(identifier_path):
            proc_doc_path = os.path.join(identifier_path, doctype)
            print(proc_doc_path)
            
            for fname in os.listdir(proc_doc_path):
                if fname.endswith('.xml'):
                    fpath = os.path.join(proc_doc_path, fname)
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    m = re.match(r'^(<annotation>\n\t<folder>[^<]*</folder>\n\t<filename>[^<]*</filename>\n\t<path>)[^<]*(</path>(.|\n)*)$', content)
                    new_content = '{}.{}'.format(m.group(1), m.group(2))
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)