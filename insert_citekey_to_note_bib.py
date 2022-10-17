
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





    #             bib_items[citekey] = BibTexItem(citekey, literature_type, tmp_data)

    #             # Get identifier (citekey) and literature type
    #             parts = line[1:].split('{')
    #             literature_type = parts[0]
    #             citekey = parts[1].split(',')[0]

    #             # Initialize an object to collect data
    #             tmp_data = {}

    #         # Collect literature data
    #         else:
    #             parts = line.rstrip(',').split('=')
    #             field = parts[0].strip()
    #             try:
    #                 value = parts[1].strip().strip('"')
    #             except IndexError:
    #                 raise IndexError(line)

    #             assert field not in tmp_data
    #             tmp_data[field] = value
    
    # assert citekey not in bib_items
    # bib_items[citekey] = BibTexItem(citekey, literature_type, tmp_data)

    # return bib_items


