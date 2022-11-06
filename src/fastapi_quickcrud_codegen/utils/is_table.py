from typing import Union

from sqlalchemy import Table
from sqlalchemy.orm import decl_api


def is_table(db_model: Union[Table, decl_api.DeclarativeMeta]):
    if isinstance(db_model, Table):
        return True
    return False