
from customtkinter import (CTk,
                           CTkButton,
                           CTkEntry,
                           CTkFrame,
                           CTkInputDialog,
                           CTkLabel,
                           StringVar)
from typing import Iterator
from re import match
from verse_validation.gui_utils import create_label_entry_frame
from verse_validation.utils import LetterIterator


class CreateFootnotesPerVersePanel(CTkFrame):
    verse_iter: Iterator[list[str]]
    list_of_valid_verses: list[str]

    book: str
    footnotes_per_verse: dict[str, list[str]]
    current_verse: str
    current_first: str
    previous_verse: str
    previous_first: str

    verse_strvar: StringVar
    footnote_entry: CTkEntry
    submit_button: CTkButton

    # callback: None

    def __init__(self,
                 parent: CTk,
                 list_of_verses: list[str],
                 list_of_valid_verses: list[str],
                 callback=None):
        '''
        The panel for the second step of the process: Selecting footnotes
        per verse

        Args:
            parent (CTk): The parent window.
            list_of_verses (list[str]): The list of verses to get footnotes
                for.
            list_of_valid_verses (list[str]): The list of verses to skip.
            callback: To-be-defined - Used to return to the parent class
                with the information.
        '''
        # Create the frame for all of this stuff to go into
        super().__init__(parent)
        self.pack(padx=5, pady=5)

        # Store the book, which is always attached to any verse in the list
        # Checks for things like `Genesis`, `1 Kings`, `Song of Solomon`
        pattern = r'^(.*?)\d+:\d+$'
        self.book = match(pattern, list_of_verses[0]).group()

        # Store the inputs
        self.verse_iter = iter(list_of_verses)
        self.list_of_valid_verses = list_of_valid_verses
        self.callback = callback

        # Create the holding vars
        self.footnotes_per_verse = {}
        self.current_verse = ''
        self.current_first = ''
        self.previous_verse = ''
        self.previous_first = ''

        # Create a StringVar to go 'Current Verse: {verse}`
        self.verse_strvar = StringVar(self)
        # Create a label to display the stringvar
        info_label = CTkLabel(self, textvariable=self.verse_strvar)
        info_label.pack(padx=5, pady=5)

        # Create the entry for the footnote
        text = 'What is the first footnote?'
        self.footnote_entry = create_label_entry_frame(self, text)

        # Create a button for the user to confirm and finish
        self.submit_button = CTkButton(self,
                                       text='Confirm',
                                       command=self.process_entry)
        self.submit_button.pack(padx=5, pady=5)

        # TODO: Can I bind "enter" to confirm?

        self.load_next_verse()

    def ask_for_last_footnote(self) -> None:
        '''
        Creates an input dialog for the final footnote, and updates
        the last verse.
        '''
        # Create a dialogue window for the last footnote
        text = 'What is the last footnote?'
        last_footnote_dialog = CTkInputDialog(title='Last Footnote', text=text)

        # Get the input from the dialogue window
        last_footnote = last_footnote_dialog.get_input()

        # If they selected "Cancel", or did not put anything in, re-request
        if (last_footnote is None) or (not last_footnote):
            self.ask_for_last_footnote()

        # Otherwise, process the final footnote and last verse entry
        self.current_first = last_footnote
        self.process_last_footnote()

    def create_footnote_list(self) -> list[str]:
        '''
        Creates a list of footnotes, based on the
        starting footnote and ending footnote.

        Returns:
            (list[str]): A list of footnotes between the
                first footnote (inclusive) and the selected
                final footnote (inclusive).
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

        return footnote_list

    def load_next_verse(self) -> None:
        '''
        Attempts to load the next verse and update the label.
        If `StopIteration`, then return to callback fn.
        '''
        # Attempt to load the next verse and update the label
        try:
            # Go to the next verse
            self.current_verse = next(self.verse_iter)

            # If valid verse, attempt to load the next verse
            if (self.current_verse in self.list_of_valid_verses):
                self.load_next_verse()

            # If not a pre-validated verse, update the label
            # and empty out the entry box
            self.verse_strvar.set(f'Current Verse: {self.current_verse}')
            self.footnote_entry.delete(0, 'end')

        # If `StopIteration`, then we are done and need to wrap up
        except StopIteration:
            self.ask_for_last_footnote()

    def process_entry(self) -> None:
        '''
        Processes the entry, and either proceeds with footnote processing,
        or initiates a skip.
        '''
        # Removes any trailing whitespace when getting the footnote
        # Also, lowercase the footnote should I accidentally have caps on
        footnote = self.footnote_entry.get().strip().lower()

        # If blank, then just load the next verse
        if not footnote:
            self.load_next_verse()
            return

        # TODO: skip keybind
        # If 'skip', then initiate a skip
        if footnote == 'skip':
            self.skip_verses()
            return

        # TODO: "undo" - go back a verse
        # TODO: undo keybind

        # Otherwise, we have a valid first foonote
        self.current_first = footnote

        # If there is a previous entry, update it
        if self.previous_first:
            # Create the base list
            self.update_previous_entry()
            # Pop the last footnote from the list
            self.footnotes_per_verse[self.previous_verse].pop()

        # Store the current first footnote in the entry
        self.footnotes_per_verse[self.current_verse] = self.current_first

        # Update previous
        self.previous_verse = self.current_verse
        self.previous_first = self.current_first

        # Load the next verse
        self.load_next_verse()

    def process_last_footnote(self) -> None:
        '''
        Updates the final verse entry using the input last footnote.
        '''
        # Update the final verse entry
        self.update_previous_entry()

        # Return to callback
        # self.callback(self.footnotes_per_verse)
        print(self.footnotes_per_verse)  # DEBUG
        self.destroy()

    def skip_verses(self) -> None:
        '''
        The process for skipping verses.
        '''
        # Ask which verse to skip to
        text = 'Skip to which verse? (Just need `chapter:verse`)'
        skip_to_dialog = CTkInputDialog(title='Skip Verses', text=text)

        skip_to = skip_to_dialog.get_input()

        # TODO: "Hey, uhm, I changed my mind. I don't wanna skip, actually"
        # If they select none, or empty str, then re-run the query
        if (skip_to is None) or (not skip_to):
            self.skip_verses()
            return

        # TODO: keybind?
        # If they select `end`, jump to the end of the page
        if skip_to == 'end':
            self.ask_for_last_footnote()
            return

        # Prepend the book
        skip_to = self.book + skip_to

        # Otherwise, try to load the next verse until the selected verse
        while (self.current_verse != skip_to):
            self.load_next_verse()

    def update_previous_entry(self) -> None:
        '''
        Updates the previous entry in the footnotes per verse dict with
        a footnote list instead of simply the first footnote.
        '''
        # Create the footnote list
        footnote_list = self.create_footnote_list()
        # Update the previous entry
        self.footnotes_per_verse[self.previous_verse] = footnote_list
