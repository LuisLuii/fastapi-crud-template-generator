import os
import sys

from ..misc.constant import GENERATION_FOLDER, ROUTE
from ..utils.create_file import create_folder, create_file_and_add_code_into_there


class CrudTemplateGenerator:
    def __init__(self):
        dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))
        self.current_directory = dirname
        self.template_root_directory = os.path.join(self.current_directory, GENERATION_FOLDER)
        self.module_path_map = {}


    def add_route(self, model_name, code):
        template_model_directory = os.path.join(self.template_root_directory, ROUTE)

        create_folder(template_model_directory)

        path = f'{template_model_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_model_directory}/{model_name}.py'
        create_file_and_add_code_into_there(path, code)
        # self.module_path_map[model_name] = {'model': path}


