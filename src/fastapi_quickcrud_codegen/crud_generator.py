from typing import \
    List, \
    TypeVar, Optional

import sqlalchemy
from pydantic import \
    BaseModel

from .utils.sqlalchemy_to_pydantic import sqlalchemy_to_pydantic
from .generator.common_module_template_generator import CommonModuleTemplateGenerator
from .generator.crud_template_generator import CrudTemplateGenerator
from .misc.crud_model import CRUDModel
from .misc.get_table_name import get_table_name
from .misc.type import CrudMethods, SqlType
from .utils.is_table import is_table
from .model.common_builder import CommonCodeGen
from .model.crud_builder import CrudCodeGen

CRUDModelType = TypeVar("CRUDModelType", bound=BaseModel)
CompulsoryQueryModelType = TypeVar("CompulsoryQueryModelType", bound=BaseModel)
OnConflictModelType = TypeVar("OnConflictModelType", bound=BaseModel)


def crud_router_builder(
        *,
        db_model_list: List[dict],
        is_async: Optional[bool],
        database_url: Optional[str],
) :
    """
        Generate project from sqlalchemy model

        :param database_url: a database URL. The URL is passed directly to SQLAlchemy's create_engine() method so
                                                please refer to SQLAlchemy's documentation for instructions on how to
                                                construct a proper URL.
        :param is_async: True for async; False for sync
        :param db_model_list: model list of dict for code generate

        Raises:
            ValueError: TODO
        Examples:
            >>> crud_router_builder(db_model_list=[
                        {
                            "db_model": SampleTable,
                            "prefix": "/my_first_api",
                            "tags": ["sample api"],
                            "exclude_columns": ['bytea_value'],
                            "crud_methods": [CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE,
                                             CrudMethods.UPDATE_MANY, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE],
                        },
                        {
                            "db_model": SampleTableTwo,
                            "prefix": "/my_second_api",
                            "tags": ["sample api"],
                            "exclude_columns": ['bytea_value'],
                            "crud_methods": [CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE,
                                             CrudMethods.UPDATE_MANY, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE],
                        }
                    ],
                    is_async=False,
                    database_url="sqlite://"
                )

    """
    print("Start Fastapi's CRUD project generation")
    engine = sqlalchemy.create_engine(database_url)
    is_in_memory_db = False
    if engine and engine.url and not engine.url.host and not engine.url.port:
        print("\nThis is in-memory db")
        is_in_memory_db = True

    sql_type = SqlType(engine.dialect.name)
    print(f"\ndatabase type: {sql_type}")

    # : Optional[SqlType]
    model_list = []

    common_module_template_generator = CommonModuleTemplateGenerator()

    print("\nStart generate model and router module...")
    for db_model_info in db_model_list:

        db_model = db_model_info["db_model"]
        prefix = db_model_info["prefix"]
        tags = db_model_info["tags"]
        exclude_columns = db_model_info.get("exclude_columns", [])
        crud_methods = db_model_info.get("crud_methods", CrudMethods.get_full_crud_method())
        print(f"\n\t\tGenerating db_model:{db_model} prefix:{prefix} tags:{tags}")
        this_modeL_is_table = is_table(db_model)
        if this_modeL_is_table:
            raise RuntimeError("only support declarative from Sqlalchemy, you can try to give the table a fake pk"
                               " to work around")
        table_name = db_model.__name__

        model_name = get_table_name(db_model)

        model_list.append({"model_name": model_name, "file_name": table_name})

        # code gen
        crud_code_generator = CrudCodeGen(tags=tags, prefix=prefix)
        # create a file
        crud_template_generator = CrudTemplateGenerator()

        constraints = db_model.__table__.constraints

        print(f"\t\tfollowing api method will be generated:{crud_methods} ")

        # model generation
        print(f"\t\tGenerating model for API")
        crud_models_builder: CRUDModel = sqlalchemy_to_pydantic
        crud_models: CRUDModel = crud_models_builder(db_model=db_model,
                                                     constraints=constraints,
                                                     crud_methods=crud_methods,
                                                     exclude_columns=exclude_columns,
                                                     sql_type=sql_type)
        print(f"\t\tGenerating model success")
        methods_dependencies = crud_models.get_available_request_method()
        primary_name = crud_models.PRIMARY_KEY_NAME
        if primary_name:
            path = '/{' + primary_name + '}'
        else:
            path = ""

        # router generation
        def find_one_api():
            print(f"\t\tGenerating find one API")
            crud_code_generator.build_find_one_route(is_async=is_async, path=path, file_name=model_name, model_name=table_name)
            print(f"\t\tfind one API generate successfully")

        def find_many_api():
            print(f"\t\tGenerating find many API")
            crud_code_generator.build_find_many_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tfind many API generate successfully")

        def create_one_api():
            print(f"\t\tGenerating insert one API")
            crud_code_generator.build_insert_one_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tinsert one API generate successfully")

        def create_many_api():
            print(f"\t\tGenerating insert many API")
            crud_code_generator.build_insert_many_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tinsert many API generate successfully")

        def update_one_api():
            print(f"\t\tGenerating update one API")
            crud_code_generator.build_update_one_route(is_async=is_async, path=path, file_name=model_name, model_name=table_name)
            print(f"\t\tupdate one API generate successfully")

        def update_many_api():
            print(f"\t\tGenerating update many API")
            crud_code_generator.build_update_many_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tupdate many API generate successfully")

        def patch_one_api():
            print(f"\t\tGenerating patch one API")
            crud_code_generator.build_patch_one_route(is_async=is_async, path=path, file_name=model_name, model_name=table_name)
            print(f"\t\tpatch one API generate successfully")

        def patch_many_api():
            print(f"\t\tGenerating patch many API")
            crud_code_generator.build_patch_many_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tpatch many API generate successfully")

        def delete_one_api():
            print(f"\t\tGenerating delete one API")
            crud_code_generator.build_delete_one_route(is_async=is_async, path=path, file_name=model_name, model_name=table_name)
            print(f"\t\tdelete one API generate successfully")

        def delete_many_api():
            print(f"\t\tGenerating delete many API")
            crud_code_generator.build_delete_many_route(is_async=is_async, path="", file_name=model_name, model_name=table_name)
            print(f"\t\tdelete many API generate successfully")

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

    print("\nStart generate common module")
    # type generation
    print("\t\tStart generate type module")
    common_code_builder = CommonCodeGen()
    common_code_builder.build_type()
    common_code_builder.gen(common_module_template_generator.add_type)

    # module generation
    print("\t\tStart generate utils module")
    common_utils_code_builder = CommonCodeGen()
    common_utils_code_builder.build_utils()
    common_utils_code_builder.gen(common_module_template_generator.add_utils)

    # http_exception generation
    print("\t\tStart generate http exception module")
    common_http_exception_code_builder = CommonCodeGen()
    common_http_exception_code_builder.build_http_exception()
    common_http_exception_code_builder.gen(common_module_template_generator.add_http_exception)

    # db generation
    print("\t\tStart generate db module")
    common_db_code_builder = CommonCodeGen()
    common_db_code_builder.build_db()
    common_db_code_builder.gen(common_module_template_generator.add_db)

    # sql session
    print("\t\tStart generate session module")
    common_db_session_code_builder = CommonCodeGen()
    common_db_session_code_builder.build_db_session(model_list=model_list, is_async=is_async, database_url=database_url, is_in_memory_db = is_in_memory_db)
    common_db_session_code_builder.gen(common_module_template_generator.add_memory_sql_session)

    # app py
    print("\t\tStart generate app.py")
    common_app_code_builder = CommonCodeGen()
    common_app_code_builder.build_app(model_list=model_list)
    common_app_code_builder.gen(common_module_template_generator.add_app)


    print("\nProject generation completed successfully")