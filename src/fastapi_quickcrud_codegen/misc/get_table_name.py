from sqlalchemy.orm import decl_api


def get_table_name_from_model(table: decl_api.DeclarativeMeta):
    return table.__tablename__


def get_table_name(table: decl_api.DeclarativeMeta):
    return get_table_name_from_model(table)
