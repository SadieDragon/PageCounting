
from string import ascii_lowercase


class LetterIterator:
    current_index: int

    def __init__(self):
        '''
        Creates an iterator that goes a-z.
        `1: a`
        `27: aa`
        `53: ba`
        etc...
        '''
        # 1 based index, so init with 0
        self.current_index = 0

    # Needed to be able to call `next`
    def __iter__(self):
        return self

    # The actual method for `next`
    def __next__(self):
        return self.number_to_label()

    def number_to_label(self) -> str:
        '''
        Converts a number to a letter sequence.

        Returns:
            str: The next letter sequence
        '''
        # Figure out how many sets there are, and how far in the
        # current set the current number is
        sets, letter_index = divmod(self.current_index, 26)

        # If sets is not 0, then we need a first letter
        first_letter = ''
        if sets >= 1:
            # Remove 1, sets is a 1 indexed thing
            sets -= 1
            first_letter = ascii_lowercase[sets]

        # The second letter is how far into the set we are now
        second_letter = ascii_lowercase[letter_index]

        # Increment the index
        self.current_index += 1

        return f'{first_letter}{second_letter}'

    def reset(self) -> None:
        '''
        Reset the counter to 0.
        '''
        self.current_index = 0
