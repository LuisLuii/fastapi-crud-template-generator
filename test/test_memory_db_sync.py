from test.conftest import *

import unittest
import pytest
from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder, CrudMethods

Base = declarative_base()
metadata = Base.metadata


# class SampleTable(Base):
#     primary_key_of_table = "primary_key"
#     unique_fields = ['primary_key', 'int4_value', 'float4_value']
#     __tablename__ = 'test_build_myself'
#     __table_args__ = (
#         UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
#     )
#     primary_key = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'}, autoincrement=True,
#                          server_default="nextval('test_build_myself_id_seq'::regclass)")
#     bool_value = Column(Boolean, nullable=False, server_default=text("false"))
#     bytea_value = Column(LargeBinary)
#     char_value = Column(CHAR(10))
#     date_value = Column(Date, server_default=text("now()"))
#     float4_value = Column(Float, nullable=False)
#     float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
#     int2_value = Column(SmallInteger, nullable=False)
#     int4_value = Column(Integer, nullable=False)
#     int8_value = Column(BigInteger, server_default=text("99"))
#     interval_value = Column(INTERVAL)
#     json_value = Column(JSON)
#     jsonb_value = Column(JSONB(astext_type=Text()))
#     numeric_value = Column(Numeric)
#     text_value = Column(Text)
#     time_value = Column(Time)
#     timestamp_value = Column(DateTime)
#     timestamptz_value = Column(DateTime(True))
#     timetz_value = Column(Time(True))
#     uuid_value = Column(UUID(as_uuid=True))
#     varchar_value = Column(String)
#     # xml_value = Column(NullType)
#     array_value = Column(ARRAY(Integer()))
#     array_str__value = Column(ARRAY(String()))
#     # box_valaue = Column(NullType)


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
    # @classmethod
    # def setUpClass(cls):
    #     # SampleTable.__table__.create(engine, checkfirst=True)
    #     # SampleTableTwo.__table__.create(engine, checkfirst=True)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     # SampleTable.__table__.drop()
    #     # SampleTableTwo.__table__.drop()

    def test_project_generation(self):
        is_async = False
        if is_async:
            database_url="sqlite+aiosqlite://"
        else:
            database_url="sqlite://"

        crud_router_builder(
            db_model_list=[
                {
                    "db_model": SampleTable,
                    "prefix": "/my_first_api",
                    "tags": ["sample api"]
                },
                {
                    "db_model": SampleTableTwo,
                    "prefix": "/my_second_api",
                    "tags": ["sample api"]
                }
            ],
            exclude_columns=['bytea_value', 'xml_value', 'box_valaue'],
            crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE],
            is_async=is_async,
            database_url=database_url
        )
