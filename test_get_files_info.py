from functions.get_files_info import get_files_info

# List of directories to test
test_cases = [".", "pkg", "/bin", "../"]

for i, directory in enumerate(test_cases, start=1):
    # Call the function
    result = get_files_info("calculator", directory)

    # Header
    if directory == ".":
        print(f"{i}. get_files_info('calculator', '.'):") 
        print("Result for current directory:")
    else:
        print(f"{i}. get_files_info('calculator', '{directory}'):")
        print(f"Result for '{directory}' directory:")

    # Indent result lines for readability
    for line in result.split("\n"):
        print("    " + line)

    # Separator
    print()
