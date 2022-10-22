import inspect
import sys

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

def called():
    print(inspect.getsource(sys._getframe().f_back))
def table_to_declarative_base(db_model):
    print(dir(db_model))
    print(called())
    db_name = str(db_model.fullname)
    Base = declarative_base()
    table_dict = {'__tablename__': db_name}
    if not db_model.primary_key:
        db_model.append_column(Column('__id', Integer, primary_key=True, autoincrement=True))
    for i in db_model.c:
        _, = i.expression.base_columns
        _.table = None
        a = str(_.base_columns)
        table_dict[str(i.key)] = _
    tmp = type(f'{db_name}', (Base,), table_dict)
    tmp.__table__ = db_model
    return tmp
