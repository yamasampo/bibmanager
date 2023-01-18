# bibmanager

parses a BibTex file (obtain entry type, citekey and 
other data), creates "note" field if it does not exist, and adds citekey 
to the "note" field. 

Currently, this script accepts only a BibTex file format ([BibTex official], 
[Wikipedia], [PaperPile article]), but other formats, such as CSV and JASON 
formats, may be supported in the future. 

## Table of Contents

1. [Input Arguments](#input-arguments)
2. [About BibTex File Format](#about-bibtex-file-format)
3. [How To Use](#how-to-use)
4. [Future Implementation](#future-implementation)

## Input Arguments

- input file path (required)
- ouptut file path (required)
- prefix (optional)
- suffix (optional)

A user can pass these arguments via a control file, which should be ]
formatted like `sample.ctl`. 

## About BibTex file format

In the BibTex file format, each entry is defined by @ and a curly bracket. 
Here is an example, 

```
@ARTICLE{Talbert2022-wc,
title = "Viral histones: pickpocket's prize or primordial progenitor?",
author = "Talbert, Paul B and Armache, Karim-Jean and Henikoff, Steven",
abstract = "The common histones ...",
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
```

This format mainly includes three types of information: entry type, entry ID 
(so called citekey), and other properties of the entry. 

- Entry type can be found as a string between @ and the open parenthesis 
(ARTICLE in this example). An entry type is not a case sensitive property. 
Currently, BibTex has a total of 14 entry types, a [PaperPile article] says. 

- Citekey can be found as a string between an open parenthesis and the first
comma (Talbert2022-wc in this example). The citekey should be assigned 
uniquely to entries in a BibTex file. This script checks this. 

- Other properties follows citekey and are listed as pairs of field and 
value. Field and value are separated by = sign. 

There are many other specifics in BibTex format and please refer to others' 
explanations for details. I found [articles by PaperPile] very informative. 

Below shows what you will find in an output file if you input the BibTex 
sample above. Since the input does not have `note` field, it is created, and
citekey "Talbert2022-wc" is added to the `note` field with prefix "221017_PaperPile_citekey: ". 

```
@ARTICLE{Talbert2022-wc,
title = "Viral histones: pickpocket's prize or primordial progenitor?",
author = "Talbert, Paul B and Armache, Karim-Jean and Henikoff, Steven",
abstract = "The common histones ...",
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
```

## How To Use

```
usage: insert_citekey_to_note_bib.py [-h] [-i INPUT_FILE_PATH] [-o OUTPUT_FILE_PATH] [-p [PREFIX]] [-s [SUFFIX]] [-c [CONTROL_FILE_PATH]]

Insert citekey into "note" field.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE_PATH, --input_file_path INPUT_FILE_PATH
                        A path to an input BibTex file.
  -o OUTPUT_FILE_PATH, --output_file_path OUTPUT_FILE_PATH
                        A path to an output file.
  -p [PREFIX], --prefix [PREFIX]
                        Prefix string in the inserted string in the note field.
  -s [SUFFIX], --suffix [SUFFIX]
                        Suffix string in the inserted string in the note field.
  -c [CONTROL_FILE_PATH], --control_file_path [CONTROL_FILE_PATH]
                        A path to an control file, where parameters are listed in the file. Note that other command-line arguments will be ignored if a control file
                        is given.
```

Calling `insert_citekey_to_note_bib.py -h` or 
`python3 insert_citekey_to_note_bib.py -h` will show this usage on Terminal. 

## Future implementation

- [ ] Retrieve information from different file format (e.g., JASON, RIS, CSV and so on) and add to BibTex

- [ ] Add task controller so that users do not have to look for a script that does 
a job they want this package to do. Users just need to read this file and specify 
tasks by flags (e.g., running the current functionality by 
`bibmanager.py --insert_citekey -c [control_file]`). 


<!-- ## References -->

[BibTex official]: http://www.bibtex.org/Format/ 

[Wikipedia]: https://en.wikipedia.org/wiki/BibTeX

[PaperPile article]: https://www.bibtex.com/g/bibtex-format/ 

[articles by PaperPile]: https://www.bibtex.com/format/

