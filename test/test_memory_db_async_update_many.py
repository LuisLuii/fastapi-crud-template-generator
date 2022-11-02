import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
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

        crud_router_builder(
            db_model_list=[
                {
                    "db_model": SampleTable,
                    "prefix": "/my_first_api",
                    "tags": ["sample api"],
                    "exclude_columns": ['bytea_value']
                },
                {
                    "db_model": SampleTableTwo,
                    "prefix": "/my_second_api",
                    "tags": ["sample api"],
                    "exclude_columns": ['bytea_value']
                }
            ],
            crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE, CrudMethods.UPDATE_MANY],
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

from fastapi_quick_crud_template.route.test_build_myself_memory import api as test_build_myself_memory_router
from fastapi_quick_crud_template.route.test_build_myself_memory_two import api as test_build_myself_memory_two_router
app = FastAPI()

[app.include_router(api_route) for api_route in [
test_build_myself_memory_router,test_build_myself_memory_two_router,
]]

uvicorn.run(app, host="0.0.0.0", port=8000)"""
        validate_app(expected=app_expected)

        # common
        #   sql_session
        common_sql_session_expected='''import asyncio
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool


from fastapi_quick_crud_template.model.test_build_myself_memory import SampleTable
from fastapi_quick_crud_template.model.test_build_myself_memory_two import SampleTableTwo


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
from fastapi_quick_crud_template.common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from fastapi_quick_crud_template.common.db import Base
from fastapi_quick_crud_template.common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators





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



    
PRIMARY_KEY_NAME = "primary_key"
    
    
UNIQUE_LIST = "primary_key"
    


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


@dataclass
class SampleTableTwoFindManyRequestBodyModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    limit: Optional[int] = Query(None)
    offset: Optional[int] = Query(None)
    order_by_columns: Optional[List[pydantic.constr(regex="(?=(primary_key|bool_value)?\s?:?\s*?(?=(DESC|ASC))?)")]] = Query(
                None,
                description="""<br> support column: 
            <br> ['primary_key', 'bool_value'] <hr><br> support ordering:  
            <br> ['DESC', 'ASC'] 
            <hr> 
            <br/>example: 
            <br/>&emsp;&emsp;any name of column:ASC
            <br/>&emsp;&emsp;any name of column: DESC 
            <br/>&emsp;&emsp;any name of column    :    DESC
            <br/>&emsp;&emsp;any name of column (default sort by ASC)""")
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoFindManyResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = None
    bool_value: bool = None
    class Config:
        orm_mode = True


class SampleTableTwoFindManyItemListResponseModel(ExcludeUnsetBaseModel):
    __root__: List[SampleTableTwoFindManyResponseModel]
    class Config:
        orm_mode = True


@dataclass
class SampleTableTwoCreateOneRequestBodyModel:
    primary_key: int = Body(None, description=None)
    bool_value: bool = Body(False, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoCreateOneResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None, description=None)
    bool_value: bool = Body(False, description=None)
    class Config:
        orm_mode = True


@dataclass
class SampleTableTwoUpdateManyRequestQueryModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


@dataclass
class SampleTableTwoUpdateManyRequestBodyModel:
    bool_value: bool = Body(..., description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoUpdateManyResponseItemModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(False)
    class Config:
        orm_mode = True


class SampleTableTwoUpdateManyItemListResponseModel(BaseModel):
    __root__: List[SampleTableTwoUpdateManyResponseItemModel]
    class Config:
        orm_mode = True'''
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
from fastapi_quick_crud_template.common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from fastapi_quick_crud_template.common.db import Base
from fastapi_quick_crud_template.common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators





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



    
PRIMARY_KEY_NAME = "primary_key"
    
    
UNIQUE_LIST = "primary_key", "int4_value", "float4_value"
    


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


@dataclass
class SampleTableFindManyRequestBodyModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    char_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    char_value____str: Optional[List[str]] = Query(None, description=None)
    char_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    char_value____list: Optional[List[str]] = Query(None, description=None)
    date_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    date_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    date_value____from: Optional[NewType(ExtraFieldTypePrefix.From, date)] = Query(None, description=None)
    date_value____to: Optional[NewType(ExtraFieldTypePrefix.To, date)] = Query(None, description=None)
    date_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    date_value____list: Optional[List[date]] = Query(None, description=None)
    float4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float4_value____list: Optional[List[float]] = Query(None, description=None)
    float8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float8_value____list: Optional[List[float]] = Query(None, description=None)
    int2_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int2_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int2_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int2_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int2_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int2_value____list: Optional[List[int]] = Query(None, description=None)
    int4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int4_value____list: Optional[List[int]] = Query(None, description=None)
    int8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int8_value____list: Optional[List[int]] = Query(None, description=None)
    text_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    text_value____str: Optional[List[str]] = Query(None, description=None)
    text_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    text_value____list: Optional[List[str]] = Query(None, description=None)
    time_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    time_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    time_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    time_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    time_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    time_value____list: Optional[List[time]] = Query(None, description=None)
    timestamp_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamp_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamp_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamp_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamp_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamp_value____list: Optional[List[datetime]] = Query(None, description=None)
    timestamptz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamptz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamptz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamptz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamptz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamptz_value____list: Optional[List[datetime]] = Query(None, description=None)
    timetz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timetz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timetz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    timetz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    timetz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timetz_value____list: Optional[List[time]] = Query(None, description=None)
    varchar_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    varchar_value____str: Optional[List[str]] = Query(None, description=None)
    varchar_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    varchar_value____list: Optional[List[str]] = Query(None, description=None)
    limit: Optional[int] = Query(None)
    offset: Optional[int] = Query(None)
    order_by_columns: Optional[List[pydantic.constr(regex="(?=(primary_key|bool_value|char_value|date_value|float4_value|float8_value|int2_value|int4_value|int8_value|text_value|time_value|timestamp_value|timestamptz_value|timetz_value|varchar_value)?\s?:?\s*?(?=(DESC|ASC))?)")]] = Query(
                None,
                description="""<br> support column: 
            <br> ['primary_key', 'bool_value', 'char_value', 'date_value', 'float4_value', 'float8_value', 'int2_value', 'int4_value', 'int8_value', 'text_value', 'time_value', 'timestamp_value', 'timestamptz_value', 'timetz_value', 'varchar_value'] <hr><br> support ordering:  
            <br> ['DESC', 'ASC'] 
            <hr> 
            <br/>example: 
            <br/>&emsp;&emsp;any name of column:ASC
            <br/>&emsp;&emsp;any name of column: DESC 
            <br/>&emsp;&emsp;any name of column    :    DESC
            <br/>&emsp;&emsp;any name of column (default sort by ASC)""")
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableFindManyResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = None
    bool_value: bool = None
    char_value: str = None
    date_value: date = None
    float4_value: float = None
    float8_value: float = None
    int2_value: int = None
    int4_value: int = None
    int8_value: int = None
    text_value: str = None
    time_value: time = None
    timestamp_value: datetime = None
    timestamptz_value: datetime = None
    timetz_value: time = None
    varchar_value: str = None
    class Config:
        orm_mode = True


class SampleTableFindManyItemListResponseModel(ExcludeUnsetBaseModel):
    __root__: List[SampleTableFindManyResponseModel]
    class Config:
        orm_mode = True


@dataclass
class SampleTableCreateOneRequestBodyModel:
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
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableCreateOneResponseModel(BaseModel):
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


@dataclass
class SampleTableUpdateManyRequestQueryModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    char_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    char_value____str: Optional[List[str]] = Query(None, description=None)
    char_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    char_value____list: Optional[List[str]] = Query(None, description=None)
    date_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    date_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    date_value____from: Optional[NewType(ExtraFieldTypePrefix.From, date)] = Query(None, description=None)
    date_value____to: Optional[NewType(ExtraFieldTypePrefix.To, date)] = Query(None, description=None)
    date_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    date_value____list: Optional[List[date]] = Query(None, description=None)
    float4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float4_value____list: Optional[List[float]] = Query(None, description=None)
    float8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float8_value____list: Optional[List[float]] = Query(None, description=None)
    int2_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int2_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int2_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int2_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int2_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int2_value____list: Optional[List[int]] = Query(None, description=None)
    int4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int4_value____list: Optional[List[int]] = Query(None, description=None)
    int8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int8_value____list: Optional[List[int]] = Query(None, description=None)
    text_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    text_value____str: Optional[List[str]] = Query(None, description=None)
    text_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    text_value____list: Optional[List[str]] = Query(None, description=None)
    time_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    time_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    time_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    time_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    time_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    time_value____list: Optional[List[time]] = Query(None, description=None)
    timestamp_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamp_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamp_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamp_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamp_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamp_value____list: Optional[List[datetime]] = Query(None, description=None)
    timestamptz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamptz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamptz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamptz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamptz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamptz_value____list: Optional[List[datetime]] = Query(None, description=None)
    timetz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timetz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timetz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    timetz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    timetz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timetz_value____list: Optional[List[time]] = Query(None, description=None)
    varchar_value____str_____matching_pattern: Optional[List[MatchingPatternInStringBase]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    varchar_value____str: Optional[List[str]] = Query(None, description=None)
    varchar_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    varchar_value____list: Optional[List[str]] = Query(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


@dataclass
class SampleTableUpdateManyRequestBodyModel:
    bool_value: bool = Body(..., description=None)
    char_value: str = Body(..., description=None)
    date_value: date = Body(..., description=None)
    float4_value: float = Body(..., description=None)
    float8_value: float = Body(..., description=None)
    int2_value: int = Body(..., description=None)
    int4_value: int = Body(..., description=None)
    int8_value: int = Body(..., description=None)
    text_value: str = Body(..., description=None)
    time_value: time = Body(..., description=None)
    timestamp_value: datetime = Body(..., description=None)
    timestamptz_value: datetime = Body(..., description=None)
    timetz_value: time = Body(..., description=None)
    varchar_value: str = Body(..., description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableUpdateManyResponseItemModel(BaseModel):
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


class SampleTableUpdateManyItemListResponseModel(BaseModel):
    __root__: List[SampleTableUpdateManyResponseItemModel]
    class Config:
        orm_mode = True'''
        validate_model("test_build_myself_memory", model_test_build_myself_memory_expected)

        # route
        route_test_build_myself_memory_two_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from fastapi_quick_crud_template.common.utils import clean_input_fields, find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session
from fastapi_quick_crud_template.model.test_build_myself_memory_two import SampleTableTwo, SampleTableTwoCreateOneRequestBodyModel, SampleTableTwoCreateOneResponseModel, SampleTableTwoFindManyItemListResponseModel, SampleTableTwoFindManyRequestBodyModel, SampleTableTwoFindManyResponseModel, SampleTableTwoFindOneRequestBodyModel, SampleTableTwoFindOneResponseModel, SampleTableTwoPrimaryKeyModel, SampleTableTwoUpdateManyItemListResponseModel, SampleTableTwoUpdateManyRequestBodyModel, SampleTableTwoUpdateManyRequestQueryModel
from pydantic import parse_obj_as
from fastapi_quick_crud_template.common.http_exception import UnknownColumn, UnknownOrderType
from fastapi_quick_crud_template.common.typing import Ordering
from sqlalchemy.exc import IntegrityError



api = APIRouter(tags=['sample api'],prefix="/my_second_api")



@api.get("/{primary_key}", status_code=200, response_model=SampleTableTwoFindOneResponseModel)
async def get_one_by_primary_key(response: Response,
                           url_param=Depends(SampleTableTwoPrimaryKeyModel),
                           query=Depends(SampleTableTwoFindOneRequestBodyModel),
                           session=Depends(db_session)):


    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTableTwo)

    extra_query_expression: List[BinaryExpression] = find_query_builder(param=url_param.__dict__,
                                                                        model=SampleTableTwo)
    model = SampleTableTwo
    stmt = select(*[model]).where(and_(*filter_list + extra_query_expression))
    sql_executed_result = await session.execute(stmt)

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


@api.get("", status_code=200, response_model=SampleTableTwoFindManyItemListResponseModel)
async def get_many(response: Response,
                           query=Depends(SampleTableTwoFindManyRequestBodyModel),
                           session=Depends(db_session)):

    filter_args = query.__dict__
    limit = filter_args.pop('limit', None)
    offset = filter_args.pop('offset', None)
    order_by_columns = filter_args.pop('order_by_columns', None)
    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTableTwo)
    model = SampleTableTwo
    stmt = select(*[model]).filter(and_(*filter_list))
    if order_by_columns:
        order_by_query_list = []

        for order_by_column in order_by_columns:
            if not order_by_column:
                continue
            sort_column, order_by = (order_by_column.replace(' ', '').split(':') + [None])[:2]
            if not hasattr(model, sort_column):
                raise UnknownColumn(f'column {sort_column} is not exited')
            if not order_by:
                order_by_query_list.append(getattr(model, sort_column).asc())
            elif order_by.upper() == Ordering.DESC.upper():
                order_by_query_list.append(getattr(model, sort_column).desc())
            elif order_by.upper() == Ordering.ASC.upper():
                order_by_query_list.append(getattr(model, sort_column).asc())
            else:
                raise UnknownOrderType(f"Unknown order type {order_by}, only accept DESC or ASC")
        if order_by_query_list:
            stmt = stmt.order_by(*order_by_query_list)
    stmt = stmt.limit(limit).offset(offset)

    sql_executed_result = await session.execute(stmt)

    result = sql_executed_result.fetchall()
    if not result:
        return Response(status_code=HTTPStatus.NO_CONTENT)
    response_data_list = []
    for i in result:
        result_value, = dict(i).values()
        temp = {}
        for column in SampleTableTwoFindManyResponseModel.__fields__:
            temp[column] = getattr(result_value, column)
        response_data_list.append(temp)
    if not response_data_list:
        return Response(status_code=HTTPStatus.NO_CONTENT)

    response_data = parse_obj_as(SampleTableTwoFindManyItemListResponseModel, response_data_list)
    response.headers["x-total-count"] = str(len(response_data_list))
    return response_data

@api.post("", status_code=201, response_model=SampleTableTwoCreateOneResponseModel)
async def insert_one(response: Response,
                           request_body=Depends(SampleTableTwoCreateOneRequestBodyModel),
                           session=Depends(db_session)):
    insert_arg_dict: Union[list, dict] = request_body.__dict__
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
        result = Response(status_code=HTTPStatus.CONFLICT)
        return result
    inserted_data, = new_inserted_data
    result = parse_obj_as(SampleTableTwoCreateOneResponseModel, inserted_data)
    response.headers["x-total-count"] = str(1)
    return result

@api.put("", status_code=200, response_model=SampleTableTwoUpdateManyItemListResponseModel)
async def entire_update_many_by_query(
                                                response: Response,
                                                update_data: SampleTableTwoUpdateManyRequestBodyModel = Depends(),
                                                extra_query: SampleTableTwoUpdateManyRequestQueryModel = Depends(),
                                                session=Depends(db_session)):
    model = SampleTableTwo

    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=extra_args,
                                                             model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = await session.execute(stmt)
    data_instance_list = [i for i in sql_executed_result.scalars()]


    if not data_instance_list:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        response_data = []
        for i in data_instance_list:
            for update_arg_name, update_arg_value in update_args.items():
                        setattr(i, update_arg_name, update_arg_value)
            response_data.append(i)

        result = parse_obj_as(SampleTableTwoUpdateManyItemListResponseModel, response_data)
        response.headers["x-total-count"] = str(len(response_data))

        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT)
        return result'''
        validate_route("test_build_myself_memory_two", route_test_build_myself_memory_two_expected)
        model_test_build_myself_memory_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from fastapi_quick_crud_template.common.utils import clean_input_fields, find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session
from fastapi_quick_crud_template.model.test_build_myself_memory import SampleTable, SampleTableCreateOneRequestBodyModel, SampleTableCreateOneResponseModel, SampleTableFindManyItemListResponseModel, SampleTableFindManyRequestBodyModel, SampleTableFindManyResponseModel, SampleTableFindOneRequestBodyModel, SampleTableFindOneResponseModel, SampleTablePrimaryKeyModel, SampleTableUpdateManyItemListResponseModel, SampleTableUpdateManyRequestBodyModel, SampleTableUpdateManyRequestQueryModel
from pydantic import parse_obj_as
from fastapi_quick_crud_template.common.http_exception import UnknownColumn, UnknownOrderType
from fastapi_quick_crud_template.common.typing import Ordering
from sqlalchemy.exc import IntegrityError



api = APIRouter(tags=['sample api'],prefix="/my_first_api")



@api.get("/{primary_key}", status_code=200, response_model=SampleTableFindOneResponseModel)
async def get_one_by_primary_key(response: Response,
                           url_param=Depends(SampleTablePrimaryKeyModel),
                           query=Depends(SampleTableFindOneRequestBodyModel),
                           session=Depends(db_session)):


    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTable)

    extra_query_expression: List[BinaryExpression] = find_query_builder(param=url_param.__dict__,
                                                                        model=SampleTable)
    model = SampleTable
    stmt = select(*[model]).where(and_(*filter_list + extra_query_expression))
    sql_executed_result = await session.execute(stmt)

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


@api.get("", status_code=200, response_model=SampleTableFindManyItemListResponseModel)
async def get_many(response: Response,
                           query=Depends(SampleTableFindManyRequestBodyModel),
                           session=Depends(db_session)):

    filter_args = query.__dict__
    limit = filter_args.pop('limit', None)
    offset = filter_args.pop('offset', None)
    order_by_columns = filter_args.pop('order_by_columns', None)
    filter_list: List[BinaryExpression] = find_query_builder(param=query.__dict__,
                                                             model=SampleTable)
    model = SampleTable
    stmt = select(*[model]).filter(and_(*filter_list))
    if order_by_columns:
        order_by_query_list = []

        for order_by_column in order_by_columns:
            if not order_by_column:
                continue
            sort_column, order_by = (order_by_column.replace(' ', '').split(':') + [None])[:2]
            if not hasattr(model, sort_column):
                raise UnknownColumn(f'column {sort_column} is not exited')
            if not order_by:
                order_by_query_list.append(getattr(model, sort_column).asc())
            elif order_by.upper() == Ordering.DESC.upper():
                order_by_query_list.append(getattr(model, sort_column).desc())
            elif order_by.upper() == Ordering.ASC.upper():
                order_by_query_list.append(getattr(model, sort_column).asc())
            else:
                raise UnknownOrderType(f"Unknown order type {order_by}, only accept DESC or ASC")
        if order_by_query_list:
            stmt = stmt.order_by(*order_by_query_list)
    stmt = stmt.limit(limit).offset(offset)

    sql_executed_result = await session.execute(stmt)

    result = sql_executed_result.fetchall()
    if not result:
        return Response(status_code=HTTPStatus.NO_CONTENT)
    response_data_list = []
    for i in result:
        result_value, = dict(i).values()
        temp = {}
        for column in SampleTableFindManyResponseModel.__fields__:
            temp[column] = getattr(result_value, column)
        response_data_list.append(temp)
    if not response_data_list:
        return Response(status_code=HTTPStatus.NO_CONTENT)

    response_data = parse_obj_as(SampleTableFindManyItemListResponseModel, response_data_list)
    response.headers["x-total-count"] = str(len(response_data_list))
    return response_data

@api.post("", status_code=201, response_model=SampleTableCreateOneResponseModel)
async def insert_one(response: Response,
                           request_body=Depends(SampleTableCreateOneRequestBodyModel),
                           session=Depends(db_session)):
    insert_arg_dict: Union[list, dict] = request_body.__dict__
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
        result = Response(status_code=HTTPStatus.CONFLICT)
        return result
    inserted_data, = new_inserted_data
    result = parse_obj_as(SampleTableCreateOneResponseModel, inserted_data)
    response.headers["x-total-count"] = str(1)
    return result

@api.put("", status_code=200, response_model=SampleTableUpdateManyItemListResponseModel)
async def entire_update_many_by_query(
                                                response: Response,
                                                update_data: SampleTableUpdateManyRequestBodyModel = Depends(),
                                                extra_query: SampleTableUpdateManyRequestQueryModel = Depends(),
                                                session=Depends(db_session)):
    model = SampleTable

    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=extra_args,
                                                             model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = await session.execute(stmt)
    data_instance_list = [i for i in sql_executed_result.scalars()]


    if not data_instance_list:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        response_data = []
        for i in data_instance_list:
            for update_arg_name, update_arg_value in update_args.items():
                        setattr(i, update_arg_name, update_arg_value)
            response_data.append(i)

        result = parse_obj_as(SampleTableUpdateManyItemListResponseModel, response_data)
        response.headers["x-total-count"] = str(len(response_data))

        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT)
        return result'''
        validate_route("test_build_myself_memory", model_test_build_myself_memory_expected)
