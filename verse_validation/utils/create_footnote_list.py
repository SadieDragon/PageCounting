
from verse_validation.utils import LetterIterator


def create_footnote_list(first_footnote: str, last_footnote: str) -> list[str]:
    '''
    Creates a list of footnotes, based on the
    starting footnote and ending footnote.

    Args:
        first_footnote (str): The first footnote of the list.
        last_footnote (str): Where to stop the list. Gets popped off.

    Returns:
        (list[str]): A list of footnotes between the first footnote (inclusive)
            and the selected final footnote (exclusive).
    '''
    # Create the letter iterator used to generate the list
    letter_iterator = LetterIterator()

    # Create the placeholder var for the current note test
    current_note = ''

    # Iterate through the footnote iterator until
    # the first footnote is found
    while (current_note != first_footnote):
        current_note = next(letter_iterator)

    # Until the last footnote of the list is the last footnote on the
    # page, generate a list of footnotes
    footnote_list = [current_note]
    while (current_note != last_footnote):
        current_note = next(letter_iterator)
        footnote_list.append(current_note)

    return footnote_list
