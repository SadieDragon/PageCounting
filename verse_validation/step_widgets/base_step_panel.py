
from collections.abc import Callable  # https://stackoverflow.com/a/71118433
from customtkinter import CTk, CTkEntry, CTkFrame, CTkLabel


class BaseStepPanel(CTkFrame):
    parent: CTk

    callback: None

    def __init__(self, parent: CTk, callback=None):
        '''
        The base class for step widgets.
        '''
        # Create the panel
        super().__init__(parent)
        self.pack(padx=5, pady=5)

        # Store the parent window to create keybinds
        self.parent = parent

        # Store the callback fn
        self.callback = callback

    def add_bind(self, key: str, fn: Callable[[], None]) -> None:
        '''
        A wrapper for binding a key to a fn without
        spamming it with keypress information.

        Args:
            key (str): The keysm for the key that's to be bound.
            fn (Callable[[], None]): The fn to bind to.
        '''
        self.parent.bind(f'<{key}>', lambda _: fn())

    def create_label_entry_frame(self, text: str) -> CTkEntry:
        '''
        Create a frame with a label packed next to the entrybox.

        Args:
            text (str): The text to go in the label.

        Returns:
            (CTkEntry): The entry box, to be accessed for data later.
        '''
        # Create a frame to grid things into
        new_frame = CTkFrame(master=self)
        new_frame.pack(padx=5, pady=5)

        # Create a label
        new_label = CTkLabel(master=new_frame, text=text)
        new_label.grid(column=0, padx=5, pady=5, row=0, sticky='W')

        # Create the entry box
        new_entry = CTkEntry(master=new_frame, width=75)
        new_entry.grid(column=1, padx=5, pady=5, row=0, sticky='E')

        return new_entry

    def enforce_focus(self, target_entry: CTkEntry) -> None:
        '''
        A quick wrapper for enforcing focus is set
        to the specified entry upon frame initialization.

        Args:
            target_entry (CTkEntry): The target entry to force focus on.
        '''
        # Delay focus setting slightly, to enforce focus on the entry
        self.after(100, lambda: target_entry.focus())

    def get_entry_response(self, entry: CTkEntry) -> str:
        '''
        A wrapper for getting data from an entry.
        '''
        return entry.get().strip()
