import os
import json
import numpy as np
from PIL import Image
from pascal import PascalVOC
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

top_path = os.path.abspath(os.path.join('..', 'interm_pages'))
for domain in os.listdir(top_path):
    domain_path = os.path.join(top_path, domain)
    for identifier in os.listdir(domain_path):
        identifier_path = os.path.join(domain_path, identifier)
        for doctype in os.listdir(identifier_path):
            pages_path = os.path.join(identifier_path, doctype)
            print(pages_path)
            
            frags_path = os.path.abspath(os.path.join('..', 'interm_frags', domain, identifier, doctype))
            os.makedirs(frags_path)
            
            page_fnames = [fname for fname in os.listdir(pages_path) if fname.endswith('.jpg')]
            anno_fnames = {fname for fname in os.listdir(pages_path) if fname.endswith('.xml')}
            for page_fname in page_fnames:
                page_num = int(page_fname[:-4])
                anno_fname = page_fname[:-4]+'.xml'
                if anno_fname in anno_fnames:
                    page = np.array(Image.open(os.path.join(pages_path, page_fname)))

                    ann = PascalVOC.from_xml(os.path.join(pages_path, anno_fname))
                    
                    frag_id = 0
                    for obj in ann.objects:
                        name = obj.name
                        x1 = obj.bndbox.xmin
                        y1 = obj.bndbox.ymin
                        x2 = obj.bndbox.xmax
                        y2 = obj.bndbox.ymax

                        if name == 'text':
                            frag_id += 1
                            frag_img = page[y1:y2, x1:x2, :]
                            with open(os.path.join(frags_path, f'{page_num:0>3d}_{frag_id:0>2d}.txt'), 'w', encoding='utf-8') as f:
                                print(pytesseract.image_to_string(frag_img, lang='mlt'), file=f)
                            Image.fromarray(frag_img).save(os.path.join(frags_path, f'{page_num:0>3d}_{frag_id:0>2d}.jpg'))
                        elif name == 'whiteout':
                            page[y1:y2, x1:x2, :] = 255
                        else:
                            raise AssertionError(name)
