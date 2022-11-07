from pathlib import Path
from typing import ClassVar

import jinja2

from ..generator.crud_template_generator import CrudTemplateGenerator
from ..utils.import_builder import ImportBuilder


class CrudCodeGen():
    def __init__(self, tags, prefix):
        self.code = "\n" + "api = APIRouter(tags=" + str(tags) + ',' + "prefix=" + '"' + prefix + '")' + "\n\n\n"
        self.import_helper = ImportBuilder()
        self.import_helper.add(import_="HTTPStatus", from_="http")
        self.import_helper.add(import_=set(["List", "Union"]), from_="typing")
        self.import_helper.add(import_=set(["and_", "select"]), from_="sqlalchemy")
        self.import_helper.add(import_=set(["Depends", "Response", "APIRouter"]), from_="fastapi")
        self.import_helper.add(import_=set(["BinaryExpression"]), from_="sqlalchemy.sql.elements")
        self.import_helper.add(import_=set(["find_query_builder"]), from_="common.utils")
        self.import_helper.add(import_=set(["db_session"]), from_="common.sql_session")

    def gen(self, *, template_generator: CrudTemplateGenerator, file_name: str) -> None:
        template_generator.add_route(file_name, self.import_helper.to_code() + self.code)

    def build_find_one_route(self, *, is_async: bool, path: str, file_name: str, model_name: str) -> None:
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/find_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'find_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_=set([
            f"{model_name}FindOneResponseModel",
            f"{model_name}FindOneRequestBodyModel",
            f"{model_name}PrimaryKeyModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_find_many_route(self, *, is_async: bool, path: str, file_name: str, model_name: str) -> None:
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/find_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'find_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})

        self.import_helper.add(import_=set([
            f"{model_name}FindManyResponseModel",
            f"{model_name}FindManyRequestBodyModel",
            f"{model_name}FindManyItemListResponseModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_=set(["UnknownOrderType", "UnknownColumn"]),
                               from_="common.http_exception")
        self.import_helper.add(import_=set(["Ordering"]), from_="common.typing")

        self.code += code + "\n\n"

    def build_insert_one_route(self, *, is_async: bool, path: str, file_name: str, model_name: str) -> None:
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/insert_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'insert_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_="clean_input_fields", from_="common.utils")
        self.import_helper.add(import_=set(["UnknownOrderType", "UnknownColumn"]),
                               from_="common.http_exception")
        self.import_helper.add(import_=set(["Ordering"]), from_="common.typing")

        self.import_helper.add(import_=set([
            f"{model_name}CreateOneResponseModel",
            f"{model_name}CreateOneRequestBodyModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_insert_many_route(self, *, is_async: bool, path: str, file_name: str, model_name: str) -> None:
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/insert_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'insert_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_="clean_input_fields", from_="common.utils")
        self.import_helper.add(import_=set(["UnknownOrderType", "UnknownColumn"]),
                               from_="common.http_exception")
        self.import_helper.add(import_=set(["Ordering"]), from_="common.typing")

        self.import_helper.add(import_=set([
            f"{model_name}CreateManyItemListResponseModel",
            f"{model_name}CreateManyItemListRequestModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_update_one_route(self, *, is_async: bool, path: str, file_name: str, model_name: str) -> None:
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/update_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'update_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_="clean_input_fields", from_="common.utils")
        self.import_helper.add(import_=set(["UnknownOrderType", "UnknownColumn"]),
                               from_="common.http_exception")
        self.import_helper.add(import_=set(["Ordering"]), from_="common.typing")

        self.import_helper.add(import_=set([
            f"{model_name}UpdateOneRequestBodyModel",
            f"{model_name}UpdateOneRequestQueryModel",
            f"{model_name}UpdateOneResponseModel",
            f"{model_name}PrimaryKeyModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_update_many_route(self, *, is_async: bool, path: str, file_name: str, model_name: str):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/update_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'update_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_="clean_input_fields", from_="common.utils")
        self.import_helper.add(import_=set(["UnknownOrderType", "UnknownColumn"]),
                               from_="common.http_exception")
        self.import_helper.add(import_=set(["Ordering"]), from_="common.typing")

        self.import_helper.add(import_=set([
            f"{model_name}UpdateManyRequestQueryModel",
            f"{model_name}UpdateManyRequestBodyModel",
            f"{model_name}UpdateManyItemListResponseModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_patch_one_route(self, *, is_async: bool, path: str, file_name: str, model_name: str):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/patch_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'patch_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_=set([
            f"{model_name}PatchOneRequestQueryModel",
            f"{model_name}PatchOneRequestBodyModel",
            f"{model_name}PatchOneResponseModel",
            f"{model_name}PrimaryKeyModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_patch_many_route(self, *, is_async: bool, path: str, file_name: str, model_name: str):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/patch_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'patch_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="IntegrityError", from_="sqlalchemy.exc")
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_=set([
            f"{model_name}PatchManyRequestQueryModel",
            f"{model_name}PatchManyRequestBodyModel",
            f"{model_name}PatchManyItemListResponseModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_delete_one_route(self, *, is_async: bool, path: str, file_name: str, model_name: str):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/delete_one.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'delete_one.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_=set([
            f"{model_name}DeleteOneRequestQueryModel",
            f"{model_name}DeleteOneResponseModel",
            f"{model_name}PrimaryKeyModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"

    def build_delete_many_route(self, *, is_async: bool, path: str, file_name: str, model_name: str):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'route/delete_many.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)

        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'delete_many.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render(
            {"model_name": model_name, "path": path, "is_async": is_async})
        self.import_helper.add(import_="parse_obj_as", from_="pydantic")
        self.import_helper.add(import_=set([
            f"{model_name}DeleteManyRequestQueryModel",
            f"{model_name}DeleteManyItemListResponseModel",
            f"{model_name}"]
        ), from_=f"model.{file_name}")
        self.code += code + "\n\n"
