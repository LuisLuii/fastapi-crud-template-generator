import os
import sys

from ..misc.constant import GENERATION_FOLDER, ROUTE, COMMON


class CommonModuleTemplateGenerator:
    def __init__(self):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        self.current_directory = dirname
        self.template_root_directory = os.path.join(self.current_directory, GENERATION_FOLDER)
        self.module_path_map = {}


    def __create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def add_type(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/typing.py'
        self.create_file_and_add_code_into_there(path, code)

    def add_utils(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/utils.py'
        self.create_file_and_add_code_into_there(path, code)

    def add_http_exception(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/http_exception.py'
        self.create_file_and_add_code_into_there(path, code)

    def add_db(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/db.py'
        self.create_file_and_add_code_into_there(path, code)

    def add_memory_sql_session(self, code):

        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/sql_session.py'
        self.create_file_and_add_code_into_there(path, code)


    def add_app(self, code):

        template_module_directory = os.path.join(self.template_root_directory)
        self.__create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        self.create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/app.py'
        self.create_file_and_add_code_into_there(path, code)

    @staticmethod
    def create_file_and_add_code_into_there(path, code):
        with open(path, 'a') as model_file:
            model_file.write(code)

