
from verse_validation.utils import query_points


def select_verse_range(book: str) -> list[str]:
    '''
    Queries what the first and last verse of the current page of the Bible
    are. Assumes the book is known.

    Args:
        book (str): The current book title.

    Returns:
        (list[str]): The list of verse endpoints.
    '''
    # Grab the verse endpoints
    endpoints = query_points('verse')

    # Append the book to the endpoints
    bookified_endpoints = []
    for endpoint in endpoints:
        bookified_endpoints.append(f'{book} {endpoint}')
