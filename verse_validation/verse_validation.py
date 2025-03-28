
from json import dump, load
from os import getcwd
from pathlib import Path
from pythonbible import get_references
from verse_validation.steps import (CreateFootnotesPerVerseDict,
                                    Pagination,
                                    # select_verse_range,
                                    validate_verses)
from verse_validation.utils import BookIterator


class VerseValidation:
    '''
    The process to do verse validation, all in one file.

    Includes graceful stopping and starting.
    '''
    session_file: Path
    valid_verses_file: Path

    book_endpoint: str
    book_iter: BookIterator
    current_book: str
    page_of_bible: int

    valid_verses: list[str]

    pages_to_do: int

    def __init__(self, pages_to_do: int, reload_from_error=False):
        # Store how many pages to do
        self.pages_to_do = pages_to_do

        # Create the root path to the output dir
        output_dir = Path(getcwd()) / 'session_data'
        # Create the paths to the output files
        self.session_file = (output_dir / 'session_state')
        self.session_file = self.session_file.with_suffix('.json')
        self.valid_verses_file = (output_dir / 'valid_verses')
        self.valid_verses_file = self.valid_verses_file.with_suffix('.txt')

        # Init the book iterator
        self.book_iter = BookIterator()

        # Init valid verses
        self.valid_verses = []

        # Load the session data
        self.load_session(reload_from_error)

        # And run the program
        self.verse_validation()

    # Session Saving ==========================================================

    def dump_valid_verses(self) -> None:
        '''
        Dump the valid verses to a file.
        '''
        # Ensure the file exists
        self.valid_verses_file.touch()

        # Dump the verses into the file
        with self.valid_verses_file.open('a', encoding='utf-8') as f:
            # Dump the individual verses onto each line
            for verse in self.valid_verses:
                f.write(f'{verse}\n')

    def load_session(self, reload_from_error: bool) -> None:
        '''
        Load session progress from the output file.

        Args:
            reload_from_error (bool): If true, then grab the valid verses
                from the session data.
        '''
        # If this is our first session, load blank data
        if not self.session_file.exists():
            # Init the book iterator, and set the first endpoint
            self.current_book = next(self.book_iter)
            self.get_last_verse()

            # Init the page to be 0
            self.page_of_bible = 0

            # Break out
            return

        # Otherwise, load the previous session data
        with self.session_file.open('r', encoding='utf-8') as f:
            session_data = load(f)

        # Store the chunks of the session data
        self.current_book = session_data['current_book']
        self.book_endpoint = session_data['last_verse']
        # Ensure that the book iterator is set properly
        self.set_current_book()

        # Load the last page number
        self.page_of_bible = session_data['last_page']

        # If we are reloading from a crash, reload the verse data
        if reload_from_error:
            self.valid_verses = session_data['valid_verses']

    def save_session(self) -> None:
        '''
        Saves current session progress to a file.
        '''
        # Store the current session data
        session_data = {
            'current_book': self.current_book,
            'last_verse': self.book_endpoint,
            'last_page': self.page_of_bible,
            'valid_verses': self.valid_verses
        }

        # Dump the data to a json
        with self.session_file.open('w', encoding='utf-8') as f:
            dump(session_data, f, indent=2)

    # =========================================================================

    # Book Iter Functions =====================================================

    def get_last_verse(self) -> None:
        '''
        Sets the endpoint verse for the current book.
        '''
        # Get the normalized refs for the book
        book_ref = get_references(self.current_book)[0]

        # Grab the end chapter and verse for PEP8 compliance cleanliness
        end_chapter = book_ref.end_chapter
        end_verse = book_ref.end_verse

        # Set the endpoint
        self.book_endpoint = (f'{self.current_book} {end_chapter}:{end_verse}')

    def set_current_book(self) -> None:
        '''
        Updates the book iterator to be at the current book.
        '''
        while self.current_book != self.book_iter.current_title:
            next(self.book_iter)

    # =========================================================================

    # =========================================================================

    def verse_validation(self) -> None:
        '''
        Runs all of the processes together to validate verses.
        '''
        # A flag for "end of Bible"
        to_paginate = False

        # For the pages we wanted to do:
        for _ in range(self.pages_to_do):
            # Increment the page of the Bible we are on
            self.page_of_bible += 1

            # Get the range of verses
            # verse_range = select_verse_range(self.current_book,
            #                                  self.page_of_bible)
            verse_range = []

            # Get the footnotes per verse
            f_p_v = CreateFootnotesPerVerseDict(verse_range,
                                                self.valid_verses)
            f_p_v = f_p_v.footnotes_per_verse

            # Add the new valid verses to the old
            self.valid_verses = self.valid_verses + validate_verses(f_p_v)

            # If the last verse of the range is the book endpoint,
            # increment the book we are on
            if verse_range[-1] == self.book_endpoint:
                # If the current book is Revelation, break out, it's time!
                if 'Rev' in self.current_book:
                    # Set the flag, and get out
                    to_paginate = True
                    break

                self.current_book = next(self.book_iter)
                self.book_endpoint = self.get_last_verse()

            # Save session data after each iteration just to be safe
            self.save_session()

        # Dump valid verses into the text file
        self.dump_valid_verses()

        # If we are to paginate, paginate
        if to_paginate:
            Pagination()

    # =========================================================================
