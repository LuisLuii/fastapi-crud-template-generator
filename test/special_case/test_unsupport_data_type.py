import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder
from fastapi_quickcrud_codegen.db_model import DbModel
from fastapi_quickcrud_codegen.misc.type import CrudMethods
from test.misc.common import *
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INTERVAL, JSON, UUID

Base = declarative_base()
metadata = Base.metadata


class TestUuidPrimary(Base):
    __tablename__ = 'test_uuid_primary'
    __table_args__ = (
    )

    primary_key = Column(BLOB, primary_key=True, comment="hello")
    bool_value = Column(Boolean, nullable=False, server_default=text('false'))
    float4_value = Column(Float(53), nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text('10.10'))
    interval_value = Column(INTERVAL)
    int4_value = Column(Integer, nullable=False)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text('now()'))
    int8_value = Column(BigInteger, server_default=text('99'))
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

    def test_project_generation(self):
        try:
            is_async = True
            if is_async:
                database_url = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
            else:
                database_url = "postgresql://postgres:1234@127.0.0.1:5432/postgres"

            model_list = [DbModel(db_model=TestUuidPrimary, prefix="/uuid_pk_api", tags=["sample api"]
                                  , crud_methods=[CrudMethods.FIND_MANY])]

            crud_router_builder(
                db_model_list=model_list,
                is_async=is_async,
                database_url=database_url
            )

        except BaseException as e:
            assert True
            return

        assert False
