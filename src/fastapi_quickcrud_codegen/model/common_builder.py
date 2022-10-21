from pathlib import Path
from typing import ClassVar

import jinja2

from ..utils.import_builder import ImportBuilder


class CommonCodeGen():
    def __init__(self):
        self.code = ""
        self.model_code = ""
        self.import_list = ""
        self.import_helper = ImportBuilder()

    # todo add tpye for template_generator
    def gen(self, template_generator_method):
        template_generator_method(self.code)

    def build_type(self):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/typing.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'typing.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render()
        self.code += code

    def build_utils(self):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/utils.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'utils.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        self.import_helper.add(import_=set(["QueryOperatorNotFound", "UnknownColumn"]),
                               from_="fastapi_quick_crud_template.common.http_exception")
        self.import_helper.add(
            import_=set(["ExtraFieldType", "ExtraFieldTypePrefix", "process_type_map", "process_map"]),
            from_="fastapi_quick_crud_template.common.typing")

        code = template.render({"import": self.import_helper.to_code()})

        self.code += code

    def build_http_exception(self):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/http_exception.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'http_exception.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render()
        self.code += code

    def build_db(self):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/db.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'db.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render()
        self.code += code

    def build_db_session(self, model_list: dict, is_async: bool, database_url: str, is_in_memory_db: bool):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/memory_sql_session.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'memory_sql_session.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({"model_list": model_list, "is_async": is_async, "database_url": database_url,
                                "is_in_memory_db": is_in_memory_db})
        self.code += code

    def build_app(self, model_list):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'common/app.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'app.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({"model_list": model_list})
        self.code += code
