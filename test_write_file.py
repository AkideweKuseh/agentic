from functions.write_file import write_file

def test_write_file():
    print("=== Overwriting lorem.txt ===")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    print("\n=== Writing to new file in pkg ===")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("\n=== Writing outside working directory ===")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    test_write_file()
