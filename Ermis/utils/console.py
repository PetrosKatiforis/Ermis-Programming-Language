import os

def clear_console():
    """
    Clears the console of the interpreter
    Works for all Windows, Linux and MacOS
    """

    os.system("cls" if os.name == "nt" else "clear")

def red(message):
    """
    Returns a red colored message
    """

    return f"\33[41m {message} \33[0m"
