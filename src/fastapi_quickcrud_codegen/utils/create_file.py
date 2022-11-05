import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_file_and_add_code_into_there(path, code):
    with open(path, 'a') as model_file:
        model_file.write(code)
