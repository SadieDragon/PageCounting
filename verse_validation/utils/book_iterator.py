
from pythonbible import Book


class BookIterator:
    current_id: int
    current_title: str
    maximum: int

    def __init__(self):
        '''
        An iterator for the books of the Bible.
        '''
        self.current_id = 0
        self.current_title = ''
        self.maximum = 66

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_book()

    def next_book(self) -> str | None:
        '''
        Increments the book id, then converts that to the book title.

        Returns:
            (str): The current book title.
                (If None then we have reached the end.)
        '''
        # Increment current id
        self.current_id += 1

        # If it exceeds maximum, return None
        if self.current_id > self.maximum:
            return None

        # Otherwise, store and return the book title
        self.current_title = Book(self.current_id).title
        return self.current_title
