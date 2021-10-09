from time import sleep

ermis_globals = {}

def builtin(function):
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
def διάβασε(message):
    return input(message)

@builtin
def ρίζα(number):
    return number ** 0.5


