
# This is a file for me to know what script I used to get the info
# used to replace pythonbible

from os import getcwd
from pathlib import Path
from pythonbible import get_references
from verse_validation.bible_utils import BOOKS, BOOK_ENDPOINTS
from yaml import safe_dump


# Target output file
root_dir = Path(getcwd())
# constants_dir = root_dir / 'verse_validation' / 'bible_utils' / 'constants'
output_file = (root_dir / 'chapter_endpoints').with_suffix('.yaml')

# Dict to store chapter endpoints
chapter_endings: dict[str, dict[int, int]] = {}

# Populate the dict
for book in BOOKS:
    # Add the book to the dict with a blank dict
    chapter_endings[book] = {}

    # Get the last chapter of the book
    last_chapter = BOOK_ENDPOINTS[book][0]

    # Iterate over each chapter
    for chapter in range(1, (last_chapter + 1)):
        # Grab the chapter reference
        chapter_ref = get_references(f'{book} {chapter}')[0]

        # Grab the end verse
        last_verse = chapter_ref.end_verse

        # Store the chapter and its last verse
        chapter_endings[book][chapter] = last_verse

with output_file.open('w', encoding='utf-8') as f:
    safe_dump(chapter_endings, f, indent=2, sort_keys=False)
