
# This is step 2 of the process.

from verse_validation.utils.letter_iterator import LetterIterator


class CreateFootnotesPerVerseDict:
    list_of_verses: list[str]
    list_of_valid_verses: list[str]

    footnotes_per_verse: dict[str, list[str]]
    previous_verse: str
    previous_first: str
    current_verse: str
    current_first: str

    to_skip: int

    def __init__(self,
                 list_of_verses: list[str],
                 list_of_valid_verses: list[str]):
        # Store the input vars
        self.list_of_verses = list_of_verses
        self.list_of_valid_verses = list_of_valid_verses

        # Init the holding vars
        self.footnotes_per_verse = {}
        self.to_skip = 0

        self.previous_verse = ''
        self.previous_first = ''

        self.current_verse = ''
        self.current_first = ''

        # Run the process
        return self.create_footnotes_per_verse_dict()

    def create_footnote_list(self) -> list[str]:
        '''
        Creates a list of footnotes, based on the
        starting footnote and ending footnote.

        Args:
            first_footnote (str): The first footnote of the list.
            last_footnote (str): Where to stop the list. Gets popped off.

        Returns:
            (list[str]): A list of footnotes between the
                first footnote (inclusive) and the selected
                final footnote (exclusive).
        '''
        # Create the letter iterator used to generate the list
        letter_iterator = LetterIterator()

        # Create the placeholder var for the current note test
        current_note = ''

        # Iterate through the footnote iterator until
        # the first footnote is found
        while (current_note != self.previous_first):
            current_note = next(letter_iterator)

        # Until the last footnote of the list is the last footnote on the
        # page, generate a list of footnotes
        footnote_list = [current_note]
        while (current_note != self.current_first):
            current_note = next(letter_iterator)
            footnote_list.append(current_note)

        # Remove the ending footnote
        footnote_list.pop()

        return footnote_list

    def create_footnotes_per_verse_dict(self) -> dict[str, list[str]]:
        '''
        Iterates through the generated list of verses to create a dict
        which represents footnotes per verse.

        Returns:
            (dict[str, list[str]]): `{verse: [list_of_footnotes]}`
        '''
        # Create footnote lists for all but the last verse
        for verse in self.list_of_verses:
            # If there is a count to skip, or if the verse is valid,
            # then skip the current verse
            if self.to_skip != 0:
                self.to_skip -= 1
                continue
            if verse in self.list_of_valid_verses:
                continue

            # Ask for the first footnote of the verse
            query_msg = (f'What is the first footnote of {verse}? '
                         '("skip" to initiate a block skip.)')
            self.current_first = input(query_msg)

            # If there was no footnote, skip
            if not self.current_first:
                continue

            # If the response is "skip", then init the skip
            if self.current_first == 'skip':
                # How many to skip?
                query_msg = 'How many verses to skip? (Including this verse) '
                # Remove 1 as we are skipping this verse
                self.to_skip = int(input(query_msg)) - 1

                # Skip the current verse
                continue

            # If there was a previous verse, then replace
            # the string with a list between its first and the current first
            if self.previous_first:
                # Create a list of footnotes between previous and current first
                footnote_list = self.create_footnote_list()

                # Store the footnote list in the previous verse
                self.footnotes_per_verse[self.previous_verse] = footnote_list

            # Update the previous to now be current
            self.previous_verse = verse
            self.previous_first = self.current_first

            # Store the first footnote for the current verse
            self.footnotes_per_verse[verse] = self.current_first

        # Ask what the last footnote of the page is
        self.current_first = input('What is the last footnote? ')

        # Create the last footnote list
        footnote_list = self.create_footnote_list()

        # Store it at the previous verse's location
        self.footnotes_per_verse[self.previous_verse] = footnote_list

        return self.footnotes_per_verse
