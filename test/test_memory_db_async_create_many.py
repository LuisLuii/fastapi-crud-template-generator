import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen.db_model import DbModel
from src.fastapi_quickcrud_codegen.misc.type import CrudMethods
from src.fastapi_quickcrud_codegen import crud_router_builder
from test.misc.common import *

Base = declarative_base()
metadata = Base.metadata


class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself_memory'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10, collation='NOCASE'))
    date_value = Column(Date)
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, default=10.10)
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, default=99)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)


class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_memory_two'
    __table_args__ = (
        UniqueConstraint('primary_key'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)


class Testing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        is_async = True
        if is_async:
            database_url = "sqlite+aiosqlite://"
        else:
            database_url = "sqlite://"

        model_list = [DbModel(db_model=SampleTable, prefix="/my_first_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.CREATE_MANY]),
                      DbModel(db_model=SampleTableTwo, prefix="/my_second_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.CREATE_MANY]), ]

        crud_router_builder(
            db_model_list=model_list,
            is_async=is_async,
            database_url=database_url
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(template_root_directory)

    def test_hardcode(self):
        hard_code_validate()

    def test_project_generation(self):
        # root
        #   app
        app_expected = \
            """import uvicorn
from fastapi import FastAPI

from route.test_build_myself_memory import api as test_build_myself_memory_router
from route.test_build_myself_memory_two import api as test_build_myself_memory_two_router
app = FastAPI()

[app.include_router(api_route) for api_route in [
test_build_myself_memory_router,test_build_myself_memory_two_router,
]]

uvicorn.run(app, host="0.0.0.0", port=8000)"""
        validate_app(expected=app_expected)

        # common
        #   sql_session
        common_sql_session_expected = '''import asyncio
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from model.test_build_myself_memory import SampleTable
from model.test_build_myself_memory_two import SampleTableTwo

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite://"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                             future=True,
                             echo=True,
                             pool_pre_ping=True,
                             pool_recycle=7200,
                             connect_args={"check_same_thread": False}, 
                             poolclass=StaticPool)
session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine,
                       class_=AsyncSession)


async def db_session():
    async with session() as _session:
        yield _session
        await _session.commit()


async def create_table(engine, model):
    async with engine.begin() as conn:
        await conn.run_sync(model._sa_registry.metadata.create_all)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_table(engine, SampleTable))
loop.run_until_complete(create_table(engine, SampleTableTwo))
'''
        validate_common_sql_session(common_sql_session_expected)

        # model
        model_test_build_myself_memory_two_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from common.db import Base
from common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators

PRIMARY_KEY_NAME = "primary_key"
UNIQUE_LIST = "primary_key"
    

class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_memory_two'
    __table_args__ = (
        UniqueConstraint('primary_key'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)


@dataclass
class SampleTableTwoPrimaryKeyModel:
    primary_key: int = Query(None, description=None)


@dataclass
class SampleTableTwoCreateManyItemRequestModel:
    primary_key: int = field(default=Body(None, description=None))
    bool_value: bool = field(default=Body(False, description=None))


@dataclass
class SampleTableTwoCreateManyItemListRequestModel:
    insert: List[SampleTableTwoCreateManyItemRequestModel] = Body(...)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoCreateManyItemResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None, description=None)
    bool_value: bool = Body(False, description=None)

    class Config:
        orm_mode = True


class SampleTableTwoCreateManyItemListResponseModel(BaseModel):
    __root__: List[SampleTableTwoCreateManyItemResponseModel]

    class Config:
        orm_mode = True


'''
        validate_model("test_build_myself_memory_two", model_test_build_myself_memory_two_expected)

        model_test_build_myself_memory_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from common.db import Base
from common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators

PRIMARY_KEY_NAME = "primary_key"
UNIQUE_LIST = "primary_key", "int4_value", "float4_value"
    

class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself_memory'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10, collation='NOCASE'))
    date_value = Column(Date)
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, default=10.10)
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, default=99)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)


@dataclass
class SampleTablePrimaryKeyModel:
    primary_key: int = Query(None, description=None)


@dataclass
class SampleTableCreateManyItemRequestModel:
    primary_key: int = field(default=Body(None, description=None))
    bool_value: bool = field(default=Body(False, description=None))
    char_value: str = field(default=Body(None, description=None))
    date_value: date = field(default=Body(None, description=None))
    float4_value: float = field(default=Body(..., description=None))
    float8_value: float = field(default=Body(10.1, description=None))
    int2_value: int = field(default=Body(..., description=None))
    int4_value: int = field(default=Body(..., description=None))
    int8_value: int = field(default=Body(99, description=None))
    text_value: str = field(default=Body(None, description=None))
    time_value: time = field(default=Body(None, description=None))
    timestamp_value: datetime = field(default=Body(None, description=None))
    timestamptz_value: datetime = field(default=Body(None, description=None))
    timetz_value: time = field(default=Body(None, description=None))
    varchar_value: str = field(default=Body(None, description=None))


@dataclass
class SampleTableCreateManyItemListRequestModel:
    insert: List[SampleTableCreateManyItemRequestModel] = Body(...)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableCreateManyItemResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None, description=None)
    bool_value: bool = Body(False, description=None)
    char_value: str = Body(None, description=None)
    date_value: date = Body(None, description=None)
    float4_value: float = Body(..., description=None)
    float8_value: float = Body(10.1, description=None)
    int2_value: int = Body(..., description=None)
    int4_value: int = Body(..., description=None)
    int8_value: int = Body(99, description=None)
    text_value: str = Body(None, description=None)
    time_value: time = Body(None, description=None)
    timestamp_value: datetime = Body(None, description=None)
    timestamptz_value: datetime = Body(None, description=None)
    timetz_value: time = Body(None, description=None)
    varchar_value: str = Body(None, description=None)

    class Config:
        orm_mode = True


class SampleTableCreateManyItemListResponseModel(BaseModel):
    __root__: List[SampleTableCreateManyItemResponseModel]

    class Config:
        orm_mode = True


'''
        validate_model("test_build_myself_memory", model_test_build_myself_memory_expected)

        # route
        route_test_build_myself_memory_two_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from common.utils import clean_input_fields, find_query_builder
from common.sql_session import db_session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as
from common.http_exception import UnknownColumn, UnknownOrderType
from common.typing import Ordering
from model.test_build_myself_memory_two import SampleTableTwo, SampleTableTwoCreateManyItemListRequestModel, SampleTableTwoCreateManyItemListResponseModel

api = APIRouter(tags=['sample api'],prefix="/my_second_api")


@api.post("", status_code=201, response_model=SampleTableTwoCreateManyItemListResponseModel)
async def insert_many(
                response: Response,
                request_body=Depends(SampleTableTwoCreateManyItemListRequestModel),
                session=Depends(db_session)):
    insert_arg_list: list = request_body.__dict__.pop('insert', None)
    insert_arg_dict = []
    for i in insert_arg_list:
        insert_arg_dict.append(i.__dict__)
    if not isinstance(insert_arg_dict, list):
        insert_arg_dict = [insert_arg_dict]
    model = SampleTableTwo
    insert_arg_dict: list[dict] = [clean_input_fields(model=model, param=insert_arg)
                                   for insert_arg in insert_arg_dict]
    new_inserted_data = []
    if isinstance(insert_arg_dict, list):
        for i in insert_arg_dict:
            new_inserted_data.append(model(**i))
    session.add_all(new_inserted_data)
    try:
        await session.flush()
    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result

    result = parse_obj_as(SampleTableTwoCreateManyItemListResponseModel, new_inserted_data)
    response.headers["x-total-count"] = str(len(new_inserted_data))
    return result

'''
        validate_route("test_build_myself_memory_two", route_test_build_myself_memory_two_expected)
        model_test_build_myself_memory_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from common.utils import clean_input_fields, find_query_builder
from common.sql_session import db_session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as
from common.http_exception import UnknownColumn, UnknownOrderType
from common.typing import Ordering
from model.test_build_myself_memory import SampleTable, SampleTableCreateManyItemListRequestModel, SampleTableCreateManyItemListResponseModel

api = APIRouter(tags=['sample api'],prefix="/my_first_api")


@api.post("", status_code=201, response_model=SampleTableCreateManyItemListResponseModel)
async def insert_many(
                response: Response,
                request_body=Depends(SampleTableCreateManyItemListRequestModel),
                session=Depends(db_session)):
    insert_arg_list: list = request_body.__dict__.pop('insert', None)
    insert_arg_dict = []
    for i in insert_arg_list:
        insert_arg_dict.append(i.__dict__)
    if not isinstance(insert_arg_dict, list):
        insert_arg_dict = [insert_arg_dict]
    model = SampleTable
    insert_arg_dict: list[dict] = [clean_input_fields(model=model, param=insert_arg)
                                   for insert_arg in insert_arg_dict]
    new_inserted_data = []
    if isinstance(insert_arg_dict, list):
        for i in insert_arg_dict:
            new_inserted_data.append(model(**i))
    session.add_all(new_inserted_data)
    try:
        await session.flush()
    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result

    result = parse_obj_as(SampleTableCreateManyItemListResponseModel, new_inserted_data)
    response.headers["x-total-count"] = str(len(new_inserted_data))
    return result

'''
        validate_route("test_build_myself_memory", model_test_build_myself_memory_expected)
