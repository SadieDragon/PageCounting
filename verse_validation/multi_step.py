
from os import getcwd
from pathlib import Path
from pythonbible import get_references
from verse_validation.steps import (create_footnotes_per_verse_dict,
                                    select_verse_range,
                                    validate_verses)
from verse_validation.utils import BookIterator


def dump_valid_verses(valid_verses: list[str]) -> None:
    '''
    Dumps the valid verses into a file so the user can stop after 100 pages.

    Args:
        valid_verses (list[str]): The list of valid verses generated this run.
    '''
    # Create the path to the file
    output_file = Path(getcwd()) / 'valid_verses.txt'
    # Create it if it doesn't exist
    output_file.touch()

    # Dump the valid verses
    with output_file.open('a', encoding='utf-8') as f:
        f.write(f'{valid_verses}\n')


def get_last_verse(book: str) -> str:
    '''
    Gets the endpoint for a book, to know when to iterate.

    Args:
        book (str): The book title.

    Returns:
        (str): The endpoint.
    '''
    # Get the normalized reference for the book
    book_ref = get_references(book)[0]

    # The last chapter and verse will be `end`
    last_chapter = book_ref.end_chapter
    last_verse = book_ref.end_verse

    return f'{book} {last_chapter}:{last_verse}'


def multi_step() -> None:
    # The book iterator that will be used to pass books to the first step
    book_iter = BookIterator()

    # Grab the first endpoint
    last_verse = get_last_verse(next(book_iter))

    # Init valid verses
    valid_verses = []

    # Let's do... 100 pages at a time. Yeah...
    # TODO: Make this better written to accommodate multiple sessions
    for _ in range(100):
        # Get the verses on the page
        verse_range = select_verse_range(book_iter.current_title)

        # If the last verse of the range is the endpoint, iterate the book
        if verse_range[-1] == last_verse:
            last_verse = get_last_verse(next(book_iter))

        # Get the footnotes per verse
        footnotes_per_verse = create_footnotes_per_verse_dict(verse_range,
                                                              valid_verses)

        # Validate the verses
        valid_verses = valid_verses + validate_verses(footnotes_per_verse)

    # Dump the valid verses into a text file for nice and clean stopping
    dump_valid_verses(valid_verses)
