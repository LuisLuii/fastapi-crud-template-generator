import os
import sys

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
current_directory = dirname
template_root_directory = os.path.join(current_directory, 'fastapi_quick_crud_template')

def validate(result, expected):
    contents = result.read()
    assert contents == expected


def validate_app(expected):
    with open(f'{template_root_directory}/app.py') as f:
        validate(f, expected)

def validate_root_init():
    os.path.exists(f"{template_root_directory}/__init__.py")

def validate_model_init():
    os.path.exists(f"{template_root_directory}/model/__init__.py")

def validate_commom_init():
    os.path.exists(f"{template_root_directory}/common/__init__.py")

def validate_route_init():
    os.path.exists(f"{template_root_directory}/route/__init__.py")

def validate_common_db(expected):
    with open(f'{template_root_directory}/common/db.py') as f:
        validate(f, expected)

def validate_common_http_exception(expected):
    with open(f'{template_root_directory}/common/http_exception.py') as f:
        validate(f, expected)

def validate_common_sql_session(expected):
    with open(f'{template_root_directory}/common/sql_session.py') as f:
        validate(f, expected)

def validate_common_typing(expected):
    with open(f'{template_root_directory}/common/typing.py') as f:
        validate(f, expected)

def validate_common_utils(expected):
    with open(f'{template_root_directory}/common/utils.py') as f:
        validate(f, expected)

def validate_model(file_name, expected):
    with open(f'{template_root_directory}/model/{file_name}.py') as f:
        validate(f, expected)

def validate_route(file_name, expected):
    with open(f'{template_root_directory}/route/{file_name}.py') as f:
        validate(f, expected)


def hard_code_validate():
    # root
    validate_root_init()

    # common
    validate_commom_init()
    #   db
    common_db_expected = """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata"""
    validate_common_db(common_db_expected)
    #   http exception
    common_http_exception_expected = '''from fastapi import HTTPException


class FindOneApiNotRegister(HTTPException):
    pass


class CRUDBuilderException(BaseException):
    pass


class RequestMissing(CRUDBuilderException):
    pass


class PrimaryMissing(CRUDBuilderException):
    pass


class UnknownOrderType(CRUDBuilderException):
    pass


class UpdateColumnEmptyException(CRUDBuilderException):
    pass


class UnknownColumn(CRUDBuilderException):
    pass


class QueryOperatorNotFound(CRUDBuilderException):
    pass


class UnknownError(CRUDBuilderException):
    pass


class ConflictColumnsCannotHit(CRUDBuilderException):
    pass


class MultipleSingleUniqueNotSupportedException(CRUDBuilderException):
    pass


class SchemaException(CRUDBuilderException):
    pass


class CompositePrimaryKeyConstraintNotSupportedException(CRUDBuilderException):
    pass


class MultiplePrimaryKeyNotSupportedException(CRUDBuilderException):
    pass


class ColumnTypeNotSupportedException(CRUDBuilderException):
    pass


class InvalidRequestMethod(CRUDBuilderException):
    pass

class FDDRestHTTPException(HTTPException):
    """Baseclass for all HTTP exceptions in FDD Rest API.  This exception can be called as WSGI
        application to render a default error page or you can catch the subclasses
        of it independently and render nicer error messages.
        """'''
    validate_common_http_exception(common_http_exception_expected)
    #   typing
    common_typing_expected = """from enum import Enum, auto
from itertools import chain
from sqlalchemy import or_
from strenum import StrEnum

class CrudMethods(Enum):
    FIND_ONE = "FIND_ONE"
    FIND_MANY = "FIND_MANY"
    UPDATE_ONE = "UPDATE_ONE"
    UPDATE_MANY = "UPDATE_MANY"
    PATCH_ONE = "PATCH_ONE"
    PATCH_MANY = "PATCH_MANY"
    UPSERT_ONE = "UPSERT_ONE"
    UPSERT_MANY = "UPSERT_MANY"
    CREATE_ONE = "CREATE_ONE"
    CREATE_MANY = "CREATE_MANY"
    DELETE_ONE = "DELETE_ONE"
    DELETE_MANY = "DELETE_MANY"
    POST_REDIRECT_GET = "POST_REDIRECT_GET"
    FIND_ONE_WITH_FOREIGN_TREE = "FIND_ONE_WITH_FOREIGN_TREE"
    FIND_MANY_WITH_FOREIGN_TREE = "FIND_MANY_WITH_FOREIGN_TREE"

    @staticmethod
    def get_table_full_crud_method():
        return [CrudMethods.FIND_MANY, CrudMethods.CREATE_MANY, CrudMethods.UPDATE_MANY, CrudMethods.PATCH_MANY,
                CrudMethods.DELETE_MANY]

    @staticmethod
    def get_declarative_model_full_crud_method():
        return [CrudMethods.FIND_MANY, CrudMethods.FIND_ONE,
                CrudMethods.UPDATE_MANY, CrudMethods.UPDATE_ONE,
                CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE, CrudMethods.CREATE_MANY,
                 CrudMethods.DELETE_MANY, CrudMethods.DELETE_ONE, CrudMethods.FIND_ONE_WITH_FOREIGN_TREE,
                 CrudMethods.FIND_MANY_WITH_FOREIGN_TREE]



class ExtraFieldTypePrefix(StrEnum):
    List = '____list'
    From = '____from'
    To = '____to'
    Str = '____str'



class ExtraFieldType(StrEnum):
    Comparison_operator = '_____comparison_operator'
    Matching_pattern = '_____matching_pattern'



class MatchingPatternInStringBase(StrEnum):
    case_insensitive = auto()
    case_sensitive = auto()
    not_case_insensitive = auto()
    not_case_sensitive = auto()
    contains = auto()


class PGSQLMatchingPattern(StrEnum):
    match_regex_with_case_sensitive = auto()
    match_regex_with_case_insensitive = auto()
    does_not_match_regex_with_case_sensitive = auto()
    does_not_match_regex_with_case_insensitive = auto()
    similar_to = auto()
    not_similar_to = auto()


PGSQLMatchingPatternInString = StrEnum('PGSQLMatchingPatternInString',
                                       {Pattern: auto() for Pattern in
                                        chain(MatchingPatternInStringBase, PGSQLMatchingPattern)})

process_type_map = {
    ExtraFieldTypePrefix.List: ExtraFieldType.Comparison_operator,
    ExtraFieldTypePrefix.From: ExtraFieldType.Comparison_operator,
    ExtraFieldTypePrefix.To: ExtraFieldType.Comparison_operator,
    ExtraFieldTypePrefix.Str: ExtraFieldType.Matching_pattern,
}

class RangeFromComparisonOperators(StrEnum):
    Greater_than = auto()
    Greater_than_or_equal_to = auto()


class RangeToComparisonOperators(StrEnum):
    Less_than = auto()
    Less_than_or_equal_to = auto()


class ItemComparisonOperators(StrEnum):
    Equal = auto()
    Not_equal = auto()
    In = auto()
    Not_in = auto()


process_map = {
    RangeFromComparisonOperators.Greater_than:
        lambda field, value: field > value,

    RangeFromComparisonOperators.Greater_than_or_equal_to:
        lambda field, value: field >= value,

    RangeToComparisonOperators.Less_than:
        lambda field, value: field < value,

    RangeToComparisonOperators.Less_than_or_equal_to:
        lambda field, value: field <= value,

    ItemComparisonOperators.Equal:
        lambda field, values: or_(field == value for value in values),

    ItemComparisonOperators.Not_equal:
        lambda field, values: or_(field != value for value in values),

    ItemComparisonOperators.In:
        lambda field, values: or_(field.in_(values)),

    ItemComparisonOperators.Not_in:
        lambda field, values: or_(field.notin_(values)),

    MatchingPatternInStringBase.case_insensitive:
        lambda field, values: or_(field.ilike(value) for value in values),

    MatchingPatternInStringBase.case_sensitive:
        lambda field, values: or_(field.like(value) for value in values),

    MatchingPatternInStringBase.not_case_insensitive:
        lambda field, values: or_(field.not_ilike(value) for value in values),

    MatchingPatternInStringBase.not_case_sensitive:
        lambda field, values: or_(field.not_like(value) for value in values),

    MatchingPatternInStringBase.contains:
        lambda field, values: or_(field.contains(value) for value in values),

    PGSQLMatchingPatternInString.similar_to:
        lambda field, values: or_(field.op("SIMILAR TO")(value) for value in values),

    PGSQLMatchingPatternInString.not_similar_to:
        lambda field, values: or_(field.op("NOT SIMILAR TO")(value) for value in values),

    PGSQLMatchingPatternInString.match_regex_with_case_sensitive:
        lambda field, values: or_(field.op("~")(value) for value in values),

    PGSQLMatchingPatternInString.match_regex_with_case_insensitive:
        lambda field, values: or_(field.op("~*")(value) for value in values),

    PGSQLMatchingPatternInString.does_not_match_regex_with_case_sensitive:
        lambda field, values: or_(field.op("!~")(value) for value in values),

    PGSQLMatchingPatternInString.does_not_match_regex_with_case_insensitive:
        lambda field, values: or_(field.op("!~*")(value) for value in values)
}"""
    validate_common_typing(common_typing_expected)
    #   utils
    common_utils_expected = """from fastapi_quick_crud_template.common.http_exception import QueryOperatorNotFound
from fastapi_quick_crud_template.common.typing import ExtraFieldType, ExtraFieldTypePrefix, process_type_map, process_map


from typing import TypeVar, List, Union
from copy import deepcopy

from sqlalchemy import or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from pydantic import BaseModel


Base = TypeVar("Base", bound=declarative_base)


def find_query_builder(param: dict, model: Base) -> List[Union[BinaryExpression]]:
    query = []
    for column_name, value in param.items():
        if ExtraFieldType.Comparison_operator in column_name or ExtraFieldType.Matching_pattern in column_name:
            continue
        if ExtraFieldTypePrefix.List in column_name:
            type_ = ExtraFieldTypePrefix.List
        elif ExtraFieldTypePrefix.From in column_name:
            type_ = ExtraFieldTypePrefix.From
        elif ExtraFieldTypePrefix.To in column_name:
            type_ = ExtraFieldTypePrefix.To
        elif ExtraFieldTypePrefix.Str in column_name:
            type_ = ExtraFieldTypePrefix.Str
        else:
            query.append((getattr(model, column_name) == value))
            # raise Exception('known error')
            continue
        sub_query = []
        table_column_name = column_name.replace(type_, "")
        operator_column_name = column_name + process_type_map[type_]
        operators = param.get(operator_column_name, None)
        if not operators:
            raise QueryOperatorNotFound(f'The query operator of {column_name} not found!')
        if not isinstance(operators, list):
            operators = [operators]
        for operator in operators:
            sub_query.append(process_map[operator](getattr(model, table_column_name), value))
        query.append((or_(*sub_query)))
    return query


def value_of_list_to_str(request_or_response_object, columns):
    received_request = deepcopy(request_or_response_object.__dict__)
    if isinstance(columns, str):
        columns = [columns]
    if 'insert' in request_or_response_object.__dict__:
        insert_str_list = []
        for insert_item in request_or_response_object.__dict__['insert']:
            for column in columns:
                for insert_item_column, _ in insert_item.__dict__.items():
                    if column in insert_item_column:
                        value_ = insert_item.__dict__[insert_item_column]
                        if value_ is not None:
                            if isinstance(value_, list):
                                str_value_ = [str(i) for i in value_]
                            else:
                                str_value_ = str(value_)
                            setattr(insert_item, insert_item_column, str_value_)
            insert_str_list.append(insert_item)
        setattr(request_or_response_object, 'insert', insert_str_list)
    else:
        for column in columns:
            for received_column_name, _ in received_request.items():
                if column in received_column_name:
                    value_ = received_request[received_column_name]
                    if value_ is not None:
                        if isinstance(value_, list):
                            str_value_ = [str(i) for i in value_]
                        else:
                            str_value_ = str(value_)
                        setattr(request_or_response_object, received_column_name, str_value_)


def filter_none(request_or_response_object):
    received_request = deepcopy(request_or_response_object.__dict__)
    if 'insert' in received_request:
        insert_item_without_null = []
        for received_insert in received_request['insert']:
            received_insert_ = deepcopy(received_insert)
            for received_insert_item, received_insert_value in received_insert_.__dict__.items():
                if hasattr(received_insert_value, '__module__'):
                    if received_insert_value.__module__ == 'fastapi.params' or received_insert_value is None:
                        delattr(received_insert, received_insert_item)
                elif received_insert_value is None:
                    delattr(received_insert, received_insert_item)

            insert_item_without_null.append(received_insert)
        setattr(request_or_response_object, 'insert', insert_item_without_null)
    else:
        for name, value in received_request.items():
            if hasattr(value, '__module__'):
                if value.__module__ == 'fastapi.params' or value is None:
                    delattr(request_or_response_object, name)
            elif value is None:
                delattr(request_or_response_object, name)

class ExcludeUnsetBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_unset"] = True
            return BaseModel.dict(self, *args, **kwargs)
"""
    validate_common_utils(common_utils_expected)

    # model
    validate_model_init()