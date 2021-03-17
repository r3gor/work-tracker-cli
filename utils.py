def controled_input(validator, msj, type):
    s = type(input(f"{msj}:\t"))
    while not validator(s):
        print("type a valid value!")
        s = type(input(f"{msj}:\t"))
    return s