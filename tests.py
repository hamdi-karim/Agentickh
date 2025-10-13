import os
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file


# file_content = get_file_content("calculator", "main.py")
# print(file_content)

# file_content = get_file_content("calculator", "pkg/calculator.py")
# print(file_content)

# file_content = get_file_content("calculator", "/bin/cat")
# print(file_content)

# file_content = get_file_content("calculator", "pkg/does_not_exist.py")
# print(file_content)


# res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(res)

# res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(res)

# res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(res)

# _________

res = run_python_file("calculator", "main.py")
print(res)

res = run_python_file("calculator", "main.py", ["3 + 5"])
print(res)

res = run_python_file("calculator", "tests.py")
print(res)

res = run_python_file("calculator", "../main.py")
print(res)

res = run_python_file("calculator", "nonexistent.py")
print(res)

res = run_python_file("calculator", "lorem.txt")
print(res)
