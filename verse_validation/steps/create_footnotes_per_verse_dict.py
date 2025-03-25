
# This is step 2 of the process.

from verse_validation.utils import create_footnote_list


def create_footnotes_per_verse_dict(list_of_verses: list[str],
                                    list_of_valid_verses: list[str]) \
                                    -> dict[str, list[str]]:
    '''
    Iterates through the generated list of verses to create a dict
    which represents footnotes per verse.

    Args:
        list_of_verses (list[str]): The list of verses to turn into keys.
        list_of_valid_verses (list[str]): The list of already checked verses.

    Returns:
        (dict[str, list[str]]): `{verse: [list_of_footnotes]}`
    '''
    # Iterate through the list of verses, and create the dict
    footnotes_per_verse = {}
    previous_verse = ''
    to_skip = 0
    for index, verse in enumerate(list_of_verses):
        # If there is a count to skip, then do so
        if to_skip != 0:
            to_skip -= 1
            continue

        # Skip any already valid verses
        if verse in list_of_valid_verses:
            continue

        # Otherwise, query the first footnote of the verse
        query_msg = (f'What is the first footnote of {verse}? '
                     '("skip" to initiate a block skip.) ')
        current_first = input(query_msg)

        # If there was no footnote, skip
        if not current_first:
            continue

        # If the response is "skip", then query "How many verses?"
        # and initiate the skip
        if current_first == 'skip':
            # Query how many to skip
            query_msg = ('How many verses to skip? (Including this verse) ')
            # Remove one as we are skipping this verse
            to_skip = int(input(query_msg)) - 1

            # Skip the current verse
            continue

        # Grab the previous verse's first note
        previous_first = footnotes_per_verse.get(previous_verse, '')

        # If there was a previous verse, then replace the string footnote
        # with a list of footnotes between the two footnotes
        if previous_first:
            # Create a list of footnotes between the two points
            footnote_list = create_footnote_list(previous_first, current_first)

            # Store the footnote list in the previous verse
            footnotes_per_verse[previous_verse] = footnote_list

        # If this is not the last verse, then store the first footnote
        value = current_first
        # If this is the last verse, then get the last footnote, and
        # create the final foonote list
        if (index == (len(list_of_verses) - 1)):
            # Get the last footnote
            final_footnote = input('What is the last footnote? ')

            # Create the list
            footnote_list = create_footnote_list(current_first, final_footnote)
            # Re-append the final footnote
            footnote_list.append(final_footnote)

            # Set the value
            value = footnote_list

        # Store in the dict
        footnotes_per_verse[verse] = value

        # Update previous verse
        previous_verse = verse

    return footnotes_per_verse
