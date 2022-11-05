import os
import sys

from ..misc.constant import GENERATION_FOLDER, MODEL
from ..utils.create_file import create_folder, create_file_and_add_code_into_there


class ModelTemplateGenerator:
    def __init__(self):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        self.current_directory = dirname
        self.template_root_directory = os.path.join(self.current_directory, GENERATION_FOLDER)
        self.module_path_map = {}

    def add_model(self, model_name, code):
        template_model_directory = os.path.join(self.template_root_directory, MODEL)
        create_folder(template_model_directory)

        path = f'{template_model_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_model_directory}/{model_name}.py'
        create_file_and_add_code_into_there(path, code)
        self.module_path_map[model_name] = {'model': path}

    @staticmethod
    def add_code_to_file(path, code):
        with open(path, 'a') as model_file:
            model_file.write(code)



