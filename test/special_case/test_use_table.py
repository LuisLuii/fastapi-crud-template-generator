import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder
from src.fastapi_quickcrud_codegen.db_model import DbModel
from src.fastapi_quickcrud_codegen.misc.type import CrudMethods
from test.misc.common import *
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INTERVAL, JSON, UUID

Base = declarative_base()
metadata = Base.metadata


t_hello = Table(
    'hello', metadata,
    Column('code', nullable=False),
    Column('group'),
)


class Testing(unittest.TestCase):
    def test_raise(cls):
        is_async = True
        if is_async:
            database_url = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
        else:
            database_url="postgresql://postgres:1234@127.0.0.1:5432/postgres"
        try:

            model_list = [DbModel(db_model=t_hello, prefix="/test", tags=["sample api"], crud_methods=[])]

            crud_router_builder(
                db_model_list=model_list,
                is_async=is_async,
                database_url=database_url
            )
        except RuntimeError as e:
            assert True
            return
        assert False