
from typing import Dict, List

from collections import namedtuple

BibTexItem = namedtuple(
    'BibTexItem', 
    ['citekey', 'literature_type', 'data']
)

def get_BibTex_file_contents(file_path: str):
    contents: List[str] = []
    tmp_lines = []

    with open(file_path, 'r') as f:
        for l in f:
            # Remove empty characters at the left and right ends.
            line = l.strip()

            # Skip comment line
            if line.startswith('%'):
                continue

            # Skip empty line
            if line == '':
                continue

            if line.startswith('@'):
                if len(tmp_lines) > 0:
                    contents.append(''.join(tmp_lines))
                
                tmp_lines = []
                tmp_lines.append(line)
            else:
                tmp_lines.append(line)
    
    contents.append(''.join(tmp_lines))
    return contents

def convert_str_to_BibTexItem(item: str):
    assert item.startswith('@')
    literature_type = item[1:].split('{')[0]
    
    data = item[1:].split(literature_type)[1]
    assert data.startswith('{')
    assert data.endswith('}')

    citekey = data[1:-1].split(',')[0]

    meta_data = data[1:-1].lstrip(citekey).lstrip(',').split('=')

    data = {}
    for i, chunk_info in enumerate(meta_data): 
        if i == 0: 
            field = chunk_info.strip()
        elif i == len(meta_data)-1: 
            data[field] = chunk_info.rstrip()
        else: 
            parts = chunk_info.strip().split(',') 
            prev_field_value = ','.join(parts[:-1]) 
            data[field] = prev_field_value 
            field = parts[-1]

    return BibTexItem(citekey, literature_type, data)
