
# This is step 3 of the process.

def validate_verses(footnotes_per_verse: dict[str, list[str]]) \
        -> list[list[str]]:
    '''
    Queries if any footnote in the verse is a valid reference.

    Args:
        footnotes_per_verse (dict[str, list[str]]): A dict of verses with a
            list of footnotes mapped to them.

    Returns:
        (list[list[str]]): The valid verses, the invalid verses.
    '''
    # The output list
    valid_verses = []
    invalid_verses = []

    # Iterate through the dict
    was_valid = False
    for verse, footnotes in footnotes_per_verse.items():
        # Iterate through the footnotes to check if any are valid
        for footnote in footnotes:
            # Query if the footnote has verses
            msg = f'Does "{footnote}" have any references? (y / n) '
            has_refs = input(msg)

            # If the answer is "y" (or "yes"), then the verse is valid
            # store it, and break out of the loop
            if 'y' in has_refs:
                valid_verses.append(verse)
                was_valid = True
                break

        # If it was not valid, store it in the invalid verses
        if not was_valid:
            invalid_verses.append(verse)

        # Ensure the flag is always reset
        was_valid = False

    return [valid_verses, invalid_verses]
