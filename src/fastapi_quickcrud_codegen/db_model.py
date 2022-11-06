from typing import List

from sqlalchemy.orm import decl_api

from .generator.crud_template_generator import CrudTemplateGenerator
from .misc.crud_model import CRUDModel
from .misc.get_table_name import get_table_name
from .misc.type import CrudMethods, SqlType
from .model.crud_builder import CrudCodeGen
from .utils.is_table import is_table
from .utils.sqlalchemy_to_pydantic import sqlalchemy_to_pydantic


class DbModel:
    def __init__(self, db_model: decl_api.DeclarativeMeta,
                 prefix: str,
                 tags: List[str],
                 exclude_columns: List[str] = None,
                 crud_methods: List[CrudMethods] = None):

        self.db_model = db_model
        self.prefix = prefix
        self.tags = tags

        if exclude_columns is None:
            exclude_columns = []
        self.exclude_columns = exclude_columns

        if crud_methods is None:
            crud_methods = CrudMethods.get_full_crud_method()
        self.crud_methods = crud_methods
        self.model_list = []

    def get_model_list(self) -> List[dict]:
        return self.model_list

    def gen(self, is_async: bool, sql_type: SqlType) -> None:

        print(f"\n\t\tGenerating db_model:{self.db_model} prefix:{self.prefix} tags:{self.tags}")
        this_modeL_is_table = is_table(self.db_model)
        if this_modeL_is_table:
            raise RuntimeError("only support declarative from Sqlalchemy, you can try to give the table a fake pk"
                               " to work around")
        table_name = self.db_model.__name__

        model_name = get_table_name(self.db_model)

        self.model_list.append({"model_name": model_name, "file_name": table_name})

        # code gen
        crud_code_generator = CrudCodeGen(tags=self.tags, prefix=self.prefix)
        # create a file
        crud_template_generator = CrudTemplateGenerator()

        constraints = self.db_model.__table__.constraints

        print(f"\t\tfollowing api method will be generated:{self.crud_methods} ")

        # model generation
        print("\t\tGenerating model for API")
        crud_models_builder: CRUDModel = sqlalchemy_to_pydantic
        crud_models: CRUDModel = crud_models_builder(db_model=self.db_model,
                                                     constraints=constraints,
                                                     crud_methods=self.crud_methods,
                                                     exclude_columns=self.exclude_columns,
                                                     sql_type=sql_type)
        print("\t\tGenerating model success")
        methods_dependencies = crud_models.get_available_request_method()
        primary_name = crud_models.PRIMARY_KEY_NAME
        path = '/{' + primary_name + '}'

        # router generation
        def find_one_api():
            print("\t\tGenerating find one API")
            crud_code_generator.build_find_one_route(is_async=is_async, path=path, file_name=model_name,
                                                     model_name=table_name)
            print("\t\tfind one API generate successfully")

        def find_many_api():
            print("\t\tGenerating find many API")
            crud_code_generator.build_find_many_route(is_async=is_async, path="", file_name=model_name,
                                                      model_name=table_name)
            print("\t\tfind many API generate successfully")

        def create_one_api():
            print("\t\tGenerating insert one API")
            crud_code_generator.build_insert_one_route(is_async=is_async, path="", file_name=model_name,
                                                       model_name=table_name)
            print("\t\tinsert one API generate successfully")

        def create_many_api():
            print("\t\tGenerating insert many API")
            crud_code_generator.build_insert_many_route(is_async=is_async, path="", file_name=model_name,
                                                        model_name=table_name)
            print("\t\tinsert many API generate successfully")

        def update_one_api():
            print("\t\tGenerating update one API")
            crud_code_generator.build_update_one_route(is_async=is_async, path=path, file_name=model_name,
                                                       model_name=table_name)
            print("\t\tupdate one API generate successfully")

        def update_many_api():
            print("\t\tGenerating update many API")
            crud_code_generator.build_update_many_route(is_async=is_async, path="", file_name=model_name,
                                                        model_name=table_name)
            print("\t\tupdate many API generate successfully")

        def patch_one_api():
            print("\t\tGenerating patch one API")
            crud_code_generator.build_patch_one_route(is_async=is_async, path=path, file_name=model_name,
                                                      model_name=table_name)
            print("\t\tpatch one API generate successfully")

        def patch_many_api():
            print("\t\tGenerating patch many API")
            crud_code_generator.build_patch_many_route(is_async=is_async, path="", file_name=model_name,
                                                       model_name=table_name)
            print("\t\tpatch many API generate successfully")

        def delete_one_api():
            print("\t\tGenerating delete one API")
            crud_code_generator.build_delete_one_route(is_async=is_async, path=path, file_name=model_name,
                                                       model_name=table_name)
            print("\t\tdelete one API generate successfully")

        def delete_many_api():
            print("\t\tGenerating delete many API")
            crud_code_generator.build_delete_many_route(is_async=is_async, path="", file_name=model_name,
                                                        model_name=table_name)
            print("\t\tdelete many API generate successfully")

        api_register = {
            CrudMethods.FIND_ONE.value: find_one_api,
            CrudMethods.FIND_MANY.value: find_many_api,
            CrudMethods.CREATE_ONE.value: create_one_api,
            CrudMethods.CREATE_MANY.value: create_many_api,
            CrudMethods.UPDATE_ONE.value: update_one_api,
            CrudMethods.UPDATE_MANY.value: update_many_api,
            CrudMethods.PATCH_ONE.value: patch_one_api,
            CrudMethods.PATCH_MANY.value: patch_many_api,
            CrudMethods.DELETE_ONE.value: delete_one_api,
            CrudMethods.DELETE_MANY.value: delete_many_api,
        }
        for request_method in methods_dependencies:
            value_of_dict_crud_model = crud_models.get_model_by_request_method(request_method)
            crud_model_of_this_request_methods = value_of_dict_crud_model.keys()
            for crud_model_of_this_request_method in crud_model_of_this_request_methods:
                api_register[crud_model_of_this_request_method.value]()
        crud_code_generator.gen(template_generator=crud_template_generator, file_name=model_name)
