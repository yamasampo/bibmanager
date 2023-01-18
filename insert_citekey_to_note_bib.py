#!/usr/bin/python3

"""A Python script that retrieves identifiers of entries in a reference library, 
which are called citekey, and inserts it into a field tractable across libraries. 

Currently, this script accepts only a BibTex file format (ref. 1-3), but other 
formats, such as CSV and JASON formats, may be supported in the future. 

In the BibTex file format, each entry is defined by @ and a curly bracket. 
Here is an example, 

    @ARTICLE{Talbert2022-wc,
    title = "Viral histones: pickpocket's prize or primordial progenitor?",
    author = "Talbert, Paul B and Armache, Karim-Jean and Henikoff, Steven",
    abstract = "The common histones H2A, H2B, H3, and H4 are the characteristic components of eukaryotic nucleosomes, which function to wrap DNA and compact the genome as well as to regulate access to DNA for transcription and replication in all eukaryotes. In the past two decades, histones have also been found to be encoded in some DNA viruses, where their functions and properties are largely unknown, though recently histones from two related viruses have been shown to form nucleosome-like structures in vitro. Viral histones can be highly similar to eukaryotic histones in primary sequence, suggesting they have been recently picked up from eukaryotic hosts, or they can be radically divergent in primary sequence and may occur as conjoined histone doublets, triplets, or quadruplets, suggesting ancient origins prior to the divergence of modern eukaryotes. Here, we review what is known of viral histones and discuss their possible origins and functions. We consider how the viral life cycle may affect their properties and histories, and reflect on the possible roles of viruses in the origin of the nucleus of modern eukaryotic cells.",
    journal = "Epigenetics \& chromatin",
    volume =  15,
    number =  1,
    pages = "21",
    month =  may,
    year =  2022,
    url = "http://dx.doi.org/10.1186/s13072-022-00454-7",
    file = "All_Papers/T/Talbert-Henikoff-2022-epigenetics_chromatin.pdf",
    language = "en",
    issn = "1756-8935",
    pmid = "35624484",
    doi = "10.1186/s13072-022-00454-7"
    }

This format includes three types of information: entry type, entry ID 
(so called citekey), and other data about the entry. 

    Entry type can be found as a string between @ and the open parenthesis 
    (ARTICLE in this example). An entry type is not a case sensitive property. 
    Currently, BibTex has a total of 14 entry types, a PaperPile article says 
    (ref. 3). 

    Citekey can be found as a string between an open parenthesis and the first
    comma (Talbert2022-wc in this example). The citekey should be assigned 
    uniquely to entries in a BibTex file. This script checks this. 

    Other data follows after citekey and is formatted as a list of field and 
    value pairs. Field and value are separated by = sign, and there are standard 
    field types (ref. 3). 

There are many other specifics in BibTex format but please refer to others' 
explanations. I found the PaperPile's website very informative (ref. 4). 

This Python script parses a BibTex file (obtain entry type, citekey and other 
data), creates "note" field if it does not exist, and adds citekey to the "note" 
field. In the output file, the sample entry above is shown like this,

    @ARTICLE{Talbert2022-wc,
    title = "Viral histones: pickpocket's prize or primordial progenitor?",
    author = "Talbert, Paul B and Armache, Karim-Jean and Henikoff, Steven",
    abstract = "The common histones H2A, H2B, H3, and H4 are the characteristic components of eukaryotic nucleosomes, which function to wrap DNA and compact the genome as well as to regulate access to DNA for transcription and replication in all eukaryotes. In the past two decades, histones have also been found to be encoded in some DNA viruses, where their functions and properties are largely unknown, though recently histones from two related viruses have been shown to form nucleosome-like structures in vitro. Viral histones can be highly similar to eukaryotic histones in primary sequence, suggesting they have been recently picked up from eukaryotic hosts, or they can be radically divergent in primary sequence and may occur as conjoined histone doublets, triplets, or quadruplets, suggesting ancient origins prior to the divergence of modern eukaryotes. Here, we review what is known of viral histones and discuss their possible origins and functions. We consider how the viral life cycle may affect their properties and histories, and reflect on the possible roles of viruses in the origin of the nucleus of modern eukaryotic cells.",
    journal = "Epigenetics \& chromatin",
    volume = 15,
    number = 1,
    pages = "21",
    month = may,
    year = 2022,
    url = "http://dx.doi.org/10.1186/s13072-022-00454-7",
    file = "All_Papers/T/Talbert-Henikoff-2022-epigenetics_chromatin.pdf",
    language = "en",
    issn = "1756-8935",
    pmid = "35624484",
    doi =  "10.1186/s13072-022-00454-7",
    note = "221017_PaperPile_citekey: Talbert2022-wc",
    }


References
----------
[1] BibTex official HP: http://www.bibtex.org/Format/ 
[2] Wikipedia about BibTex: https://en.wikipedia.org/wiki/BibTeX
[3] BibTex format overview by PaperPile: https://www.bibtex.com/g/bibtex-format/ 
[4] BibTex format details by PaperPile https://www.bibtex.com/format/

"""

# Imports from Python built-in packages
import os
import argparse
import configparser

from typing import List, Set, Union

from collections import namedtuple

__version__ = '0.1.1'
__author__ = 'Haruka Yamashita'
__email__ = 'haruka.yamashita.t@gmail.com'

# Define an object that represents each reference entry in a BibTex file
BibTexEntry = namedtuple(
    'BibTexEntry', 
    ['citekey', 'entry_type', 'data']
)

def main(
        input_file_path:    str, 
        output_file_path:   str, 
        prefix:             str = '', 
        suffix:             str = ''
        ) -> None:
    """Creates a BibTex file that include citekey in 'note' field. This will be 
    useful when another citekey may be created for an existing entry by external 
    programs but you want to keep the old citekey. 
    
    This function is composed of three steps:
        1. Read an input file
        2. Insert citekey to note section
        3. Output the modified data as a text file
    and each of them was done by sub-functions:
        1. read_BibTex_file
        2. insert_citekey_to_note
        3. save_as_BibTex_file
    , respectively. 

    Parameters
    ----------
    input_file_path: str
        A path to the input BibTex file
    output_file_path: str
        A path to the output BibTex file
    prefix: str (optional: '' by default)
        A string that will be put just before citekey in note section. 
    suffix: str (optional: '' by default)
        A string that will be put just after citekey in note section.
    """
    # Check if an output file is given properly
    if output_file_path == '':
        raise ValueError('Please give output_file_path.')
    
    # Check if a file does not exist at output_file_path
    if os.path.isfile(output_file_path):
        raise FileExistsError(f'File exists: {output_file_path}')

    # Read the input file content
    bibtex_entries: List[BibTexEntry] = read_BibTex_file(input_file_path)
    
    # Insert citekey in note field. 
    # NOTE: Currently, the field to which citekey will be inserted is hard-coded 
    # under this function, but I can make it accessible by users. 
    new_bibtex_entries = insert_citekey_to_note(bibtex_entries, prefix, suffix)

    # Output as file
    save_as_BibTex_file(new_bibtex_entries, output_file_path)

# ================ Primary functions ================ #

def read_BibTex_file(file_path: str) -> List[BibTexEntry]:
    """Returns a list of reference entries. Each entry is contained in a 
    BibTexEntry namedtuple. 

    Parameter
    ---------
    file_path: str
        A path to the input BibTex file

    Return
    ------
    List[BibTexEntry]
    """
    # Get a list of strings, each of them represent one reference entry
    contents: List[str]         = get_BibTex_file_contents(file_path)
    # Initialize a list to output
    entries: List[BibTexEntry]    = []

    # For each entry
    for entry_str in contents:
        # Read a string into BibTexEntry
        bibtex_entry = convert_str_to_BibTexEntry(entry_str)
        entries.append(bibtex_entry)

    # Get a set of citekeys to check if they are unique to each entries
    citekey_set: Set[str] = {entry.citekey for entry in entries}
    assert len(entries) == len(citekey_set), \
        'The number of entries and citekey does not match: '\
        f'{len(entries)} != {len(citekey_set)}'
    
    return entries

def insert_citekey_to_note(
        bibtex_entries: List[BibTexEntry], 
        prefix: str = '', 
        suffix: str = ''
        ) -> List[BibTexEntry]:
    """Returns a list of BibTexEntry with citekey in 'note' field. If 'note' 
    field does not exist in the input data, note field will be created, 
    otherwise citekey is added at the end. 

    Parameters
    ----------
    bibtex_entries: List[BibTexEntry]
    prefix: str (optional: '' by default)
    suffix: str (optional: '' by default)

    Return
    ------
    List[BibTexEntry]
    """
    new_bibtex_entries = []

    for entry in bibtex_entries:
        out_entry = insert_citekey(entry, prefix, suffix)
        new_bibtex_entries.append(out_entry)

    return new_bibtex_entries

def save_as_BibTex_file(
        bibtex_entries: List[BibTexEntry], 
        output_file_path: str) -> None:
    """Create a new BibTex file for the given entries. Please note that this 
    function does not raise an error if a file exists at the output_file_path but
    will overwrite the content of the existing file. 
    """
    out_lines = []

    for entry in bibtex_entries:
        out_lines.append(format_BibTexEntry_to_str(entry))

    with open(output_file_path, 'w') as f:
        print(f'% itemnum: {len(out_lines)}', file=f)
        print('\n'.join(out_lines), file=f)

# ================ Secondary functions ================ #

def get_BibTex_file_contents(file_path: str) -> List[str]:
    """Returns a list of strings. Each string is BibTex format of one reference 
    entry. In the future, it is better to convert each string to BibTexEntry 
    object inside this function. Currently, we are looping through all the 
    entries twice just to get a BibTexEntry list. 

    Parameter
    ---------
    file_path: str
        A path to the input BibTex file

    Return
    ------
    List[List[str]]
    """
    # Initialize a list that will be output
    contents: List[str] = []

    # Initialized a list in which information for one entry is collected
    tmp_lines = []

    # Open a file
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

            # If a line starts with @ sign, 
            if line.startswith('@'):
                # If tmp_lines includes some data from the last entry,  
                if len(tmp_lines) > 0:
                    # Add the tmp_lines to output list, contents. 
                    # NOTE: Here, we can pass the string to a function that 
                    # converts a string to BibTexEntry. 
                    contents.append(''.join(tmp_lines))

                # Initialize tmp_lines
                tmp_lines = []

                # Add the information in this line to tmp_lines
                tmp_lines.append(line)

            # If a line is not either a comment line, empty line, or a line with @,
            else:
                # Add to tmp_lines
                tmp_lines.append(line)

    # Add tmp_lines for the last entry to contents
    # NOTE: Here, we can pass the string to a function that converts a string 
    # to BibTexEntry. 
    contents.append(''.join(tmp_lines))

    return contents

def convert_str_to_BibTexEntry(entry: str) -> BibTexEntry:
    """Returns a given entry (string) in BibTexEntry object. This function will 
    raise errors if
    - a given entry is not a string object
    - the given entry does not start with @ sign
    - the given entry does not have {
    - the given entry does not ends with }

    """
    # Check if this is string
    assert isinstance(entry, str)
    
    # Check if string starts with @
    assert entry.startswith('@')
    assert '{' in entry
    # Get entry_type
    entry_type = entry[1:].split('{')[0]
    
    # Get data after entry_type
    entry_wo_entry_type = entry[1:].split(entry_type)[1]
    # Check if data starts with {
    assert entry_wo_entry_type.startswith('{')
    # Check if data ends with }
    assert entry_wo_entry_type.endswith('}')

    # Get citekey
    citekey = entry_wo_entry_type[1:-1].split(',')[0]
    
    # Get field and value pairs. The corresponding field and value is in 
    # neighboring element in this list
    meta_data: List[str] = entry_wo_entry_type[1:-1].lstrip(citekey)\
        .lstrip(',').split('=')

    # Collect data into a dictionary
    data = {}
    for i, element in enumerate(meta_data):
        # If this is the first element in the list
        if i == 0:
            # This element is field for the first item. 
            # Remove empty characters on the right and left sides and assign to 
            # `field` variable
            field = element.strip()

        # If this is the last element in the list
        elif i == len(meta_data)-1: 
            # Assign to data with `field` obtained from the element one before 
            # this. 
            data[field] = element.rstrip()

        # If this is the second to second last element,
        else:
            # Split the element by comma. 
            parts: List[str] = element.strip().split(',')
            # Get value for the previous field, which is obtained from the 
            # element one before. 
            prev_field_value: str = ','.join(parts[:-1]) 

            # Add to the data dictionary
            data[field] = prev_field_value 

            # The string at the end is `field` for the next value
            field = parts[-1]

    # Create BibTexEntry
    return BibTexEntry(citekey, entry_type, data)

def insert_citekey(
        entry: BibTexEntry, 
        prefix: str = '', suffix: str = '') -> BibTexEntry:
    """Insert citekey (with prefix and suffix strings if specified) to note 
    field in a given BibTexEntry. If note field does not exist, this function 
    will make note field. The returned BibTexEntry object is the input one with 
    modification of its `data` dictionary. 
    """
    # NOTE: Here is hard-coded. This can be a user-accessible argument so that
    # users can specify the field to insert citekey. 
    insert_field = 'note'

    # If field does not exist
    if insert_field not in entry.data:
        # Create a new field and assign a string including citekey
        entry.data[insert_field] = '"' + prefix + entry.citekey + suffix + '"'

        return entry

    # If field exists
    # Get the existing note and remove double quotations on right and left sides
    existing_note = entry.data[insert_field].strip('"')
    # Create a new node with citekey at the end of lines. 
    new_note = '"' + existing_note + f'\n{prefix}{entry.citekey}{suffix}' + '"'
    # Replace with the existing one
    entry.data[insert_field] = new_note

    return entry

def format_BibTexEntry_to_str(entry: BibTexEntry) -> str:
    """Returns a string in a BibTex format. 

    Format
    ------
    @entry_type{citekey,
    data
    }
    """
    # Convert data (dict) to a string
    data_str = '\n'.join([
        field + ' = ' + value + ','
        for field, value in entry.data.items()
    ])

    return f'@{entry.entry_type}' + '{' + entry.citekey \
        + f',\n{data_str}' + '\n}'

def cut_quotation(string: str) -> str:
    """Returns a string without empty characters and quotations (' and ") at 
    both ends. 
    """
    # Remove empty characters at both ends
    string = string.strip()

    if '"' in string:
        msg = f'Unexpected number of double quotations is found in {string}. '\
               'should be 2.'
        assert string.count('"') == 2, msg
        assert string.startswith('"'), '" is not at the beginning.'
        assert string.endswith('"'), '" is not at the end.'

        string = string.strip('"')

    if "'" in string:
        msg = f'Unexpected number of single quotations is found in {string}. '\
               'should be 2.'
        assert string.count("'") == 2, msg
        assert string.startswith("'"), "' is not at the beginning."
        assert string.endswith("'"), "' is not at the end."

        string = string.strip('"')

    return string

def read_control_file(
        control_file_path: str, 
        expected_sections: Union[Set[str], List[str]] = {'REQUIRED', 'OPTIONAL'}
        ) -> dict:
    """Returns a dictionary of arguments listed in the given file. 
    """
    assert isinstance(control_file_path, str)

    # Initialize ConfigParser object
    config = configparser.ConfigParser(
        strict=True,
        comment_prefixes=('#', ';'),
        inline_comment_prefixes=('#', ';')
    )

    # Parse control file
    paths = config.read(control_file_path)

    # Check the number of read control files.
    if len(paths) == 0:
        msg = f'Specified control file, {control_file_path}, is not found.'
        raise FileNotFoundError(msg)
    elif len(paths) > 1:
        msg = f'Multiple files are given: {paths}. Please give one file.'
        raise TypeError(msg)
    
    # Check if expected sections exist in the file
    for expected_section in expected_sections:
        assert expected_section in config.sections(), \
            f'{expected_section} is not found in control file.'

    # Flatten arguments
    args = {
        key: cut_quotation(value)
        for expected_section in expected_sections
            for key, value in config[expected_section].items()
    }
    return args

if __name__ == '__main__':
    desc = 'Insert citekey into "note" field.'
    parser = argparse.ArgumentParser(description=desc)

    # Define expected arguments
    parser.add_argument(
        "-i", "--input_file_path", 
        help="A path to an input BibTex file.", 
        type=str
    )
    parser.add_argument(
        "-o", "--output_file_path", 
        help="A path to an output file.", 
        type=str
    )
    parser.add_argument(
        "-p", "--prefix", 
        help="Prefix string in the inserted string in the note field.", 
        type=str, nargs='?', default=''
    )
    parser.add_argument(
        "-s", "--suffix", 
        help="Suffix string in the inserted string in the note field.",
        type=str, nargs='?', default=''
    )
    parser.add_argument(
        "-c", "--control_file_path", 
        help="A path to an control file, where parameters are listed in the "\
             "file. Note that other command-line arguments will be ignored if "\
             "a control file is given.", 
        type=str, nargs='?', default=''
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Call main function
    if args.control_file_path == '':
        main(
            args.input_file_path, 
            args.output_file_path,
            args.prefix,
            args.suffix
        )
    else:
        args_from_ctl = read_control_file(args.control_file_path)
        main(**args_from_ctl)

