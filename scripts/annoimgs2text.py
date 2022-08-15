import os
import json
import numpy as np
from PIL import Image
from pascal import PascalVOC
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

top_path = os.path.abspath(os.path.join('..', 'proc_docs'))
for domain in os.listdir(top_path):
    domain_path = os.path.join(top_path, domain)
    for identifier in os.listdir(domain_path):
        identifier_path = os.path.join(domain_path, identifier)
        corpus_path = os.path.abspath(os.path.join('..', 'corpus', domain, identifier))
        os.makedirs(corpus_path)
        for doctype in os.listdir(identifier_path):
            proc_doc_path = os.path.join(identifier_path, doctype)
            print(proc_doc_path)
            
            page_fnames = [fname for fname in os.listdir(proc_doc_path) if fname.endswith('.jpg')]
            anno_fnames = {fname for fname in os.listdir(proc_doc_path) if fname.endswith('.xml')}
            with open(os.path.join(corpus_path, doctype+'.txt'), 'w', encoding='utf-8') as f:
                for page_fname in page_fnames:
                    anno_fname = page_fname[:-4]+'.xml'
                    if anno_fname in anno_fnames:
                        page = np.array(Image.open(os.path.join(proc_doc_path, page_fname)))

                        ann = PascalVOC.from_xml(os.path.join(proc_doc_path, anno_fname))
                        
                        for obj in ann.objects:
                            name = obj.name
                            x1 = obj.bndbox.xmin
                            y1 = obj.bndbox.ymin
                            x2 = obj.bndbox.xmax
                            y2 = obj.bndbox.ymax

                            if name == 'text':
                                print(pytesseract.image_to_string(page[y1:y2, x1:x2, :], lang='mlt'), file=f)
                            elif name == 'whiteout':
                                page[y1:y2, x1:x2, :] = 255
                            else:
                                raise AssertionError(name)
