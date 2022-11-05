import os

from .code_generator import CodeGenerator
from ..misc.constant import ROUTE
from ..utils.create_file import create_folder, create_file_and_add_code_into_there


class CrudTemplateGenerator(CodeGenerator):
    def __init__(self):
        super(CrudTemplateGenerator, self).__init__()

    def add_route(self, model_name, code):
        template_model_directory = os.path.join(self.template_root_directory, ROUTE)

        create_folder(template_model_directory)

        path = f'{template_model_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_model_directory}/{model_name}.py'
        create_file_and_add_code_into_there(path, code)
        # self.module_path_map[model_name] = {'model': path}


