
# This is step 1.

from pythonbible import (convert_reference_to_verse_ids,
                         convert_verse_ids_to_references,
                         format_scripture_references,
                         get_references)
from collections.abc import Callable


# TODO: TO make the task of saving the last verse on a page should a
# rollover occur, perhaps also turn this into a class.
# Also need to figure out a way to implement an increment to go
# "previous last verse" or "the verse after the previous last verse"?

def select_verse_range(book: str,
                       query_fn: Callable[[int], list[str]],
                       current_page: int) \
        -> list[str]:
    '''
    Asks what the first and last verse of a page are, then creates a
    list of verses between those points. Assumes that the book is known.

    Args:
        book (str): The current book title.
        query_fn (Callable[[int], list[str]]): The function which will query
            the verse endpoints of the page.
        current_page (int): The current page number; passed to `query_fn`.

    Returns:
        (list[str]): The list of verses on the page, given the user
            selected first and last verse.
    '''
    # Request the first and last verse of the page
    endpoints = query_fn(current_page)

    # Create the verse string
    verse_range = f'{book} {endpoints[0]}-{endpoints[1]}'

    return _create_list_of_verses(verse_range)


def _create_list_of_verses(verse_str: str) -> list[str]:
    '''
    Take the input string and convert it to a list of verses.

    Args:
        verse_str (str): Ex: `Gen 1:1-2:5`

    Returns:
        (list[str]): A list of verses.
    '''
    # Convert the input str into a NormalizedReference
    verse_str_ref = get_references(verse_str)[0]

    # Convert the NormalizedReference into a list of verse ids
    verse_ids = convert_reference_to_verse_ids(verse_str_ref)

    # Convert each id to a verse str again
    list_of_verses = []
    for verse_id in verse_ids:
        # Convert the verse id (as a list) to a NormalizedReference
        verse_ref = convert_verse_ids_to_references([verse_id])

        # Format it back into a str, and append to list of verses
        list_of_verses.append(format_scripture_references(verse_ref))

    return list_of_verses
