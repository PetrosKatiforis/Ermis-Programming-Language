from time import sleep

def ermis_print(parameters):
    print(*parameters)

def ermis_wait(parameters):
    sleep(parameters[0])

def ermis_input(parameters):
    return input(parameters[0])

def ermis_sqrt(parameters):
    return parameters[0] ** 0.5
