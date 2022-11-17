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

from pydantic import (BaseModel)
from sqlalchemy import UniqueConstraint, Table, Column, inspect
from sqlalchemy.orm import decl_api

from .is_table import is_table
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
DeclarativeClassT = NewType('DeclarativeClassT', decl_api.DeclarativeMeta)
TableNameT = NewType('TableNameT', str)
ResponseModelT = NewType('ResponseModelT', BaseModel)
ForeignKeyName = NewType('ForeignKeyName', str)
TableInstance = NewType('TableInstance', Table)


class ApiParameterSchemaBuilder:
    unsupported_data_types = ["BLOB"]
    partial_supported_data_types = ["INTERVAL", "JSON", "JSONB"]

    def __init__(self,
                 db_model: decl_api.DeclarativeMeta,
                 sql_type: str,
                 foreign_include: List[decl_api.DeclarativeMeta],
                 exclude_column: Optional[List[str]] = [],
                 constraints=None):
        self.class_name = db_model.__name__
        self.root_table_name = get_table_name(db_model)
        self.constraints = constraints
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
        self.all_field: List[dict] = self._extract_all_field()
        self.primary_key_str = self._extract_primary()
        self.unique_fields: List[str] = self._extract_unique()
        self.code_gen.build_constant(constants=[("PRIMARY_KEY_NAME", self.primary_key_str),
                                                ("UNIQUE_LIST", self.unique_fields)])
        self.sql_type = sql_type

        # relationship api related variable
        self.foreign_table_response_model_sets: Dict[dict] = {}

        self.foreign_include = foreign_include

        self.foreign_mapper = self._foreign_mapper_builder()
        self.relation_level = self._extra_relation_level()
        # find many foreign base
        self.table_of_foreign, self.reference_mapper = self._extra_foreign_find_table_from_declarative_base(
            self.__db_model)
        self.foreign_join_common_column: Union[dict, None] = self._assign_foreign_join()

    def _foreign_mapper_builder(self):
        foreign_mapper = {}

        for db_model in self.foreign_include:
            if is_table(db_model):
                raise RuntimeError("only support declarative from Sqlalchemy, you can try to give the table a fake pk"
                                   " to work around")
            tmp = {}
            table_name = get_table_name(db_model)
            tmp["model"] = db_model
            foreign_mapper[table_name] = db_model
            tmp["db_model"] = db_model
            tmp["db_model_table"] = db_model.__table__
            tmp["db_name"] = db_model.__tablename__
            tmp["columns"] = db_model.__table__.c
            tmp["all_fields"] = self._extract_all_field(tmp["columns"])
            tmp["primary_key"] = self._extract_primary(tmp["db_model_table"], gen_model=False)
            foreign_mapper[table_name] = tmp
        return foreign_mapper

    def _extra_relation_level(self, model: Table = None, processed_table: list = None):
        if model is None:
            model = self.__db_model
        if processed_table is None:
            processed_table = []
        mapper = inspect(model)
        relation_level = []
        for r in mapper.relationships:

            target_table = r.target
            target_table_name = str(target_table.fullname)
            if target_table_name and target_table_name not in processed_table and target_table_name in self.foreign_mapper:
                processed_table.append(str(mapper.local_table))
                if self.foreign_mapper[target_table_name]["db_name"] not in relation_level:
                    relation_level.append(self.foreign_mapper[target_table_name]["db_name"])
                relation_level += self._extra_relation_level(self.foreign_mapper[target_table_name]["db_model"],
                                                             processed_table=processed_table
                                                             )
        return relation_level

    def _extra_foreign_find_table_from_declarative_base(self, db_model: decl_api.DeclarativeMeta,
                                                        is_foreign_tree: bool = False,
                                                        mirror_relationship: bool = False):
        mapper = inspect(db_model)
        foreign_key_table = {}
        reference_mapper = {}
        for r in mapper.relationships:
            local, = r.local_columns
            local = mapper.get_property_by_column(local).expression
            local_table = str(local).split('.')[0]
            local_column = str(local).split('.')[1]
            local_table_instance = local.table

            foreign_table = r.mapper.class_
            foreign_table_name = foreign_table.__tablename__

            if mirror_relationship and (local_table not in self.foreign_mapper or foreign_table_name != self.db_name):
                continue
            if not mirror_relationship and foreign_table_name not in self.foreign_mapper:
                continue

            foreign_secondary_table_name = ''
            if r.secondary_synchronize_pairs:
                # foreign_table_name = r.secondary.key
                foreign_secondary_table_name = str(r.secondary.key)

            local_reference_pairs = []
            for i in r.synchronize_pairs:
                for column in i:
                    table_name_ = str(column).split('.')[0]
                    column_name_ = str(column).split('.')[1]
                    if table_name_ not in [foreign_secondary_table_name, foreign_table_name]:
                        continue

                    reference_table = table_name_
                    reference_column = column_name_
                    reference_table_instance = column.table
                    if r.secondary_synchronize_pairs:

                        exclude = True
                    else:

                        reference_mapper[local_column] = {"foreign_table": foreign_table,
                                                          "foreign_table_name": foreign_table_name}
                        exclude = False
                    local_reference_pairs.append({'local': {"local_table": local_table,
                                                            "local_column": local_column},
                                                  "reference": {"reference_table": reference_table,
                                                                "reference_column": reference_column},
                                                  'local_table': local_table_instance,
                                                  'local_table_columns': local_table_instance.c,
                                                  'reference_table': reference_table_instance,
                                                  'reference_table_columns': reference_table_instance.c,
                                                  'exclude': exclude})
            for i in r.secondary_synchronize_pairs:
                local_table_: str = None
                local_column_: str = None
                reference_table_: str = None
                reference_column_: str = None
                local_table_instance_: Table = None
                reference_table_instance_: Table = None
                for column in i:

                    table_name_ = str(column).split('.')[0]
                    column_name_ = str(column).split('.')[1]
                    if table_name_ == foreign_secondary_table_name:
                        local_table_ = str(column).split('.')[0]
                        local_column_ = str(column).split('.')[1]
                        local_table_instance_ = column.table
                    if table_name_ == foreign_table_name:
                        reference_table_ = str(column).split('.')[0]
                        reference_column_ = str(column).split('.')[1]
                        reference_table_instance_ = column.table

                reference_mapper[local_column_] = {"foreign_table": foreign_table,
                                                   "foreign_table_name": foreign_table_name}
                local_reference_pairs.append({'local': {"local_table": local_table_,
                                                        "local_column": local_column_},
                                              "reference": {"reference_table": reference_table_,
                                                            "reference_column": reference_column_},
                                              'local_table': local_table_instance_,
                                              'local_table_columns': local_table_instance_.c,
                                              'reference_table': reference_table_instance_,
                                              'reference_table_columns': reference_table_instance_.c,
                                              'exclude': False})

            all_fields_ = self._extract_all_field(foreign_table.__table__.c)
            response_fields = []
            for i in all_fields_:
                response_fields.append((i['column_name'],
                                        i['column_type'],
                                        None))
            if is_foreign_tree:
                response_model_name = "FindManyForeignTreeResponseModel"
            else:
                response_model_name = "FindManyResponseModel"
            self.code_gen.build_base_model(
                class_name=db_model.__name__ + "To" + foreign_table.__name__ + response_model_name,
                fields=response_fields)

            self.foreign_table_response_model_sets[
                foreign_table] = {"class_name": db_model.__name__ + "To" + foreign_table.__name__ + response_model_name,
                                  "is_foreign_tree": is_foreign_tree}
            foreign_key_table[foreign_table_name] = {'local_reference_pairs_set': local_reference_pairs,
                                                     'fields': all_fields_,
                                                     'instance': foreign_table,
                                                     'db_column': foreign_table}
        return foreign_key_table, reference_mapper

    def _extract_primary(self, db_model_table: Table = None, gen_model: bool = True) -> Union[
        tuple, Tuple[Union[str, Any],
                     DataClassT,
                     Tuple[Union[
                               str, Any],
                           Union[Type[
                                     uuid.UUID], Any],
                           Optional[
                               Any]]]]:
        if db_model_table is None:
            db_model_table = self.__db_model_table
        primary_list = db_model_table.primary_key.columns.values()
        if len(primary_list) > 1:
            raise SchemaException(
                f'multiple primary key / or composite not supported; {self.db_name} ')
        primary_key_column, = primary_list
        column_type = str(primary_key_column.type)
        try:
            python_type = primary_key_column.type.python_type
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
                                    'datetime',
                                    'timedelta']:
            column_type = python_type.__name__
        elif python_type.__name__ in ['UUID']:
            column_type = "uuid.UUID"
        else:
            raise ColumnTypeNotSupportedException(
                f'The type of column {primary_key_column.key} ({column_type}) is not supported as pk yet')

        default = self._extra_default_value(primary_key_column)
        description = self._get_field_description(primary_key_column)
        if default == "...":
            warnings.warn(
                f'The column of {primary_key_column.key} has not default value '
                f'and it is not nullable and in exclude_list'
                f'it may throw error when you insert data ')
        primary_column_name = str(primary_key_column.key)
        primary_field_definitions = (primary_column_name, column_type, default, description)
        class_name = f'{self.class_name}PrimaryKeyModel'
        if gen_model:
            self.code_gen.build_dataclass(class_name=class_name,
                                          fields=[(primary_field_definitions[0],
                                                   primary_field_definitions[1],
                                                   f'Query({primary_field_definitions[2]}, description={primary_field_definitions[3]})')],
                                          value_of_list_to_str_columns=self.uuid_type_columns)

        return primary_column_name

    def _extract_unique(self) -> List[str]:
        unique_constraint = None
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
    def _get_many_order_by_columns_description_builder(all_columns: str, primary_name: str) -> str:
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
    def _extra_default_value(column: Column) -> str:
        if not column.nullable:
            if column.default is not None:
                default = column.default.arg
            elif column.server_default is not None:
                default = "None"
            elif column.primary_key and column.autoincrement is True:
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
             'column_default': '[MatchingPatternInStringBase.case_sensitive]',
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

        for i in [
            ('limit', 'Optional[int]', "Query(None)"),
            ('offset', 'Optional[int]', "Query(None)"),
            ('order_by_columns', f'Optional[List[pydantic.constr(regex="{regex_validation}")]]',
             f'''Query(
                None,
                description="""{self._get_many_order_by_columns_description_builder(
                 all_columns=all_column_,
                 primary_name='any name of column')}""")''')
        ]:
            result_.append(i)
        return result_

    def _assign_foreign_join(self, table_of_foreign=None, model_name=None) -> List[Union[Tuple, Dict]]:
        if table_of_foreign is None:
            table_of_foreign = self.table_of_foreign
        if model_name is None:
            model_name = self.class_name + 'Relationship'
        else:
            model_name += 'Relationship'
        if table_of_foreign:
            self.code_gen.build_enum(class_name=model_name,
                                     fields=[(table_name, f"'{table_name}'") for table_name in table_of_foreign])

            return {"column_name": 'relationship', "column_type": f"Optional[List[{model_name}]]",
                    "column_default": "None", "column_description": "'try to query the other table with foreign key'"}
        return None

    def _extra_relation_primary_key(self, relation_dbs, default_class_name=None):
        if default_class_name is None:
            default_class_name = self.class_name
        primary_key_columns = []
        foreign_table_name = ""
        primary_column_names = []
        for db_model_table in relation_dbs:
            table_name = db_model_table.key
            foreign_table_name += table_name + "_"
            primary_list = db_model_table.primary_key.columns.values()
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
                if column_type == "UUID":
                    python_type = uuid.UUID
                else:
                    raise ColumnTypeNotSupportedException(
                        f'The type of column {primary_key_column.key} ({column_type}) not supported yet')
            # handle if python type is UUID
            if python_type.__name__ in ['str',
                                        'int',
                                        'float',
                                        'Decimal',
                                        'UUID',
                                        'bool',
                                        'date',
                                        'time',
                                        'datetime']:
                column_type = python_type.__name__
            else:
                raise ColumnTypeNotSupportedException(
                    f'The type of column {primary_key_column.key} ({column_type}) not supported yet')
            default = self._extra_default_value(primary_key_column)
            if default is ...:
                warnings.warn(
                    f'The column of {primary_key_column.key} has not default value '
                    f'and it is not nullable and in exclude_list'
                    f'it may throw error when you insert data ')
            description = self._get_field_description(primary_key_column)
            primary_column_name = str(primary_key_column.key)
            alias_primary_column_name = table_name + FOREIGN_PATH_PARAM_KEYWORD + str(primary_key_column.key)
            primary_column_names.append(alias_primary_column_name)
            primary_key_columns.append(
                (alias_primary_column_name, column_type, default, description))

        # TODO test foreign uuid key
        class_name = f'{default_class_name}RelationshipPrimaryKeyModel'
        self.code_gen.build_dataclass(class_name=class_name,
                                      fields=[(primary_key_column[0],
                                               primary_key_column[1],
                                               f"Query({primary_key_column[2]}, description={primary_key_column[3]})"
                                               ) for primary_key_column in primary_key_columns],
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=self.uuid_type_columns)

        return primary_column_names, f"{foreign_table_name}_PrimaryKeyModel", primary_key_columns

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

        return None, \
               self.class_name + "CreateOneRequestBodyModel", \
               self.class_name + "CreateOneResponseModel"

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

        return None, \
               self.class_name + "CreateManyItemListRequestModel", \
               self.class_name + "CreateManyItemListResponseModel"

    def foreign_tree_get_many(self) -> Tuple:
        _tmp = []
        path = ""
        path += '/{' + self.db_name + FOREIGN_PATH_PARAM_KEYWORD + self.primary_key_str + '}'
        path_model = [self.__db_model_table]
        pk_list = [self.db_name + "." + self.primary_key_str]
        total_table_of_foreign = {}
        function_name = "get_many_by_pk_from"
        class_name = self.__db_model.__name__
        for idx, relation in enumerate(self.relation_level):
            table_detail = self.foreign_mapper[relation]
            _all_fields = table_detail["all_fields"]
            _primary_key = table_detail["primary_key"]
            _db_name = table_detail["db_name"]
            _db_model = table_detail["db_model"]
            _db_model_table = table_detail["db_model_table"]
            class_name += "To" + _db_model.__name__

            _primary_key_dataclass_model = self._extra_relation_primary_key(path_model, class_name)
            path_model.append(_db_model_table)
            _query_param: List[dict] = self._get_fizzy_query_param(pk_list, _all_fields)
            table_of_foreign, reference_mapper = self._extra_foreign_find_table_from_declarative_base(_db_model,
                                                                                                      is_foreign_tree=True,
                                                                                                      mirror_relationship=True)
            total_table_of_foreign.update(table_of_foreign)

            foreign_join_common_column: Union[dict, None] = self._assign_foreign_join(table_of_foreign,
                                                                                      model_name=_db_model.__name__)
            if foreign_join_common_column is not None:
                _query_param += [foreign_join_common_column]
            response_fields = []
            all_field = deepcopy(_all_fields)
            path += '/' + _db_name + ''
            function_name += "_/_" + _db_name
            pk_list.append(_db_name + "." + _primary_key)

            for i in all_field:
                response_fields.append((i['column_name'],
                                        i['column_type'],
                                        f"Body({i['column_default']})"))

            request_fields = []
            for i in _query_param:
                assert isinstance(i, dict) or isinstance(i, tuple)
                if isinstance(i, Tuple):
                    request_fields.append(i)
                else:
                    request_fields.append((i['column_name'],
                                           i['column_type'],
                                           f"Query({i['column_default']}, description={i['column_description']})"))

            for local_column, refer_table_info in reference_mapper.items():
                response_fields.append((f"{refer_table_info['foreign_table_name']}_foreign",
                                        self.foreign_table_response_model_sets[refer_table_info['foreign_table']][
                                            "class_name"],
                                        None))

            self.code_gen.build_dataclass(class_name=class_name + "FindManyForeignTreeRequestBody",
                                          fields=request_fields,
                                          value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)

            self.code_gen.build_base_model(class_name=class_name + "FindManyForeignTreeResponseModel",
                                           fields=response_fields,
                                           value_of_list_to_str_columns=self.uuid_type_columns)

            self.code_gen.build_base_model_paginate(
                class_name=class_name + "FindManyForeignTreeItemListResponseModel",
                field=(
                    f'{class_name + "FindManyForeignTreeResponseModel"}',
                    None),
                base_model="ExcludeUnsetBaseModel")

            _response_model = {}
            _response_model["primary_key_dataclass_model"] = _primary_key_dataclass_model[1]
            _response_model["request_query_model"] = class_name + "FindManyForeignTreeRequestBody"
            _response_model["response_model"] = class_name + "FindManyForeignTreeItemListResponseModel"
            _response_model["path"] = path
            _response_model['class_name'] = class_name
            _response_model["function_name"] = function_name
            _tmp.append(_response_model)
            path += '/{' + _db_name + FOREIGN_PATH_PARAM_KEYWORD + _primary_key + '}'

        return _tmp

    def find_many(self) -> Tuple:

        query_param: List[dict] = self._get_fizzy_query_param()
        query_param: List[Tuple] = self._assign_pagination_param(query_param)
        if self.foreign_join_common_column is not None:
            query_param.append(self.foreign_join_common_column)

        response_fields = []
        all_field = deepcopy(self.all_field)
        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    None))
        if self.foreign_table_response_model_sets:
            response_fields.append((
                "relationship",
                f"Dict[str, List[Union[{', '.join([foreign_info_dict['class_name'] for foreign_info_dict in self.foreign_table_response_model_sets.values() if foreign_info_dict['is_foreign_tree'] is not True])}]]]",
                None
            ))
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

        self.code_gen.build_base_model_paginate(class_name=self.class_name + "FindManyItemListResponseModel",
                                                field=(
                                                    f'{self.class_name + "FindManyResponseModel"}',
                                                    None),
                                                base_model="ExcludeUnsetBaseModel")

        return self.class_name + "FindManyRequestBody", \
               None, \
               f'{self.class_name}FindManyItemListResponseModel'

    def find_one(self) -> Tuple:
        query_param: List[dict] = self._get_fizzy_query_param(self.primary_key_str)
        if self.foreign_join_common_column is not None:
            query_param.append(self.foreign_join_common_column)

        response_fields = []
        all_field = deepcopy(self.all_field)

        for i in all_field:
            response_fields.append((i['column_name'],
                                    i['column_type'],
                                    f'Body({i["column_default"]})'))
        if self.foreign_table_response_model_sets:
            response_fields.append((
                "relationship",
                f"Dict[str, List[Union[{', '.join([foreign_info_dict['class_name'] for foreign_info_dict in self.foreign_table_response_model_sets.values() if foreign_info_dict['is_foreign_tree'] is not True])}]]]",
                None
            ))
        request_fields = []
        for i in query_param:
            assert isinstance(i, dict) or isinstance(i, tuple)
            # TODO add description
            request_fields.append((i['column_name'],
                                   i['column_type'],
                                   f'Query({i["column_default"]}, description={i["column_description"]})'))
        self.code_gen.build_dataclass(class_name=self.class_name + "FindOneRequestBodyModel", fields=request_fields,
                                      value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)

        self.code_gen.build_base_model(class_name=self.class_name + "FindOneResponseModel", fields=response_fields)
        self.code_gen.build_base_model_root(class_name=self.class_name + "FindOneItemListResponseModel",
                                            field=(
                                                f'{self.class_name + "FindOneResponseModel"}',
                                                None),
                                            base_model="ExcludeUnsetBaseModel")

        return self.class_name + "PrimaryKeyModel", \
               self.class_name + "FindOneRequestBodyModel", \
               None, \
               self.class_name + "FindOneItemListResponseModel", None

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
        return self.class_name + "PrimaryKeyModel", \
               self.class_name + "DeleteOneRequestQueryModel", \
               None, \
               self.class_name + "DeleteOneResponseModel"

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

        return None, self.class_name + "DeleteManyRequestQueryModel", \
               None, \
               self.class_name + "DeleteManyItemListResponseModel"

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

        return self.class_name + "PrimaryKeyModel", \
               self.class_name + "PatchOneRequestQueryModel", \
               self.class_name + "PatchOneRequestBodyModel", \
               self.class_name + "PatchOneResponseModel"

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
        return self.class_name + "PrimaryKeyModel", \
               self.class_name + "UpdateOneRequestQueryModel", \
               self.class_name + "UpdateOneRequestBodyModel", \
               self.class_name + "UpdateOneResponseModel"

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

        return None, self.class_name + "UpdateManyRequestQueryModel", \
               self.class_name + "UpdateManyRequestBodyModel", \
               f'{self.class_name}UpdateManyItemListResponseModel'

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
        return None, self.class_name + "PatchManyRequestQueryModel", \
               self.class_name + "PatchManyRequestBodyModel", \
               f'{self.class_name}PatchManyItemListResponseModel'
