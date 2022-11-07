import inspect
from pathlib import Path
from typing import ClassVar, List, Tuple

import jinja2
from sqlalchemy.orm import decl_api

from ..generator.model_template_generator import ModelTemplateGenerator
from ..utils.import_builder import ImportBuilder


class ModelCodeGen():
    def __init__(self, file_name: str, db_type: str):
        self.file_name = file_name
        self.code = ""
        self.model_code = ""
        self.constant = ""
        self.import_helper = ImportBuilder()
        self.import_helper.add(import_=set(["dataclass", "field"]), from_="dataclasses")
        self.import_helper.add(import_=set(['datetime', 'timedelta', 'date', 'time']), from_="datetime")
        self.import_helper.add(import_=set(['Decimal']), from_="decimal")
        self.import_helper.add(import_=set(['Optional', 'List', 'Union', 'NewType']), from_="typing")
        self.import_helper.add(import_=set(['pydantic']))
        self.import_helper.add(import_=set(['BaseModel']), from_="pydantic")
        self.import_helper.add(import_=set(['Query', 'Body']), from_="fastapi")
        self.import_helper.add(import_=set(['*']), from_="sqlalchemy")
        self.import_helper.add(import_=set(['*']), from_=f"sqlalchemy.dialects.{db_type}")
        self.import_helper.add(import_=set(['value_of_list_to_str', 'ExcludeUnsetBaseModel', 'filter_none']),
                               from_="common.utils")
        self.import_helper.add(import_=set(['Base']), from_="common.db")
        self.import_helper.add(import_=set(['ItemComparisonOperators', 'PGSQLMatchingPatternInString',
                                            'ExtraFieldTypePrefix', 'RangeToComparisonOperators',
                                            'MatchingPatternInStringBase', 'RangeFromComparisonOperators']),
                               from_="common.typing")
        self.import_helper.add(import_="uuid")
        self.model_template_gen = ModelTemplateGenerator()

    def gen(self):
        return self.model_template_gen.add_model(self.file_name,
                                                 self.import_helper.to_code() + self.constant + "\n" + self.model_code + "\n\n" + self.code)

    def gen_model(self, model: decl_api.DeclarativeMeta):
        self.model_code = inspect.getsource(model)

    def build_base_model(self, *, class_name: str, fields: List[Tuple], description: str = None, orm_mode: bool = True,
                         value_of_list_to_str_columns: List[str] = None, filter_none: bool = None):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "BaseModel.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"class_name": class_name, "fields": fields, "description": description, "orm_mode": orm_mode,
             "value_of_list_to_str_columns": value_of_list_to_str_columns, "filter_none": filter_none})
        self.code += code + "\n\n\n"

    def build_base_model_paginate(self, *, class_name: str, field: List[Tuple], description: str = None,
                                  base_model: str = "BaseModel",
                                  value_of_list_to_str_columns: List[str] = None, filter_none: bool = None):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/base_model_paginate.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "base_model_paginate.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"class_name": class_name, "field": field, "description": description, "base_model": base_model,
             "value_of_list_to_str_columns": value_of_list_to_str_columns, "filter_none": filter_none})
        self.code += code + "\n\n\n"

    def build_base_model_root(self, *, class_name: str, field: List[Tuple], description: str = None,
                              base_model: str = "BaseModel",
                              value_of_list_to_str_columns: List[str] = None, filter_none: bool = None):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "BaseModel_root.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"class_name": class_name, "field": field, "description": description, "base_model": base_model,
             "value_of_list_to_str_columns": value_of_list_to_str_columns, "filter_none": filter_none})
        self.code += code + "\n\n\n"

    def build_dataclass(self, *, class_name: str, fields: List[str], description: str = None,
                        value_of_list_to_str_columns: List[str] = None,
                        filter_none: bool = None):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "dataclass.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({"class_name": class_name, "fields": fields, "description": description,
                                "value_of_list_to_str_columns": value_of_list_to_str_columns,
                                "filter_none": filter_none})
        self.code += code + "\n\n\n"

    def build_constant(self, *, constants: List[Tuple]):
        TEMPLATE_FILE_PATH: ClassVar[str] = ''
        template_file_path = Path(TEMPLATE_FILE_PATH)
        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "Constant.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({"constants": constants})
        self.constant += code
