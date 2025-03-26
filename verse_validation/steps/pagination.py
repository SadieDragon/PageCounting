
# The final step.

from json import dump
from os import getcwd
from pathlib import Path
from re import compile


class Pagination:
    current_book: str
    verses_per_book: dict[str, list[str]]

    output_dir: Path

    pages: dict[int, list[list[str]]]
    page_count: int

    def __init__(self, valid_verses: list[str]):
        '''
        Runs the processes to paginate a set of valid verses.
        '''
        # Init the holding variables
        self.current_book = ''
        self.pages = {}
        self.page_count = 0

        # Process the valid verses down into books
        self.verses_per_book = {}
        self.make_verses_per_book_dict(valid_verses)

        # Create the path to the output dir
        self.output_dir = Path(getcwd()) / 'pages_per_book'
        # Make it if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)

        # Do the processing thing
        self.process_verses()

    def make_verses_per_book_dict(self, valid_verses: list[str]) -> None:
        '''
        Processes valid verses into a dict, `{book: [verses]}`

        Args:
            valid_verses (list[str]): The list of valid verses.
        '''
        # This regex will match formats like `Genesis 1:1` and `1 Kings 1:1`
        verse_pattern = compile(r"^(\d*[\sA-Za-z]+)\s(\d+:\d+)$")

        # Iterate through the valid verses
        for verse in valid_verses:
            # Break the str into ['book', 'chapter:verse']
            match = verse_pattern.match(verse)

            # If match is invalid... pretend nothing happened? Hah? ha...
            if not match:
                continue

            # Book will be first, then the `chapter:verse`
            book = match.group(1)
            verse_only = match.group(2)

            # If this is a new book, create the blank
            # list for its verses to go into
            if not (book in self.verses_per_book):
                self.verses_per_book[book] = []

            # Store the verse in that book
            self.verses_per_book[book].append(verse_only)

    def save_pages_to_file(self, book: str) -> None:
        '''
        Writes the current page contents to a JSON, named after the book.

        Args:
            book (str): The current book.
        '''
        # Create the path to the file
        file_path = (self.output_dir / book).with_suffix('.json')

        # Dump to file
        with file_path.open('w', encoding='utf-8') as f:
            dump(self.pages, f, indent=2)

    def fill_pages(self, verses: list[str]) -> None:
        '''
        Processes a set of verses into pages.

        Args:
            verses (list[str]): The list of verses to process.
        '''
        # Convert verses into an iterator, to make it easier to
        # process them into a set of pages
        verses_iter = iter(verses)

        # Reset the stopping flag
        to_stop = False

        # For all of the verses, dump them into columns and pages
        while not to_stop:
            # Reset the page, increment the counter
            page = []
            self.page_count += 1

            # 5 columns per page
            for _ in range(5):
                # Reset the column
                column = []

                # 22 rows per column
                for _ in range(22):
                    # Try to append a new verse to the column
                    try:
                        column.append(next(verses_iter))
                    # If we can't, then flag to stop
                    except StopIteration:
                        to_stop = True
                        break

                # Store the column
                page.append(column)

            # If the page is not empty, then store it
            self.pages[self.page_count] = page

    def process_verses(self) -> None:
        '''
        Processes the verses into pages.
        '''
        # Iterate through the broken down dict
        for book, verses in self.verses_per_book.items():
            # Process the verses into pages
            self.fill_pages(verses)

            # Dump the pages into the yaml
            self.save_pages_to_file(book)
