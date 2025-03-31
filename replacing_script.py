
# This is a file for me to know what script I used to get the info
# used to replace pythonbible

from os import getcwd
from pathlib import Path
from pythonbible import get_references
from verse_validation.bible_utils import BOOKS


# Create dictionary of last chapter and last verse for each book
book_endpoints = {}
for book in BOOKS:
    references = get_references(book)[0]  # Get book reference
    book_endpoints[book] = (references.end_chapter, references.end_verse)

# The target util file
output_file = (Path(getcwd()) /
               'verse_validation' /
               'bible_utils' /
               'book_endpoints')
output_file = output_file.with_suffix('.py')
output_file.touch()

# Write a map myself- as a constant :D
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\nBOOK_ENDPOINTS = {\n')
    for book, (end_chapter, end_verse) in book_endpoints.items():
        f.write(f'    \'{book}\': ({end_chapter}, {end_verse}),\n')
    f.write('}\n')
