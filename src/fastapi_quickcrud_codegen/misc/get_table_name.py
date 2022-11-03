def get_table_name_from_model(table):
    return table.__tablename__


def get_table_name(table):
    return get_table_name_from_model(table)