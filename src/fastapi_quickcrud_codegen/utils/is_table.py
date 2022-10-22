from sqlalchemy import Table


def is_table(db_model):
    if isinstance(db_model, Table):
        return True
    return False