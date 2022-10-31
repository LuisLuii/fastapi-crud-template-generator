import uuid
import warnings
from copy import deepcopy
from typing import (Optional,
                    Any)
from typing import (Type,
                    Dict,
                    List,
                    Tuple,
                    TypeVar,
                    NewType,
                    Union)

import pydantic
from pydantic import (BaseModel,
                      create_model,
                      BaseConfig)
from pydantic.dataclasses import dataclass as pydantic_dataclass
from sqlalchemy import UniqueConstraint, Table, Column
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import declarative_base

from ..misc.exceptions import (SchemaException,
                               ColumnTypeNotSupportedException)
from ..misc.get_table_name import get_table_name
from ..misc.type import (Ordering,
                         ExtraFieldTypePrefix,
                         ExtraFieldType,
                         SqlType, )
from ..model.model_builder import ModelCodeGen

FOREIGN_PATH_PARAM_KEYWORD = "__pk__"
BaseModelT = TypeVar('BaseModelT', bound=BaseModel)
DataClassT = TypeVar('DataClassT', bound=Any)
DeclarativeClassT = NewType('DeclarativeClassT', declarative_base)
TableNameT = NewType('TableNameT', str)
ResponseModelT = NewType('ResponseModelT', BaseModel)
ForeignKeyName = NewType('ForeignKeyName', str)
TableInstance = NewType('TableInstance', Table)


class ExcludeUnsetBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_unset"] = True
            return BaseModel.dict(self, *args, **kwargs)


class OrmConfig(BaseConfig):
    orm_mode = True


def _add_orm_model_config_into_pydantic_model(pydantic_model, **kwargs) -> BaseModelT:
    validators = kwargs.get('validators', None)
    config = kwargs.get('config', None)
    field_definitions = {
        name_: (field_.outer_type_, field_.field_info.default)
        for name_, field_ in pydantic_model.__fields__.items()
    }
    return create_model(f'{pydantic_model.__name__}WithValidators',
                        **field_definitions,
                        __config__=config,
                        __validators__=validators)


def _model_from_dataclass(kls: DataClassT) -> Type[BaseModel]:
    """ Converts a stdlib dataclass to a pydantic BaseModel. """

    return pydantic_dataclass(kls).__pydantic_model__


def _to_require_but_default(model: Type[BaseModelT]) -> Type[BaseModelT]:
    """
    Create a new BaseModel with the exact same fields as `model`
    but making them all require but there are default value
    """
    config = model.Config
    field_definitions = {}
    for name_, field_ in model.__fields__.items():
        field_definitions[name_] = (field_.outer_type_, field_.field_info.default)
    return create_model(f'{model.__name__}RequireButDefault', **field_definitions,
                        __config__=config)  # type: ignore[arg-type]


def _filter_none(request_or_response_object):
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


class ApiParameterSchemaBuilder:
    unsupported_data_types = ["BLOB"]
    partial_supported_data_types = ["INTERVAL", "JSON", "JSONB"]

    def __init__(self, db_model: Type, sql_type, exclude_column=None, constraints=None,
                 # ,foreign_include=False
                 ):
        self.class_name = db_model.__name__
        self.root_table_name = get_table_name(db_model)
        self.constraints = constraints
        if exclude_column is None:
            self._exclude_column = []
        else:
            self._exclude_column = exclude_column
        self.alias_mapper: Dict[str, str] = {}  # Table not support alias
        self.__db_model: DeclarativeClassT = db_model
        self.__db_model_table: Table = db_model.__table__
        self.db_name: str = db_model.__tablename__
        self.__columns = db_model.__table__.c

        self.code_gen = ModelCodeGen(self.root_table_name, sql_type)
        self.code_gen.gen_model(db_model)

        self.uuid_type_columns = []
        self.str_type_columns = []
        self.number_type_columns = []
        self.datetime_type_columns = []
        self.timedelta_type_columns = []
        self.bool_type_columns = []
        self.json_type_columns = []
        self.array_type_columns = []
        self.foreign_table_response_model_sets: Dict[TableNameT, ResponseModelT] = {}
        self.all_field: List[dict] = self._extract_all_field()
        self.primary_key_str = self._extract_primary()
        self.unique_fields: List[str] = self._extract_unique()
        self.code_gen.build_constant(constants=[("PRIMARY_KEY_NAME", self.primary_key_str),
                                                ("UNIQUE_LIST", self.unique_fields)])
        self.sql_type = sql_type

    def extra_foreign_table(self, db_model=None) -> Dict[ForeignKeyName, dict]:
        if db_model is None:
            db_model = self.__db_model
        return self._extra_foreign_table_from_declarative_base(db_model)

    def _extract_primary(self, db_model_table=None) -> Union[tuple, Tuple[Union[str, Any],
                                                                          DataClassT,
                                                                          Tuple[Union[str, Any],
                                                                                Union[Type[uuid.UUID], Any],
                                                                                Optional[Any]]]]:
        if db_model_table == None:
            db_model_table = self.__db_model_table
        primary_list = db_model_table.primary_key.columns.values()
        if len(primary_list) > 1:
            raise SchemaException(
                f'multiple primary key / or composite not supported; {self.db_name} ')
        primary_key_column, = primary_list
        column_type = str(primary_key_column.type)
        try:
            python_type = primary_key_column.type.python_type
            if column_type in self.unsupported_data_types:
                raise ColumnTypeNotSupportedException(
                    f'The type of column {primary_key_column.key} ({column_type}) not supported yet')
            if column_type in self.partial_supported_data_types:
                warnings.warn(
                    f'The type of column {primary_key_column.key} ({column_type}) '
                    f'is not support data query (as a query parameters )')
        except NotImplementedError:
            raise ColumnTypeNotSupportedException(
                f'The type of column {primary_key_column.key} ({column_type}) not supported yet')
        # handle if python type is UUID
        if python_type.__name__ in ['str',
                                    'int',
                                    'float',
                                    'Decimal',
                                    'bool',
                                    'date',
                                    'time',
                                    'datetime']:
            column_type = python_type.__name__
        elif python_type.__name__ in ['UUID']:
            column_type = "uuid.UUID"
        else:
            raise ColumnTypeNotSupportedException(
                f'The type of column {primary_key_column.key} ({column_type}) not supported yet')

        default = self._extra_default_value(primary_key_column)
        description = self._get_field_description(primary_key_column)
        if default is ...:
            warnings.warn(
                f'The column of {primary_key_column.key} has not default value '
                f'and it is not nullable and in exclude_list'
                f'it may throw error when you insert data ')
        primary_column_name = str(primary_key_column.key)
        primary_field_definitions = (primary_column_name, column_type, default)
        class_name = f'{self.class_name}PrimaryKeyModel'
        self.code_gen.build_dataclass(class_name=class_name,
                                      fields=[(primary_field_definitions[0],
                                               primary_field_definitions[1],
                                               f'Query({primary_field_definitions[2]}, description={description})')],
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        return primary_column_name

    def _extract_unique(self) -> List[str]:
        unique_constraint = None
        if not self.constraints:
            return []
        for constraint in self.constraints:
            if isinstance(constraint, UniqueConstraint):
                if unique_constraint:
                    raise SchemaException(
                        "Only support one unique constraint/ Use unique constraint and composite unique constraint "
                        "at same time is not supported / Use  composite unique constraint if there are more than one unique constraint")
                unique_constraint = constraint
        if unique_constraint:
            unique_column_name_list = []
            for constraint_column in unique_constraint.columns:
                column_name = str(constraint_column.key)
                unique_column_name = column_name
                unique_column_name_list.append(unique_column_name)
            return unique_column_name_list
        else:
            return []

    @staticmethod
    def _get_field_description(column: Column) -> str:
        if not hasattr(column, 'comment') or not column.comment:
            return None
        return f'"{column.comment}"'

    def _extract_all_field(self, columns=None) -> List[dict]:
        fields: List[dict] = []
        if not columns:
            columns = self.__columns
        elif isinstance(columns, DeclarativeMeta):
            columns = columns.__table__.c
        elif isinstance(columns, Table):
            columns = columns.c
        for column in columns:
            column_name = str(column.key)
            column_foreign = [i.target_fullname for i in column.foreign_keys]
            default = self._extra_default_value(column)
            if column_name in self._exclude_column:
                continue
            column_type = str(column.type)
            description = self._get_field_description(column)
            try:
                python_type = column.type.python_type
                if column_type in self.unsupported_data_types:
                    raise ColumnTypeNotSupportedException(
                        f'The type of column {column_name} ({column_type}) not supported yet')
                if column_type in self.partial_supported_data_types:
                    warnings.warn(
                        f'The type of column {column_name} ({column_type}) '
                        f'is not support data query (as a query parameters )')
            except NotImplementedError:
                raise ColumnTypeNotSupportedException(
                    f'The type of column {column_name} ({column_type}) not supported yet')
                # string filter
            python_type_str = deepcopy(python_type.__name__)
            if python_type_str in ['str']:
                self.str_type_columns.append(column_name)
            # uuid filter
            elif python_type_str in ['UUID']:
                self.uuid_type_columns.append(column.name)
                python_type_str = "uuid.UUID"
            # number filter
            elif python_type_str in ['int', 'float', 'Decimal']:
                self.number_type_columns.append(column_name)
            # date filter
            elif python_type_str in ['date', 'time', 'datetime']:
                self.datetime_type_columns.append(column_name)
            # timedelta filter
            elif python_type_str in ['timedelta']:
                self.timedelta_type_columns.append(column_name)
            # bool filter
            elif python_type_str in ['bool']:
                self.bool_type_columns.append(column_name)
            # json filter
            elif python_type_str in ['dict']:
                self.json_type_columns.append(column_name)
            # array filter
            elif python_type_str in ['list']:
                self.array_type_columns.append(column_name)
                base_column_detail, = column.base_columns
                if hasattr(base_column_detail.type, 'item_type'):
                    item_type = base_column_detail.type.item_type.python_type
                    fields.append({'column_name': column_name,
                                   'column_type': f"List[{item_type.__name__}]",
                                   'column_default': default,
                                   'column_description': description})
                    continue
            else:
                raise ColumnTypeNotSupportedException(
                    f'The type of column {column_name} ({column_type}) not supported yet')

            if column_type == "JSONB":
                fields.append({'column_name': column_name,
                               'column_type': f'Union[{python_type_str}, list]',
                               'column_default': default,
                               'column_description': description,
                               'column_foreign': column_foreign})
            else:
                fields.append({'column_name': column_name,
                               'column_type': python_type_str,
                               'column_default': default,
                               'column_description': description,
                               'column_foreign': column_foreign})

        return fields

    @staticmethod
    def _value_of_list_to_str(request_or_response_object, columns):
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

    @staticmethod
    def _get_many_order_by_columns_description_builder(all_columns, regex_validation, primary_name):
        return f'''<br> support column: 
            <br> {all_columns} <hr><br> support ordering:  
            <br> {list(map(str, Ordering))} 
            <hr> 
            <br/>example: 
            <br/>&emsp;&emsp;{primary_name}:ASC
            <br/>&emsp;&emsp;{primary_name}: DESC 
            <br/>&emsp;&emsp;{primary_name}    :    DESC
            <br/>&emsp;&emsp;{primary_name} (default sort by ASC)'''

    @staticmethod
    def _extra_default_value(column):
        if not column.nullable:
            if column.default is not None:
                default = column.default.arg
            elif column.server_default is not None:
                default = "None"
            elif column.primary_key and column.autoincrement == True:
                default = "None"
            else:
                default = "..."
        else:
            if column.default is not None:
                default = column.default.arg
            else:
                default = "None"
        return default

    def _assign_str_matching_pattern(self, field_of_param: dict, result_: List[dict]) -> List[dict]:
        if self.sql_type == SqlType.postgresql:
            operator = "List[PGSQLMatchingPatternInString]"
        else:
            operator = "List[MatchingPatternInStringBase]"

        for i in [
            {'column_name': field_of_param['column_name'] + ExtraFieldTypePrefix.Str + ExtraFieldType.Matching_pattern,
             'column_type': f'Optional[{operator}]',
             'column_default': f'[MatchingPatternInStringBase.case_sensitive]',
             'column_description': "None"},
            {'column_name': field_of_param['column_name'] + ExtraFieldTypePrefix.Str,
             'column_type': f'Optional[List[{field_of_param["column_type"]}]]',
             'column_default': "None",
             'column_description': field_of_param['column_description']}
        ]:
            result_.append(i)
        return result_

    @staticmethod
    def _assign_list_comparison(field_of_param, result_: List[dict]) -> List[dict]:
        for i in [
            {
                'column_name': field_of_param[
                                   'column_name'] + f'{ExtraFieldTypePrefix.List}{ExtraFieldType.Comparison_operator}',
                'column_type': 'Optional[ItemComparisonOperators]',
                'column_default': 'ItemComparisonOperators.In',
                'column_description': "None"},
            {'column_name': field_of_param['column_name'] + ExtraFieldTypePrefix.List,
             'column_type': f'Optional[List[{field_of_param["column_type"]}]]',
             'column_default': 'None',
             'column_description': field_of_param['column_description']}

        ]:
            result_.append(i)
        return result_

    @staticmethod
    def _assign_range_comparison(field_of_param, result_: List[dict]) -> List[dict]:
        for i in [
            {'column_name': field_of_param[
                                'column_name'] + f'{ExtraFieldTypePrefix.From}{ExtraFieldType.Comparison_operator}',
             'column_type': 'Optional[RangeFromComparisonOperators]',
             'column_default': 'RangeFromComparisonOperators.Greater_than_or_equal_to',
             'column_description': "None"},

            {'column_name': field_of_param[
                                'column_name'] + f'{ExtraFieldTypePrefix.To}{ExtraFieldType.Comparison_operator}',
             'column_type': 'Optional[RangeToComparisonOperators]',
             'column_default': 'RangeToComparisonOperators.Less_than.Less_than_or_equal_to',
             'column_description': "None"},
        ]:
            result_.append(i)

        for i in [
            {'column_name': field_of_param['column_name'] + ExtraFieldTypePrefix.From,
             'column_type': f'Optional[NewType(ExtraFieldTypePrefix.From, {field_of_param["column_type"]})]',
             'column_default': "None",
             'column_description': field_of_param['column_description']},

            {'column_name': field_of_param['column_name'] + ExtraFieldTypePrefix.To,
             'column_type': f'Optional[NewType(ExtraFieldTypePrefix.To, {field_of_param["column_type"]})]',
             'column_default': "None",
             'column_description': field_of_param['column_description']}
        ]:
            result_.append(i)
        return result_

    def _get_fizzy_query_param(self, exclude_column: List[str] = None, fields=None) -> List[dict]:
        if not fields:
            fields = self.all_field
        if not exclude_column:
            exclude_column = []
        fields_: List[dict] = deepcopy(fields)
        result = []
        for field_ in fields_:
            if field_['column_name'] in exclude_column:
                continue
            if "column_foreign" in field_ and field_['column_foreign']:
                jump = False
                for foreign in field_['column_foreign']:
                    if foreign in exclude_column:
                        jump = True
                if jump:
                    continue
            field_['column_default'] = None
            if field_['column_name'] in self.str_type_columns:
                result = self._assign_str_matching_pattern(field_, result)
                result = self._assign_list_comparison(field_, result)

            elif field_['column_name'] in self.uuid_type_columns or \
                    field_['column_name'] in self.bool_type_columns:
                result = self._assign_list_comparison(field_, result)

            elif field_['column_name'] in self.number_type_columns or \
                    field_['column_name'] in self.datetime_type_columns:
                result = self._assign_range_comparison(field_, result)
                result = self._assign_list_comparison(field_, result)

        return result

    def _assign_pagination_param(self, result_: List[tuple]) -> List[Union[Tuple, Dict]]:
        all_column_ = [i['column_name'] for i in self.all_field]

        regex_validation = "(?=(" + '|'.join(all_column_) + r")?\s?:?\s*?(?=(" + '|'.join(
            list(map(str, Ordering))) + r"))?)"
        columns_with_ordering = pydantic.constr(regex=regex_validation)

        for i in [
            ('limit', 'Optional[int]', "Query(None)"),
            ('offset', 'Optional[int]', "Query(None)"),
            ('order_by_columns', f'Optional[List[pydantic.constr(regex="{regex_validation}")]]',
             f'''Query(
                None,
                description="""{self._get_many_order_by_columns_description_builder(
                 all_columns=all_column_,
                 regex_validation=regex_validation,
                 primary_name='any name of column')}""")''')
        ]:
            result_.append(i)
        return result_

    def upsert_one(self) -> Tuple:
        request_validation = [lambda self_object: _filter_none(self_object)]
        request_fields = []
        response_fields = []

        # Create on_conflict Model
        all_column_ = [i['column_name'] for i in self.all_field]
        conflict_columns = ('update_columns',
                            "Optional[List[str]]",
                            f"Body({set(all_column_) - set(self.unique_fields)},description='update_columns should contain which columns you want to update when the unique columns got conflict')")

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertOneConflictModel",
                                      fields=[conflict_columns])
        on_conflict_handle = [('on_conflict', f"Optional[{self.class_name + 'UpsertOneConflictModel'}]",
                               "Body(None)")]

        # Create Request and Response Model
        all_field = deepcopy(self.all_field)
        for i in all_field:
            request_fields.append((i['column_name'],
                                   i['column_type'],
                                   f"Body({i['column_default']}, description={i['column_description']})"))
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertOneRequestBodyModel",
                                      fields=request_fields + on_conflict_handle,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertOneResponseModel",
                                      fields=response_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        return None, self.class_name + "UpsertOneRequestBodyModel", self.class_name + "UpsertOneResponseModel"

    def upsert_many(self) -> Tuple:
        insert_fields = []
        response_fields = []

        # Create on_conflict Model
        all_column_ = [i['column_name'] for i in self.all_field]
        conflict_columns = ('update_columns',
                            "Optional[List[str]]",
                            f"Body({set(all_column_) - set(self.unique_fields)},description='update_columns should contain which columns you want to update when the unique columns got conflict')")

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertManyConflictModel",
                                      fields=[conflict_columns])
        on_conflict_handle = [('on_conflict', f"Optional[{self.class_name + 'UpsertManyConflictModel'}]",
                               "Body(None)")]

        # Ready the Request and Response Model
        all_field = deepcopy(self.all_field)

        for i in all_field:
            insert_fields.append((i['column_name'],
                                  i['column_type'],
                                  f'field(default=Body({i["column_default"]}, description={i["column_description"]}))'))

            if i["column_default"] == "None":
                i["column_default"] = "..."
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f'Body({i["column_default"]}, description={i["column_description"]})'))

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertManyItemRequestBodyModel",
                                      fields=insert_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        insert_list_field = [('insert', f"List[{self.class_name + 'UpsertManyItemRequestBodyModel'}]", "Body(...)")]

        self.code_gen.build_dataclass(class_name=self.class_name + "UpsertManyItemListRequestBodyModel",
                                      fields=insert_list_field + on_conflict_handle,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True
                                      )

        self.code_gen.build_base_model(class_name=self.class_name + "UpsertManyItemResponseModel",
                                       fields=response_fields,
                                       value_of_list_to_str_columns=self.uuid_type_columns,
                                       filter_none=True)

        self.code_gen.build_base_model_root(class_name=self.class_name + "UpsertManyItemListResponseModel",
                                            field=(
                                                f'{f"{self.class_name}UpsertManyItemResponseModel"}',
                                                None))

        return None, self.class_name + "UpsertManyItemListRequestBodyModel", self.class_name + "UpsertManyItemListResponseModel"

    def create_one(self) -> Tuple:
        request_fields = []
        response_fields = []

        # Create Request and Response Model
        all_field = deepcopy(self.all_field)
        for i in all_field:
            request_fields.append((i['column_name'],
                                   i['column_type'],
                                   f'Body({i["column_default"]}, description={i["column_description"]})'))
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f'Body({i["column_default"]}, description={i["column_description"]})'))

        self.code_gen.build_dataclass(class_name=self.class_name + "CreateOneRequestBodyModel",
                                      fields=request_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        self.code_gen.build_base_model(class_name=self.class_name + "CreateOneResponseModel",
                                       fields=response_fields)

        return None, self.class_name + "CreateOneRequestBodyModel", self.class_name + "CreateOneResponseModel"

    def create_many(self) -> Tuple:
        insert_fields = []
        response_fields = []

        all_field = deepcopy(self.all_field)
        for i in all_field:
            insert_fields.append((i['column_name'],
                                  i['column_type'],
                                  f'field(default=Body({i["column_default"]}, description={i["column_description"]}))'))

            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f'Body({i["column_default"]}, description={i["column_description"]})'))

        self.code_gen.build_dataclass(class_name=self.class_name + "CreateManyItemRequestModel",
                                      fields=insert_fields)

        insert_list_field = [('insert', f"List[{self.class_name + 'CreateManyItemRequestModel'}]", "Body(...)")]

        self.code_gen.build_dataclass(class_name=self.class_name + "CreateManyItemListRequestModel",
                                      fields=insert_list_field,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        self.code_gen.build_base_model(class_name=self.class_name + "CreateManyItemResponseModel",
                                       fields=response_fields,
                                       orm_mode=True)

        self.code_gen.build_base_model_root(class_name=self.class_name + "CreateManyItemListResponseModel",
                                            field=(
                                                f'{f"{self.class_name}CreateManyItemResponseModel"}',
                                                None))

        return None, self.class_name + "CreateManyItemListRequestModel", self.class_name + "CreateManyItemListResponseModel"

    def find_many(self) -> Tuple:

        query_param: List[dict] = self._get_fizzy_query_param()
        query_param: List[Tuple] = self._assign_pagination_param(query_param)

        response_fields = []
        all_field = deepcopy(self.all_field)
        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    None))
        request_fields = []
        for i in query_param:
            assert isinstance(i, Tuple) or isinstance(i, dict)
            if isinstance(i, Tuple):
                request_fields.append(i)
            if isinstance(i, dict):
                request_fields.append((i['column_name'],
                                       i['column_type'],
                                       f'Query({i["column_default"]}, description={i["column_description"]})'))

        self.code_gen.build_dataclass(class_name=self.class_name + "FindManyRequestBodyModel", fields=request_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)
        self.code_gen.build_base_model(class_name=self.class_name + "FindManyResponseModel", fields=response_fields)

        self.code_gen.build_base_model_root(class_name=self.class_name + "FindManyItemListResponseModel",
                                            field=(
                                                f'{self.class_name + "FindManyResponseModel"}',
                                                None),
                                            base_model="ExcludeUnsetBaseModel")

        return self.class_name + "FindManyRequestBody", None, f'{self.class_name}FindManyItemListResponseModel'

    def find_one(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param(self.primary_key_str)
        response_fields = []
        all_field = deepcopy(self.all_field)

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f'Body({i["column_default"]})'))

        request_fields = []
        for i in query_param:
            assert isinstance(i, dict) or isinstance(i, tuple)
            if isinstance(i, Tuple):
                request_fields.append(i)
            else:
                request_fields.append((i['column_name'],
                                       i['column_type'],
                                       f'Query({i["column_default"]})'))
        self.code_gen.build_dataclass(class_name=self.class_name + "FindOneRequestBodyModel", fields=request_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)

        self.code_gen.build_base_model(class_name=self.class_name + "FindOneResponseModel", fields=response_fields)
        self.code_gen.build_base_model_root(class_name=self.class_name + "FindOneItemListResponseModel",
                                            field=(
                                                f'{self.class_name + "FindOneResponseModel"}',
                                                None),
                                            base_model="ExcludeUnsetBaseModel")

        return self.class_name + "PrimaryKeyModel", self.class_name + "FindOneRequestBodyModel", None, self.class_name + "FindOneItemListResponseModel", None

    def delete_one(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param(self.primary_key_str)
        response_fields = []
        all_field = deepcopy(self.all_field)
        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))

        request_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_fields.append((i['column_name'],
                                   i['column_type'],
                                   f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "DeleteOneRequestQueryModel",
                                      fields=request_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_base_model(class_name=self.class_name + "DeleteOneResponseModel",
                                       fields=response_fields)
        return self.class_name + "PrimaryKeyModel", self.class_name + "DeleteOneRequestQueryModel", None, self.class_name + "DeleteOneResponseModel"

    def delete_many(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param()
        response_fields = []
        all_field = deepcopy(self.all_field)
        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))

        request_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_fields.append((i['column_name'],
                                   i['column_type'],
                                   f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "DeleteManyRequestQueryModel",
                                      fields=request_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_base_model(class_name=self.class_name + "DeleteManyItemResponseModel",
                                       fields=response_fields)

        self.code_gen.build_base_model_root(class_name=self.class_name + "DeleteManyItemListResponseModel",
                                            field=(
                                                f'{self.class_name + "DeleteManyItemResponseModel"}',
                                                None))

        return None, self.class_name + "DeleteManyRequestQueryModel", None, self.class_name + "DeleteManyItemListResponseModel"

    def patch_one(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param(self.primary_key_str)

        response_fields = []
        all_field = deepcopy(self.all_field)
        request_body_fields = []

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))
            if i['column_name'] != self.primary_key_str:
                request_body_fields.append((i['column_name'],
                                            i['column_type'],
                                            f"Body(None, description={i['column_description']})"))

        request_query_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_query_fields.append((i['column_name'],
                                         i['column_type'],
                                         f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "PatchOneRequestQueryModel",
                                      fields=request_query_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_dataclass(class_name=self.class_name + "PatchOneRequestBodyModel",
                                      fields=request_body_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_base_model(class_name=self.class_name + "PatchOneResponseModel",
                                       fields=response_fields)

        return self.class_name + "PrimaryKeyModel", self.class_name + "PatchOneRequestQueryModel", self.class_name + "PatchOneRequestBodyModel", self.class_name + "PatchOneResponseModel"

    def update_one(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param(self.primary_key_str)

        response_fields = []
        all_field = deepcopy(self.all_field)
        request_body_fields = []

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))
            if i['column_name'] not in [self.primary_key_str]:
                request_body_fields.append((i['column_name'],
                                            i['column_type'],
                                            f"Body(..., description={i['column_description']})"))

        request_query_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_query_fields.append((i['column_name'],
                                         i['column_type'],
                                         f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "UpdateOneRequestQueryModel",
                                      fields=request_query_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        self.code_gen.build_dataclass(class_name=self.class_name + "UpdateOneRequestBodyModel",
                                      fields=request_body_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        # I have removed filter none and valuexxx for response model
        self.code_gen.build_base_model(class_name=self.class_name + "UpdateOneResponseModel",
                                       fields=response_fields)
        return self.class_name + "PrimaryKeyModel", self.class_name + "UpdateOneRequestQueryModel", self.class_name + "UpdateOneRequestBodyModel", self.class_name + "UpdateOneResponseModel"

    def update_many(self) -> Tuple:
        """
        In update many, it allow you update some columns into the same value in limit of a scope,
        you can get the limit of scope by using request query.
        And fill out the columns (except the primary key column and unique columns) you want to update
        and the update value in the request body

        The response will show you the update result
        :return: url param dataclass model
        """
        query_param: List[dict] = self._get_fizzy_query_param()

        response_fields = []
        all_field = deepcopy(self.all_field)
        request_body_fields = []

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))
            if i['column_name'] not in [self.primary_key_str]:
                request_body_fields.append((i['column_name'],
                                            i['column_type'],
                                            f"Body(..., description={i['column_description']})"))

        request_query_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_query_fields.append((i['column_name'],
                                         i['column_type'],
                                         f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "UpdateManyRequestQueryModel",
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      fields=request_query_fields,
                                      filter_none=True)
        self.code_gen.build_dataclass(class_name=self.class_name + "UpdateManyRequestBodyModel",
                                      fields=request_body_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=True)

        self.code_gen.build_base_model(class_name=self.class_name + "UpdateManyResponseItemModel",
                                       fields=response_fields)

        self.code_gen.build_base_model_root(class_name=self.class_name + "UpdateManyItemListResponseModel",
                                            field=(
                                                f'{self.class_name + "UpdateManyResponseItemModel"}',
                                                None))

        return None, self.class_name + "UpdateManyRequestQueryModel", self.class_name + "UpdateManyRequestBodyModel", f'{self.class_name}UpdateManyItemListResponseModel'

    def patch_many(self) -> Tuple:
        """
        In update many, it allow you update some columns into the same value in limit of a scope,
        you can get the limit of scope by using request query.
        And fill out the columns (except the primary key column and unique columns) you want to update
        and the update value in the request body

        The response will show you the update result
        :return: url param dataclass model
        """
        query_param: List[dict] = self._get_fizzy_query_param()

        response_fields = []
        all_field = deepcopy(self.all_field)
        request_body_fields = []

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f"Body({i['column_default']})"))
            if i['column_name'] not in [self.primary_key_str]:
                request_body_fields.append((i['column_name'],
                                            i['column_type'],
                                            f"Body(None, description={i['column_description']})"))

        request_query_fields = []
        for i in query_param:
            assert isinstance(i, dict)
            request_query_fields.append((i['column_name'],
                                         i['column_type'],
                                         f"Query({i['column_default']}, description={i['column_description']})"))

        self.code_gen.build_dataclass(class_name=self.class_name + "PatchManyRequestQueryModel",
                                      fields=request_query_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_dataclass(class_name=self.class_name + "PatchManyRequestBodyModel",
                                      fields=request_body_fields,
                                      filter_none=True,
                                      value_of_list_to_str_columns=self.uuid_type_columns)

        self.code_gen.build_base_model(class_name=self.class_name + "PatchManyItemResponseModel",
                                       fields=response_fields)

        self.code_gen.build_base_model_root(class_name=f'{self.class_name}PatchManyItemListResponseModel',
                                            field=(
                                                f'{f"{self.class_name}PatchManyItemResponseModel"}',
                                                None))
        return None, self.class_name + "PatchManyRequestQueryModel", self.class_name + "PatchManyRequestBodyModel", f'{self.class_name}PatchManyItemListResponseModel'

    def post_redirect_get(self) -> Tuple:
        request_validation = [lambda self_object: _filter_none(self_object)]
        request_body_fields = []
        response_body_fields = []

        # Create Request and Response Model
        all_field = deepcopy(self.all_field)
        for i in all_field:
            request_body_fields.append((i['column_name'],
                                        i['column_type'],
                                        f'Body({i["column_default"]}, description={i["column_description"]})'))
            response_body_fields.append((i['column_name'],
                                         i['column_type'],
                                         f'Body({i["column_default"]}, description={i["column_description"]})'))

        # Ready the uuid to str validator
        if self.uuid_type_columns:
            request_validation.append(lambda self_object: self._value_of_list_to_str(self_object,
                                                                                     self.uuid_type_columns))
        self.code_gen.build_dataclass(class_name=self.class_name + "PostAndRedirectRequestModel",
                                      fields=request_body_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns)
        self.code_gen.build_base_model(class_name=self.class_name + "PostAndRedirectResponseModel",
                                       fields=response_body_fields,
                                       value_of_list_to_str_columns=self.uuid_type_columns)
        return None, self.class_name + "PostAndRedirectRequestModel", self.class_name + "PostAndRedirectResponseModel"
