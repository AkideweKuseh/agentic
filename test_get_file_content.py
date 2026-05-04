from functions.get_file_content import get_file_content

def test_get_file_content():
    print("=== Testing lorem.txt ===")
    content = get_file_content("calculator", "lorem.txt")
    print("Length:", len(content))
    print("Truncation message present:", '[...File "lorem.txt" truncated' in content)

    print("\n=== Testing main.py ===")
    print(get_file_content("calculator", "main.py"))

    print("\n=== Testing pkg/calculator.py ===")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n=== Testing /bin/cat (outside directory) ===")
    print(get_file_content("calculator", "/bin/cat"))

    print("\n=== Testing non-existent file ===")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    test_get_file_content()
