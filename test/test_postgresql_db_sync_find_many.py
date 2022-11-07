import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder
from src.fastapi_quickcrud_codegen.db_model import DbModel
from src.fastapi_quickcrud_codegen.misc.type import CrudMethods
from test.misc.common import *

Base = declarative_base()
metadata = Base.metadata


class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'}, autoincrement=True,
                         server_default="nextval('test_build_myself_id_seq'::regclass)")
    bool_value = Column(Boolean, nullable=False, server_default=text("false"))
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text("now()"))
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, server_default=text("99"))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB(astext_type=Text()))
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_two'
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
            database_url = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
        else:
            database_url = "postgresql://postgres:1234@127.0.0.1:5432/postgres"

        
        model_list = [DbModel(db_model=SampleTable, prefix="/my_first_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.FIND_MANY]),
                      DbModel(db_model=SampleTableTwo, prefix="/my_second_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.FIND_MANY]), ]

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

from route.test_build_myself import api as test_build_myself_router
from route.test_build_myself_two import api as test_build_myself_two_router
app = FastAPI()

[app.include_router(api_route) for api_route in [
test_build_myself_router,test_build_myself_two_router,
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

from model.test_build_myself import SampleTable
from model.test_build_myself_two import SampleTableTwo

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:1234@127.0.0.1:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       future=True,
                       echo=True,
                       pool_pre_ping=True,
                       pool_recycle=7200,
                       
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
        db.close()'''
        validate_common_sql_session(common_sql_session_expected)

        # model
        model_test_build_myself_two_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from common.db import Base
from common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators

PRIMARY_KEY_NAME = "primary_key"
UNIQUE_LIST = "primary_key"
    

class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_two'
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
    total: int
    result: List[SampleTableTwoFindManyResponseModel]

    class Config:
        orm_mode = True


'''
        validate_model("test_build_myself_two", model_test_build_myself_two_expected)

        model_test_build_myself_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from common.db import Base
from common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators

PRIMARY_KEY_NAME = "primary_key"
UNIQUE_LIST = "primary_key", "int4_value", "float4_value"
    

class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'}, autoincrement=True,
                         server_default="nextval('test_build_myself_id_seq'::regclass)")
    bool_value = Column(Boolean, nullable=False, server_default=text("false"))
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text("now()"))
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, server_default=text("99"))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB(astext_type=Text()))
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


@dataclass
class SampleTablePrimaryKeyModel:
    primary_key: int = Query(None, description=None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])


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
    char_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
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
    numeric_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    numeric_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    numeric_value____from: Optional[NewType(ExtraFieldTypePrefix.From, Decimal)] = Query(None, description=None)
    numeric_value____to: Optional[NewType(ExtraFieldTypePrefix.To, Decimal)] = Query(None, description=None)
    numeric_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    numeric_value____list: Optional[List[Decimal]] = Query(None, description=None)
    text_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
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
    uuid_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    uuid_value____list: Optional[List[uuid.UUID]] = Query(None, description=None)
    varchar_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    varchar_value____str: Optional[List[str]] = Query(None, description=None)
    varchar_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    varchar_value____list: Optional[List[str]] = Query(None, description=None)
    limit: Optional[int] = Query(None)
    offset: Optional[int] = Query(None)
    order_by_columns: Optional[List[pydantic.constr(regex="(?=(primary_key|bool_value|char_value|date_value|float4_value|float8_value|int2_value|int4_value|int8_value|interval_value|json_value|jsonb_value|numeric_value|text_value|time_value|timestamp_value|timestamptz_value|timetz_value|uuid_value|varchar_value|array_value|array_str__value)?\s?:?\s*?(?=(DESC|ASC))?)")]] = Query(
                None,
                description="""<br> support column: 
            <br> ['primary_key', 'bool_value', 'char_value', 'date_value', 'float4_value', 'float8_value', 'int2_value', 'int4_value', 'int8_value', 'interval_value', 'json_value', 'jsonb_value', 'numeric_value', 'text_value', 'time_value', 'timestamp_value', 'timestamptz_value', 'timetz_value', 'uuid_value', 'varchar_value', 'array_value', 'array_str__value'] <hr><br> support ordering:  
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
        value_of_list_to_str(self, ['uuid_value'])
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
    interval_value: timedelta = None
    json_value: dict = None
    jsonb_value: Union[dict, list] = None
    numeric_value: Decimal = None
    text_value: str = None
    time_value: time = None
    timestamp_value: datetime = None
    timestamptz_value: datetime = None
    timetz_value: time = None
    uuid_value: uuid.UUID = None
    varchar_value: str = None
    array_value: List[int] = None
    array_str__value: List[str] = None

    class Config:
        orm_mode = True


class SampleTableFindManyItemListResponseModel(ExcludeUnsetBaseModel):
    total: int
    result: List[SampleTableFindManyResponseModel]

    class Config:
        orm_mode = True


'''
        validate_model("test_build_myself", model_test_build_myself_expected)

        # route
        route_test_build_myself_two_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from common.utils import find_query_builder
from common.sql_session import db_session
from model.test_build_myself_two import SampleTableTwo, SampleTableTwoFindManyItemListResponseModel, SampleTableTwoFindManyRequestBodyModel, SampleTableTwoFindManyResponseModel
from pydantic import parse_obj_as
from common.http_exception import UnknownColumn, UnknownOrderType
from common.typing import Ordering

api = APIRouter(tags=['sample api'],prefix="/my_second_api")


@api.get("", status_code=200, response_model=SampleTableTwoFindManyItemListResponseModel)
def get_many(
            response: Response,
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
                raise UnknownColumn(400,f'Column {sort_column} is not existed')
            if not order_by:
                order_by_query_list.append(getattr(model, sort_column).asc())
            elif order_by.upper() == Ordering.DESC.upper():
                order_by_query_list.append(getattr(model, sort_column).desc())
            elif order_by.upper() == Ordering.ASC.upper():
                order_by_query_list.append(getattr(model, sort_column).asc())
            else:
                raise UnknownOrderType(400,f"Unknown order type {order_by}, only accept DESC or ASC")
        if order_by_query_list:
            stmt = stmt.order_by(*order_by_query_list)

    sql_executed_result_without_paginate = session.execute(stmt)
    total = len(sql_executed_result_without_paginate.fetchall())

    response_format = {
            "total": 0,
            "result": []
        }
    if total < 1:
        response_data = parse_obj_as(SampleTableTwoFindManyItemListResponseModel, response_format)
        response.headers["x-total-count"] = str(0)
        return response_data

    stmt = stmt.limit(limit).offset(offset)

    sql_executed_result = session.execute(stmt)

    result = sql_executed_result.fetchall()
    response_data_list = []
    for i in result:
        result_value, = dict(i).values()
        temp = {}
        for column in SampleTableTwoFindManyResponseModel.__fields__:
            temp[column] = getattr(result_value, column)
        response_data_list.append(temp)

    response_format["total"] = total
    response_format["result"] = response_data_list
    response_data = parse_obj_as(SampleTableTwoFindManyItemListResponseModel, response_format)
    response.headers["x-total-count"] = str(len(response_data_list))
    return response_data

'''
        validate_route("test_build_myself_two", route_test_build_myself_two_expected)
        route_test_build_myself_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from common.utils import find_query_builder
from common.sql_session import db_session
from model.test_build_myself import SampleTable, SampleTableFindManyItemListResponseModel, SampleTableFindManyRequestBodyModel, SampleTableFindManyResponseModel
from pydantic import parse_obj_as
from common.http_exception import UnknownColumn, UnknownOrderType
from common.typing import Ordering

api = APIRouter(tags=['sample api'],prefix="/my_first_api")


@api.get("", status_code=200, response_model=SampleTableFindManyItemListResponseModel)
def get_many(
            response: Response,
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
                raise UnknownColumn(400,f'Column {sort_column} is not existed')
            if not order_by:
                order_by_query_list.append(getattr(model, sort_column).asc())
            elif order_by.upper() == Ordering.DESC.upper():
                order_by_query_list.append(getattr(model, sort_column).desc())
            elif order_by.upper() == Ordering.ASC.upper():
                order_by_query_list.append(getattr(model, sort_column).asc())
            else:
                raise UnknownOrderType(400,f"Unknown order type {order_by}, only accept DESC or ASC")
        if order_by_query_list:
            stmt = stmt.order_by(*order_by_query_list)

    sql_executed_result_without_paginate = session.execute(stmt)
    total = len(sql_executed_result_without_paginate.fetchall())

    response_format = {
            "total": 0,
            "result": []
        }
    if total < 1:
        response_data = parse_obj_as(SampleTableFindManyItemListResponseModel, response_format)
        response.headers["x-total-count"] = str(0)
        return response_data

    stmt = stmt.limit(limit).offset(offset)

    sql_executed_result = session.execute(stmt)

    result = sql_executed_result.fetchall()
    response_data_list = []
    for i in result:
        result_value, = dict(i).values()
        temp = {}
        for column in SampleTableFindManyResponseModel.__fields__:
            temp[column] = getattr(result_value, column)
        response_data_list.append(temp)

    response_format["total"] = total
    response_format["result"] = response_data_list
    response_data = parse_obj_as(SampleTableFindManyItemListResponseModel, response_format)
    response.headers["x-total-count"] = str(len(response_data_list))
    return response_data

'''
        validate_route("test_build_myself", route_test_build_myself_expected)

