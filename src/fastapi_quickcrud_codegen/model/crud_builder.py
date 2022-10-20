from pathlib import Path
from typing import ClassVar

import jinja2

from fastapi_quickcrud_codegen.generator.crud_template_generator import CrudTemplateGenerator


class CrudCodeGen():
    def __init__(self, tags, prefix):
        self.code = "\n\n\n" + "api = APIRouter(tags=" + str(tags) + ',' + "prefix=" + '"' + prefix + '")' + "\n\n"
        # self.index = SymbolIndex()
        # lib_path: list[str] = [i for i in sys.path if "FastAPIQuickCRUD" not in i]
        # self.index.build_index(lib_path)
        self.import_list = f"""
import copy
from http import HTTPStatus
from typing import List, Union
from os import path

from sqlalchemy import and_, select
from fastapi import Depends, Response, APIRouter
from sqlalchemy.sql.elements import BinaryExpression

from fastapi_quick_crud_template.common.utils import find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session
        """

    def gen(self, *, template_generator: CrudTemplateGenerator, file_name: str):
        template_generator.add_route(file_name, self.import_list + "\n\n" + self.code)

    def build_find_one_route(self, *, is_async: bool, path: str, file_name, model_name):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'route/find_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'find_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})

        self.import_list += "\n" + f"""
from fastapi_quick_crud_template.model.{file_name} import ( {model_name}FindOneResponseModel, 
                                                            {model_name}FindOneRequestBodyModel, 
                                                            {model_name}PrimaryKeyModel,
                                                            {model_name})
        """
        self.code += "\n\n\n" + code

    def build_find_many_route(self, *, is_async: bool, path: str, file_name, model_name):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'route/find_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'find_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_list += "\n" + f"""
from pydantic import parse_obj_as

from fastapi_quick_crud_template.common.http_exception import UnknownOrderType, UnknownColumn
from fastapi_quickcrud_codegen.misc.type import Ordering
from fastapi_quick_crud_template.model.{file_name} import ( {model_name}FindManyResponseModel, 
                                                            {model_name}FindManyRequestBodyModel, 
                                                            {model_name}FindManyResponseRootModel, 
                                                            {model_name})
            """
        self.code += "\n\n\n" + code

    def build_insert_one_route(self, *, is_async: bool, path: str, file_name, model_name):
        TEMPLATE_FILE_PATH: ClassVar[str] = f'route/insert_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = f'insert_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_list += "\n" + f"""
from sqlalchemy.exc import IntegrityError

from pydantic import parse_obj_as

from fastapi_quickcrud_codegen.misc.utils import clean_input_fields
from fastapi_quick_crud_template.common.http_exception import UnknownOrderType, UnknownColumn
from fastapi_quickcrud_codegen.misc.type import Ordering
from fastapi_quick_crud_template.model.{file_name} import ( {model_name}CreateOneResponseModel, 
                                                            {model_name}CreateOneRequestBodyModel, 
                                                            {model_name})
        """
        self.code += "\n\n\n" + code
