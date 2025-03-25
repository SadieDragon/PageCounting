
from verse_validation.utils import LetterIterator


def create_footnote_list() -> list[str]:
    '''
    Asks for the last footnote on the page, and creates a
    list of footnotes `a-last_footnote`.

    Returns:
        (list[str]): A list of footnotes between a and the selected endpoint.
    '''
    # Query the user for the last footnote on the page
    last_footnote = input('What is the last footnote on the page? ')

    # Create the letter iterator used to generate the list
    letter_iterator = LetterIterator()

    # Until the last footnote of the list is the last footnote on the
    # page, generate a list of footnotes
    footnote_list = []
    current_note = ''
    while (current_note != last_footnote):
        current_note = next(letter_iterator)
        footnote_list.append(current_note)

    return footnote_list
