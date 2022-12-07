from typing import \
    List, \
    TypeVar, Optional

import sqlalchemy
from pydantic import \
    BaseModel
from sqlalchemy.orm import decl_api

from .db_model import DbModel
from .generator.common_module_template_generator import CommonModuleTemplateGenerator
from .misc.type import SqlType
from .model.common_builder import CommonCodeGen

CRUDModelType = TypeVar("CRUDModelType", bound=BaseModel)
CompulsoryQueryModelType = TypeVar("CompulsoryQueryModelType", bound=BaseModel)
OnConflictModelType = TypeVar("OnConflictModelType", bound=BaseModel)


def crud_router_builder(
        *,
        db_model_list: List[DbModel],
        is_async: Optional[bool],
        database_url: Optional[str]
):
    """
        Generate project from sqlalchemy model

        :param database_url: a database URL. The URL is passed directly to SQLAlchemy's create_engine() method so
                                                please refer to SQLAlchemy's documentation for instructions on how to
                                                construct a proper URL.
        :param is_async: True for async; False for sync
        :param db_model_list: model list of dict for code generate

        Raises:
            RuntimeError: only support DeclarativeMeta Class
            SchemaException:
                multiple primary key / or composite not supported
                Only support one unique constraint/ Use unique constraint and composite unique constraint at same time
            ColumnTypeNotSupportedException:
                The type of db column is not supported

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
        db_model_info.gen(is_async=is_async, sql_type=sql_type)
        model_list += db_model_info.get_model_list()

    print("\nStart generate common module")
    common_code_builder = CommonCodeGen()
    # type generation
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
    common_db_session_code_builder.build_db_session(model_list=model_list, is_async=is_async, database_url=database_url,
                                                    is_in_memory_db=is_in_memory_db)
    common_db_session_code_builder.gen(common_module_template_generator.add_memory_sql_session)

    # app py
    print("\t\tStart generate app.py")
    common_app_code_builder = CommonCodeGen()
    common_app_code_builder.build_app(model_list=model_list)
    common_app_code_builder.gen(common_module_template_generator.add_app)

    print("\nProject generation completed successfully")
