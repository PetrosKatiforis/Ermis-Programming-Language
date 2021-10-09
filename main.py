from Ermis import Ermis

def main():
    filename = input("Insert filename: ")

    interpreter = Ermis.from_filename(filename)
    interpreter.execute()

if __name__ == "__main__":
    main()
