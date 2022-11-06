import os


def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def create_file_and_add_code_into_there(path: str, code: str):
    with open(path, 'a') as model_file:
        model_file.write(code)
