import os

from .code_generator import CodeGenerator
from ..misc.constant import COMMON
from ..utils.create_file import create_folder, create_file_and_add_code_into_there


class CommonModuleTemplateGenerator(CodeGenerator):
    def __init__(self):
        super(CommonModuleTemplateGenerator, self).__init__()

    def add_type(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/typing.py'
        create_file_and_add_code_into_there(path, code)

    def add_utils(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/utils.py'
        create_file_and_add_code_into_there(path, code)

    def add_http_exception(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/http_exception.py'
        create_file_and_add_code_into_there(path, code)

    def add_db(self, code):
        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/db.py'
        create_file_and_add_code_into_there(path, code)

    def add_memory_sql_session(self, code):

        template_module_directory = os.path.join(self.template_root_directory, COMMON)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/sql_session.py'
        create_file_and_add_code_into_there(path, code)


    def add_app(self, code):

        template_module_directory = os.path.join(self.template_root_directory)
        create_folder(template_module_directory)

        path = f'{template_module_directory}/__init__.py'
        create_file_and_add_code_into_there(path, "")

        path = f'{template_module_directory}/app.py'
        create_file_and_add_code_into_there(path, code)



