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
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.UPDATE_ONE]),
                      DbModel(db_model=SampleTableTwo, prefix="/my_second_api", tags=["sample api"],
                              exclude_columns=['bytea_value'], crud_methods=[CrudMethods.UPDATE_ONE]), ]

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
class SampleTableTwoUpdateOneRequestQueryModel:
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


@dataclass
class SampleTableTwoUpdateOneRequestBodyModel:
    bool_value: bool = Body(..., description=None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoUpdateOneResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(False)

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
class SampleTableUpdateOneRequestQueryModel:
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

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])
        filter_none(self)


@dataclass
class SampleTableUpdateOneRequestBodyModel:
    bool_value: bool = Body(..., description=None)
    char_value: str = Body(..., description=None)
    date_value: date = Body(..., description=None)
    float4_value: float = Body(..., description=None)
    float8_value: float = Body(..., description=None)
    int2_value: int = Body(..., description=None)
    int4_value: int = Body(..., description=None)
    int8_value: int = Body(..., description=None)
    interval_value: timedelta = Body(..., description=None)
    json_value: dict = Body(..., description=None)
    jsonb_value: Union[dict, list] = Body(..., description=None)
    numeric_value: Decimal = Body(..., description=None)
    text_value: str = Body(..., description=None)
    time_value: time = Body(..., description=None)
    timestamp_value: datetime = Body(..., description=None)
    timestamptz_value: datetime = Body(..., description=None)
    timetz_value: time = Body(..., description=None)
    uuid_value: uuid.UUID = Body(..., description=None)
    varchar_value: str = Body(..., description=None)
    array_value: List[int] = Body(..., description=None)
    array_str__value: List[str] = Body(..., description=None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])
        filter_none(self)


class SampleTableUpdateOneResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(None)
    char_value: str = Body(None)
    date_value: date = Body(None)
    float4_value: float = Body(...)
    float8_value: float = Body(None)
    int2_value: int = Body(...)
    int4_value: int = Body(...)
    int8_value: int = Body(None)
    interval_value: timedelta = Body(None)
    json_value: dict = Body(None)
    jsonb_value: Union[dict, list] = Body(None)
    numeric_value: Decimal = Body(None)
    text_value: str = Body(None)
    time_value: time = Body(None)
    timestamp_value: datetime = Body(None)
    timestamptz_value: datetime = Body(None)
    timetz_value: time = Body(None)
    uuid_value: uuid.UUID = Body(None)
    varchar_value: str = Body(None)
    array_value: List[int] = Body(None)
    array_str__value: List[str] = Body(None)

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
from common.utils import clean_input_fields, find_query_builder
from common.sql_session import db_session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as
from common.http_exception import UnknownColumn, UnknownOrderType
from common.typing import Ordering
from model.test_build_myself_two import SampleTableTwo, SampleTableTwoPrimaryKeyModel, SampleTableTwoUpdateOneRequestBodyModel, SampleTableTwoUpdateOneRequestQueryModel, SampleTableTwoUpdateOneResponseModel

api = APIRouter(tags=['sample api'],prefix="/my_second_api")


@api.put("/{primary_key}", status_code=200, response_model=SampleTableTwoUpdateOneResponseModel)
def entire_update_by_primary_key(
                                response: Response,
                                primary_key: SampleTableTwoPrimaryKeyModel = Depends(),
                                update_data: SampleTableTwoUpdateOneRequestBodyModel = Depends(),
                                extra_query: SampleTableTwoUpdateOneRequestQueryModel = Depends(),
                                session=Depends(db_session)):
    model = SampleTableTwo

    filter_args = primary_key.__dict__
    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=filter_args,
                                                                 model=model)
    if extra_args:
        filter_list += find_query_builder(param=extra_query.__dict__,
            model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = session.execute(stmt)
    data_instance = sql_executed_result.scalar()

    if not data_instance:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        for update_arg_name, update_arg_value in update_args.items():
            setattr(data_instance, update_arg_name, update_arg_value)

        result = parse_obj_as(SampleTableTwoUpdateOneResponseModel, data_instance)
        response.headers["x-total-count"] = str(1)
        session.flush()
        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result

'''
        validate_route("test_build_myself_two", route_test_build_myself_two_expected)
        route_test_build_myself_expected = '''from http import HTTPStatus
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
from model.test_build_myself import SampleTable, SampleTablePrimaryKeyModel, SampleTableUpdateOneRequestBodyModel, SampleTableUpdateOneRequestQueryModel, SampleTableUpdateOneResponseModel

api = APIRouter(tags=['sample api'],prefix="/my_first_api")


@api.put("/{primary_key}", status_code=200, response_model=SampleTableUpdateOneResponseModel)
def entire_update_by_primary_key(
                                response: Response,
                                primary_key: SampleTablePrimaryKeyModel = Depends(),
                                update_data: SampleTableUpdateOneRequestBodyModel = Depends(),
                                extra_query: SampleTableUpdateOneRequestQueryModel = Depends(),
                                session=Depends(db_session)):
    model = SampleTable

    filter_args = primary_key.__dict__
    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=filter_args,
                                                                 model=model)
    if extra_args:
        filter_list += find_query_builder(param=extra_query.__dict__,
            model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = session.execute(stmt)
    data_instance = sql_executed_result.scalar()

    if not data_instance:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        for update_arg_name, update_arg_value in update_args.items():
            setattr(data_instance, update_arg_name, update_arg_value)

        result = parse_obj_as(SampleTableUpdateOneResponseModel, data_instance)
        response.headers["x-total-count"] = str(1)
        session.flush()
        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result

'''
        validate_route("test_build_myself", route_test_build_myself_expected)
