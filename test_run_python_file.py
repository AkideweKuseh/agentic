from functions.run_python_file import run_python_file

def test_run_python_file():
    print("=== Run main.py (no args) ===")
    print(run_python_file("calculator", "main.py"))

    print("\n=== Run main.py with args ===")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("\n=== Run tests.py ===")
    print(run_python_file("calculator", "tests.py"))

    print("\n=== Attempt path escape ===")
    print(run_python_file("calculator", "../main.py"))

    print("\n=== Non-existent file ===")
    print(run_python_file("calculator", "nonexistent.py"))

    print("\n=== Not a Python file ===")
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    test_run_python_file()
