
from customtkinter import CTkEntry, CTkFrame


def enforce_focus(parent_frame: CTkFrame, target_entry: CTkEntry) -> None:
    '''
    A quick wrapper for enforcing focus is set
    to the specified entry upon frame initialization.

    Args:
        parent_frame (CTkFrame): The parent widget to set the delay on.
        target_entry (CTkEntry): The target entry to force focus on.
    '''
    # Delay focus setting slightly, to enforce focus on the entry
    parent_frame.after(100, lambda: target_entry.focus())
