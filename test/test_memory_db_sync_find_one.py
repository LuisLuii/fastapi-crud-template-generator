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
        is_async = False
        if is_async:
            database_url = "sqlite+aiosqlite://"
        else:
            database_url = "sqlite://"

        model_list = [DbModel(db_model=SampleTable, prefix="/my_first_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.FIND_ONE]),
                      DbModel(db_model=SampleTableTwo, prefix="/my_second_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.FIND_ONE])]

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

SQLALCHEMY_DATABASE_URL = f"sqlite://"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       future=True,
                       echo=True,
                       pool_pre_ping=True,
                       pool_recycle=7200,
                       connect_args={"check_same_thread": False}, 
                       poolclass=StaticPool)
session = sessionmaker(bind=engine, autocommit=False)


def db_session() -> Generator:
    try:
        db = session()
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    
SampleTable.__table__.create(engine, checkfirst=True)
SampleTableTwo.__table__.create(engine, checkfirst=True)
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
class SampleTableTwoFindOneRequestBodyModel:
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    bool_value____list: Optional[List[bool]] = Query(None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoFindOneResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(False)

    class Config:
        orm_mode = True


class SampleTableTwoFindOneItemListResponseModel(ExcludeUnsetBaseModel):
    __root__: List[SampleTableTwoFindOneResponseModel]

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
class SampleTableFindOneRequestBodyModel:
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    bool_value____list: Optional[List[bool]] = Query(None)
    char_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive])
    char_value____str: Optional[List[str]] = Query(None)
    char_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    char_value____list: Optional[List[str]] = Query(None)
    date_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    date_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    date_value____from: Optional[NewType(ExtraFieldTypePrefix.From, date)] = Query(None)
    date_value____to: Optional[NewType(ExtraFieldTypePrefix.To, date)] = Query(None)
    date_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    date_value____list: Optional[List[date]] = Query(None)
    float4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    float4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    float4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None)
    float4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None)
    float4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    float4_value____list: Optional[List[float]] = Query(None)
    float8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    float8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    float8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None)
    float8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None)
    float8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    float8_value____list: Optional[List[float]] = Query(None)
    int2_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    int2_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    int2_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None)
    int2_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None)
    int2_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    int2_value____list: Optional[List[int]] = Query(None)
    int4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    int4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    int4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None)
    int4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None)
    int4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    int4_value____list: Optional[List[int]] = Query(None)
    int8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    int8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    int8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None)
    int8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None)
    int8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    int8_value____list: Optional[List[int]] = Query(None)
    text_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive])
    text_value____str: Optional[List[str]] = Query(None)
    text_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    text_value____list: Optional[List[str]] = Query(None)
    time_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    time_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    time_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None)
    time_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None)
    time_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    time_value____list: Optional[List[time]] = Query(None)
    timestamp_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    timestamp_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    timestamp_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None)
    timestamp_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None)
    timestamp_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    timestamp_value____list: Optional[List[datetime]] = Query(None)
    timestamptz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    timestamptz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    timestamptz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None)
    timestamptz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None)
    timestamptz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    timestamptz_value____list: Optional[List[datetime]] = Query(None)
    timetz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to)
    timetz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to)
    timetz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None)
    timetz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None)
    timetz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    timetz_value____list: Optional[List[time]] = Query(None)
    varchar_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive])
    varchar_value____str: Optional[List[str]] = Query(None)
    varchar_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In)
    varchar_value____list: Optional[List[str]] = Query(None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableFindOneResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(False)
    char_value: str = Body(None)
    date_value: date = Body(None)
    float4_value: float = Body(...)
    float8_value: float = Body(10.1)
    int2_value: int = Body(...)
    int4_value: int = Body(...)
    int8_value: int = Body(99)
    text_value: str = Body(None)
    time_value: time = Body(None)
    timestamp_value: datetime = Body(None)
    timestamptz_value: datetime = Body(None)
    timetz_value: time = Body(None)
    varchar_value: str = Body(None)

    class Config:
        orm_mode = True


class SampleTableFindOneItemListResponseModel(ExcludeUnsetBaseModel):
    __root__: List[SampleTableFindOneResponseModel]

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
from common.utils import find_query_builder
from common.sql_session import db_session
from model.test_build_myself_memory_two import SampleTableTwo, SampleTableTwoFindOneRequestBodyModel, SampleTableTwoFindOneResponseModel, SampleTableTwoPrimaryKeyModel

api = APIRouter(tags=['sample api'],prefix="/my_second_api")


@api.get("/{primary_key}", status_code=200, response_model=SampleTableTwoFindOneResponseModel)
def get_one_by_primary_key(
                            response: Response,
                            url_param=Depends(SampleTableTwoPrimaryKeyModel),
                            query=Depends(SampleTableTwoFindOneRequestBodyModel),
                            session=Depends(db_session)):
    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTableTwo)

    extra_query_expression: List[BinaryExpression] = find_query_builder(param=url_param.__dict__,
                                                                        model=SampleTableTwo)
    model = SampleTableTwo
    stmt = select(*[model]).where(and_(*filter_list + extra_query_expression))
    sql_executed_result = session.execute(stmt)

    one_row_data = sql_executed_result.fetchall()
    if not one_row_data or len(one_row_data) < 1:
        return Response('specific data not found', status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    result_value, = one_row_data
    result_value, = dict(result_value).values()
    response_data = {}
    for column in SampleTableTwoFindOneResponseModel.__fields__:
        response_data[column] = getattr(result_value, column)
    response.headers["x-total-count"] = str(1)
    return response_data


'''
        validate_route("test_build_myself_memory_two", route_test_build_myself_memory_two_expected)
        model_test_build_myself_memory_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from common.utils import find_query_builder
from common.sql_session import db_session
from model.test_build_myself_memory import SampleTable, SampleTableFindOneRequestBodyModel, SampleTableFindOneResponseModel, SampleTablePrimaryKeyModel

api = APIRouter(tags=['sample api'],prefix="/my_first_api")


@api.get("/{primary_key}", status_code=200, response_model=SampleTableFindOneResponseModel)
def get_one_by_primary_key(
                            response: Response,
                            url_param=Depends(SampleTablePrimaryKeyModel),
                            query=Depends(SampleTableFindOneRequestBodyModel),
                            session=Depends(db_session)):
    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTable)

    extra_query_expression: List[BinaryExpression] = find_query_builder(param=url_param.__dict__,
                                                                        model=SampleTable)
    model = SampleTable
    stmt = select(*[model]).where(and_(*filter_list + extra_query_expression))
    sql_executed_result = session.execute(stmt)

    one_row_data = sql_executed_result.fetchall()
    if not one_row_data or len(one_row_data) < 1:
        return Response('specific data not found', status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    result_value, = one_row_data
    result_value, = dict(result_value).values()
    response_data = {}
    for column in SampleTableFindOneResponseModel.__fields__:
        response_data[column] = getattr(result_value, column)
    response.headers["x-total-count"] = str(1)
    return response_data


'''
        validate_route("test_build_myself_memory", model_test_build_myself_memory_expected)
