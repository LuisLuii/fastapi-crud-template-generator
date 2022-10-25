import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, \
    Numeric, SmallInteger, String, Text, Time, UniqueConstraint, LargeBinary
from sqlalchemy.orm import declarative_base

from fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
from fastapi_quickcrud_codegen.misc.type import SqlType

engine = sqlalchemy.create_engine('postgresql+asyncpg://postgres:124@127.0.0.1:5432/postgres')
print()


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
    crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE, CrudMethods.UPDATE_ONE, CrudMethods.UPDATE_MANY],
    is_async=False,
    database_url="sqlite://"
    # database_url="sqlite+aiosqlite://"
)
