
import os
import argparse
from typing import List
from warnings import warn

from collections import namedtuple

BibTexItem = namedtuple(
    'BibTexItem', 
    ['citekey', 'literature_type', 'data']
)

def main(
        input_file_path:    str, 
        output_file_path:   str, 
        prefix:             str = '', 
        suffix:             str = '\n'
        ):
    """Creates a BibTex file that include  in 'note' field. This will be useful 
    when citekey may be created by external programs but you want to key citekeys 
    (transferring BibTex data to another library). 

    Parameters
    ----------
    input_file_path: str

    """
    # Check if 
    if output_file_path == '':
        raise ValueError('Please give output_file_path.')
    
    if os.path.isfile(output_file_path):
        raise FileExistsError(f'File exists (although inplace=False): {output_file_path}')

    # Read the input file content
    bibtex_items: list = read_BibTex_file(input_file_path)
    
    # Insert citekey
    new_bibtex_items = insert_citekey_to_note(bibtex_items, prefix, suffix)

    # Output as file
    save_as_BibTex_file(new_bibtex_items, output_file_path)

# ================ Primary functions ================ #

def read_BibTex_file(file_path: str) -> List[BibTexItem]:
    contents = get_BibTex_file_contents(file_path)
    items: List[BibTexItem] = []

    for item in contents:
        bibtex_item = convert_str_to_BibTexItem(item)
        items.append(bibtex_item)

    return items

def insert_citekey_to_note(bibtex_items, prefix='', suffix='\n'):
    new_bibtex_items = []

    for item in bibtex_items:
        out_item = insert_citekey(item, prefix, suffix)
        new_bibtex_items.append(out_item)

    return new_bibtex_items

def save_as_BibTex_file(bibtex_items: List[BibTexItem], output_file_path: str):

    out_lines = []

    for item in bibtex_items:
        out_lines.append(format_BibTexItem_to_str(item))

    with open(output_file_path, 'w') as f:
        print(f'% itemnum: {len(out_lines)}', file=f)
        print('\n'.join(out_lines), file=f)

# ================ Secondary functions ================ #

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

def insert_citekey(item, prefix='', suffix='\n'):
    insert_field = 'note'

    if insert_field not in item.data:
        item.data[insert_field] = '"' + prefix + item.citekey + suffix + '"'

        return item

    existing_note = item.data[insert_field].strip('"')
    new_note = '"' + existing_note + f'\n{prefix}{item.citekey}{suffix}' + '"'
    
    item.data[insert_field] = new_note

    return item

def format_BibTexItem_to_str(item):
    """

    Format
    ------

    @literature_type{citekey
    data
    }
    """

    data_str = '\n'.join([
        field + ' = ' + value + ','
        for field, value in item.data.items()
    ])

    return f'@{item.literature_type}' + '{' + item.citekey \
        + f',\n{data_str}' + '\n}'

if __name__ == '__main__':
    desc = 'Insert citekey into "note" field.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-i", "--input_file_path", 
        help="A path to an input BibTex file.", 
        type=str
    )
    parser.add_argument(
        "-o", "--output_file_path", 
        help="A path to an output file.", 
        type=str, nargs='?', default=''
    )
    parser.add_argument(
        "-l", "--inplace", 
        help="Whether or not output content will be overwritten in the input file.", 
        type=bool, nargs='?', default=False
    )
    parser.add_argument(
        "-p", "--prefix", 
        help="Prefix string in the inserted string in the note field.", 
        type=str, nargs='?', default=''
    )
    parser.add_argument(
        "-s", "--suffix", 
        help="Suffix string in the inserted string in the note field.",
        type=str, nargs='?', default='\n'
    )
    args = parser.parse_args()
    main(
        args.input_file_path, 
        args.output_file_path,
        args.inplace, 
        args.prefix,
        args.suffix
    )

