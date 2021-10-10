from time import sleep
import random

ermis_globals = {}

def builtin(function):
    """
    A decorator to save functions
    into the ermis_globals dictionary
    """
    
    ermis_globals[function.__name__] = function

@builtin
def εμφάνισε(*parameters):
    for param in parameters:
        if isinstance(param, bool):
            print(["Ψευδές", "Αληθές"][param], end=" ")
        else:
            print(param, end=" ")

    print()

@builtin
def περίμενε(delay):
    sleep(delay)

@builtin
def ρίζα(number):
    return number ** 0.5

@builtin
def mod(a, b):
    return a % b

@builtin
def div(a, b):
    return a // b

@builtin
def ακέραιος(x):
    return int(x)

@builtin
def τυχαίος_ακέραιος(start, end):
    return random.randint(start, end)

@builtin
def διάβασε(message):
    return input(message)


