import os


top_path = os.path.abspath(os.path.join('..', 'interm_frags'))
for domain in os.listdir(top_path):
    domain_path = os.path.join(top_path, domain)
    for identifier in os.listdir(domain_path):
        identifier_path = os.path.join(domain_path, identifier)
        
        corpus_path = os.path.abspath(os.path.join('..', 'corpus', domain, identifier))
        os.makedirs(corpus_path)
        for doctype in os.listdir(identifier_path):
            frags_path = os.path.join(identifier_path, doctype)
            print(frags_path)
            
            with open(os.path.join(corpus_path, doctype+'.txt'), 'w', encoding='utf-8') as f_to:
                for fname in os.listdir(frags_path):
                    if fname.endswith('.txt'):
                        with open(os.path.join(frags_path, fname), 'r', encoding='utf-8') as f_from:
                            print(f_from.read().strip(), file=f_to)
                            print('', file=f_to)
