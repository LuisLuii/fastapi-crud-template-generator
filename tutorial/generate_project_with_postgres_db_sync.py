import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, \
    Numeric, SmallInteger, String, Text, Time, UniqueConstraint, LargeBinary, text, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INTERVAL, JSON, UUID
from sqlalchemy.orm import declarative_base

from fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
from fastapi_quickcrud_codegen.misc.type import SqlType


Base = declarative_base()
metadata = Base.metadata

class TestBuildMyself(Base):
    __tablename__ = 'test_build_myself'
    __table_args__ = (
        PrimaryKeyConstraint('primary_key', name='test_build_myself_pkey'),
        UniqueConstraint('primary_key', 'int4_value', 'float4_value', name='test_build_myself_primary_key_int4_value_float4_value_key')
    )

    primary_key = Column(Integer)
    bool_value = Column(Boolean, nullable=False, server_default=text('false'))
    float4_value = Column(Float(53), nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text('10.10'))
    int2_value = Column(SmallInteger, nullable=False)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text('now()'))
    int4_value = Column(Integer)
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
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


class TestUuidPrimarySync(Base):
    __tablename__ = 'test_uuid_primary_sync'
    __table_args__ = (
        PrimaryKeyConstraint('primary_key', name='test_uuid_primary_sync_pkey'),
        UniqueConstraint('primary_key', 'int4_value', 'float4_value', name='test_uuid_primary_sync_primary_key_int4_value_float4_value_key')
    )

    primary_key = Column(Integer)
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

crud_router_builder(
    db_model_list=[
        {
            "db_model": TestBuildMyself,
            "prefix": "/my_first_api",
            "tags": ["sample api"]
        },

        {
            "db_model": TestUuidPrimarySync,
            "prefix": "/my_second_api",
            "tags": ["sample api"]
        }
    ],
    exclude_columns=['bytea_value', 'xml_value', 'box_valaue'],
    crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_MANY, CrudMethods.UPDATE_ONE],
    is_async=True,
    # database_url="postgresql://postgres:1234@127.0.0.1:5432/postgres"
    database_url="postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
)
