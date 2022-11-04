import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
from test.misc.common import *
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INTERVAL, JSON, UUID

Base = declarative_base()
metadata = Base.metadata


class TestUuidPrimary(Base):
    __tablename__ = 'test_uuid_primary'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )

    primary_key = Column(UUID(as_uuid=True), primary_key=True)
    bool_value = Column(Boolean, nullable=False, server_default=text('false'))
    float4_value = Column(Float(53), nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text('10.10'))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text('now()'))
    int8_value = Column(BigInteger, server_default=text('99'))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB)
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


class Testing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        is_async = True
        if is_async:
            database_url = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
        else:
            database_url="postgresql://postgres:1234@127.0.0.1:5432/postgres"

        crud_router_builder(
            db_model_list=[
                {
                    "db_model": TestUuidPrimary,
                    "prefix": "/uuid_pk_api",
                    "tags": ["sample api"],
                    "crud_methods": []
                }
            ],
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

from fastapi_quick_crud_template.route.test_uuid_primary import api as test_uuid_primary_router
app = FastAPI()

[app.include_router(api_route) for api_route in [
test_uuid_primary_router,
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

from fastapi_quick_crud_template.model.test_uuid_primary import TestUuidPrimary

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                             future=True,
                             echo=True,
                             pool_pre_ping=True,
                             pool_recycle=7200,
                             
                             poolclass=StaticPool)
session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine,
                       class_=AsyncSession)


async def db_session():
    async with session() as _session:
        yield _session
        await _session.commit()'''
        validate_common_sql_session(common_sql_session_expected)

        # model
        model_test_uuid_primary = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from fastapi_quick_crud_template.common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from fastapi_quick_crud_template.common.db import Base
from fastapi_quick_crud_template.common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators

PRIMARY_KEY_NAME = "primary_key"
UNIQUE_LIST = "primary_key", "int4_value", "float4_value"
    

class TestUuidPrimary(Base):
    __tablename__ = 'test_uuid_primary'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )

    primary_key = Column(UUID(as_uuid=True), primary_key=True)
    bool_value = Column(Boolean, nullable=False, server_default=text('false'))
    float4_value = Column(Float(53), nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text('10.10'))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text('now()'))
    int8_value = Column(BigInteger, server_default=text('99'))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB)
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


@dataclass
class TestUuidPrimaryPrimaryKeyModel:
    primary_key: uuid.UUID = Query(..., description=None)

    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['primary_key'])


'''
        validate_model("test_uuid_primary", model_test_uuid_primary)

        # route
        route_test_uuid_primary = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from fastapi_quick_crud_template.common.utils import find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session

api = APIRouter(tags=['sample api'],prefix="/uuid_pk_api")


'''
        validate_route("test_uuid_primary", route_test_uuid_primary)
