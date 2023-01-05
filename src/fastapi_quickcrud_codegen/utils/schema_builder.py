import re
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
    """
        The ApiParameterSchemaBuilder class provides a way to generate Pydantic models from SQLAlchemy declarative models.
        This can be useful for generating REST API endpoints based on the schema of a database.

        Parameters:
        -----------
        db_model: decl_api.DeclarativeMeta
            The SQLAlchemy declarative model to generate the Pydantic model from.
        sql_type: str
            The SQL database type. This is used to determine how to map SQL data types to Pydantic data types.
        foreign_include: List[decl_api.DeclarativeMeta]
            A list of additional SQLAlchemy declarative models to include in the generated Pydantic model. These models
            are used to define the relationships between the main `db_model` and the other models.
        exclude_column: Optional[List[str]]
            A list of columns in the `db_model` to exclude from the generated Pydantic model.
        constraints: Optional[Any]
            Additional constraints to apply to the generated Pydantic model.
    """
    unsupported_data_types = ["BLOB"]
    partial_supported_data_types = ["INTERVAL", "JSON", "JSONB"]

    def __init__(self,
                 db_model: decl_api.DeclarativeMeta,
                 sql_type: str,
                 foreign_include: List[decl_api.DeclarativeMeta],
                 exclude_column: Optional[List[str]] = None,
                 constraints=None):
        self.class_name = db_model.__name__
        self.root_table_name = get_table_name(db_model)
        self.constraints = constraints
        if exclude_column is None:
            exclude_column = []
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
        self.foreign_table_response_model_sets_get_many: Dict[dict] = {}
        self.foreign_table_response_model_sets_get_one: Dict[dict] = {}
        self.relationship_list = []

        self.foreign_include = foreign_include

        self.foreign_mapper = self._foreign_mapper_builder()
        self.relation_level = self._extra_relation_level()
        self.foreign_tree: dict = self._extra_foreign_tree()
        # find many foreign base
        self.table_of_foreign, self.reference_mapper = self._extra_foreign_find_table_from_declarative_base(
            self.__db_model)
        self.foreign_join_common_column: Union[dict, None] = self._assign_foreign_join()


    def _foreign_mapper_builder(self) -> Dict[str, Dict[str, Any]]:
        """
        Builds a dictionary mapping table names to the information about their columns, primary keys, all fields etc....
        This dictionary is used to generate the models for the tables, and is also used to build the foreign key mappings.

        Returns:
            A dictionary mapping table names to their columns, primary keys, all fields etc....
        """
        foreign_mapper = {}

        for db_model in [*self.foreign_include + [self.__db_model]]:
            if is_table(db_model):
                raise RuntimeError("only support declarative from Sqlalchemy, you can try to give the table a fake pk"
                                   " to work around")
            tmp = {}
            table_name = get_table_name(db_model)
            tmp["model"] = db_model
            tmp["db_model"] = db_model
            tmp["db_model_table"] = db_model.__table__
            tmp["db_name"] = db_model.__tablename__
            tmp["columns"] = db_model.__table__.c
            tmp["all_fields"] = self._extract_all_field(tmp["columns"])
            tmp["primary_key"] = self._extract_primary(tmp["db_model_table"], gen_model=False)
            foreign_mapper[table_name] = tmp
        return foreign_mapper

    def _extra_relation_level(self, model: Optional[Table] = None, processed_table: Optional[List[str]] = None) -> List[
        str]:
        """
            This method is used to calculate the relation level of the given model.
            The relation level is a list of table names in the relationship hierarchy of the model.

            :param model: The model for which the relation level is to be calculated.
            :param processed_table: The list of tables that have already been processed.
            :return: The relation level of the given model.
        """
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

        return relation_level

    def __assign_local_reference_pairs_set(self, target_table_name: str, foreign_tree: Dict) -> Dict:
        """Assign a local reference pairs set to a given foreign table.


        :param target_table_name: The name of the target table.
        :param foreign_tree: A dictionary containing information about the foreign tree.
        :return: The updated foreign tree with the local reference pairs set assigned.
        """
        table_of_foreign, _ = self._extra_foreign_find_table_from_declarative_base(
            self.foreign_mapper[target_table_name]["db_model"],
            is_gen_code=True)
        tmp_foreign = []
        for foreign_dict in foreign_tree["foreign"]:
            foreign_table_name = foreign_dict["table_name"]
            if foreign_table_name in table_of_foreign:
                foreign_info_dict = table_of_foreign[foreign_table_name]
                foreign_dict['local_reference_pairs_set'] = foreign_info_dict
                tmp_foreign.append(foreign_dict)
        foreign_tree["foreign"] = tmp_foreign
        return foreign_tree

    def _extra_foreign_tree(self, model: Table = None, prev: dict = None):
        if model is None:
            model = self.__db_model
        mapper = inspect(model)
        foreign_tree = {"table_name": model.__tablename__, "model": model, "foreign": [],
                        'local_reference_pairs_set': {}}
        relationships = mapper.relationships
        for r in relationships:
            target_table = r.target
            target_table_name = str(target_table.fullname)
            if target_table_name and (target_table_name in self.foreign_mapper):
                target = self.foreign_mapper[target_table_name]
                if target["db_name"] != foreign_tree["table_name"]:
                    if prev is not None and target_table_name not in prev["foreign"]:
                        foreign_tree["foreign"].append(
                            {"table_name": target_table_name, "model": target["model"], "foreign": []})
                    else:
                        tmp_foreign_tree = self._extra_foreign_tree(self.foreign_mapper[target_table_name]["db_model"],
                                                                    foreign_tree)
                        # tmp_foreign_tree = self.__assign_local_reference_pairs_set(target_table_name, tmp_foreign_tree)
                        foreign_tree["foreign"].append(tmp_foreign_tree)
                else:
                    continue
            else:
                continue
        foreign_tree = self.__assign_local_reference_pairs_set(model.__tablename__, foreign_tree)
        return foreign_tree

    def _extra_foreign_find_table_from_declarative_base(self, db_model: decl_api.DeclarativeMeta,
                                                        is_foreign_tree: bool = False, is_get_many: bool = True,
                                                        is_gen_code: bool = False):
        """
        This function searches for foreign keys in a SQLAlchemy declarative model and returns a dictionary with information about the foreign keys.

        :param db_model: The SQLAlchemy declarative model to search for foreign keys in.
        :param is_foreign_tree: Whether to reverse the order of the foreign key search.
        :return: A tuple containing two dictionaries. The first dictionary contains information about the foreign keys found, and the second dictionary contains information about the relationships between the keys.
        """
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

            foreign_secondary_table_name = ''
            if r.secondary_synchronize_pairs:
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
                if is_get_many is True:
                    response_model_name = "FindManyForeignTreeResponseModel"
                else:
                    response_model_name = "FindOneForeignTreeResponseModel"

            else:
                if is_get_many is True:
                    response_model_name = "FindManyResponseModel"
                else:
                    response_model_name = "FindOneResponseModel"
            class_name = db_model.__name__ + "To" + foreign_table.__name__ + response_model_name

            if is_gen_code is True:
                self.code_gen.build_base_model(
                    class_name=class_name,
                    forbid=True,
                    fields=response_fields)

            if is_get_many is True and foreign_table not in self.foreign_table_response_model_sets_get_many:
                self.foreign_table_response_model_sets_get_many[
                    foreign_table] = {"class_name": class_name,
                                      "is_foreign_tree": is_foreign_tree}

            if is_get_many is False and foreign_table not in self.foreign_table_response_model_sets_get_one:
                self.foreign_table_response_model_sets_get_one[
                    foreign_table] = {"class_name": class_name,
                                      "is_foreign_tree": is_foreign_tree}

            foreign_key_table[foreign_table_name] = {'local_reference_pairs_set': local_reference_pairs,
                                                     'fields': all_fields_,
                                                     'instance': foreign_table,
                                                     'db_column': foreign_table.__table__.c}
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
        """
        Extract the primary key from the given `db_model_table` table and
        generate model for it if `gen_model` is set to True.

        :param db_model_table: The table to extract the primary key from.
        :param gen_model: Whether to generate model for the primary key or not.
        :return: The primary key as tuple along with its data class and field definitions.
        """
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
        """
        Extract the unique constraint from the table.

        :return: a list of unique column names
        """
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
    def _get_field_description(column: Column) -> Optional[str]:
        """
        Extracts the description of a column from its `comment` attribute.

        :param column: A SQLAlchemy Column instance.
        :return: A string containing the column's description, or None if no description is available.
        """
        if not hasattr(column, 'comment') or not column.comment:
            return None
        return f'"{column.comment}"'

    def _extract_all_field(self, columns: Optional[List[Column]] = None) -> List[Dict[str, Any]]:
        """
        Extracts field information from the provided list of columns.

        :param columns: A list of columns from which to extract field information.
        :return: A list of dictionaries containing field information.
        """
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
        """
        Get the default value for the given column.

        :param column: The SQLAlchemy column for which to get the default value.
        :return: The default value for the given column.
        """
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
        """
        :param field_of_param: a dict containing the column name, type, default value, and description for the field
        :param result_: a list of dicts containing the information for all fields
        :return: a list of dicts containing the information for all fields, including the new fields added by this method
            """
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
    def _assign_list_comparison(field_of_param: dict, result_: List[dict]) -> List[dict]:
        """
        This method adds comparison operator and list fields to the result list.

        :param field_of_param: A dictionary containing the name, type, default value, and description of a column.
        :param result_: A list of dictionaries representing the fields in the table.
        :return: The updated list of dictionaries representing the fields in the table.
        """
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
    def _assign_range_comparison(field_of_param: dict, result_: List[dict]) -> List[dict]:
        """
        Assign range comparison operators to the given field of parameter.

        :param field_of_param: The field of parameter to which the range comparison operators will be assigned.
        :param result_: The list of parameters to which the new fields will be added.
        :return: The updated list of parameters with the added range comparison operators.
        """
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

    def _get_fizzy_query_param(self, exclude_column: List[str] = None, fields: List[dict] = None) -> List[dict]:
        """
        :param exclude_column: a list of column names to exclude from the generated query parameters
        :param fields: a list of field dictionaries to use to generate the query parameters
        :return: a list of dictionaries representing the generated query parameters
        """
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

    def _assign_pagination_param(self, result_: List[tuple], all_field = None) -> List[Union[Tuple, Dict]]:
        if not all_field:
            all_field = self.all_field
        all_column_ = [i['column_name'] for i in all_field]

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

    def _assign_foreign_join(self,
                             table_of_foreign: dict = None,
                             model_name: str = None,
                             is_foreign_tree: bool = False) -> List[
        Union[Tuple, Dict]]:
        if table_of_foreign is None:
            table_of_foreign = self.table_of_foreign
        if model_name is None:
            model_name = self.class_name + 'Relationship'
        else:
            model_name = self.class_name+model_name+'Relationship'
        if not table_of_foreign:
            return None
        if model_name not in self.relationship_list:
            self.code_gen.build_enum(class_name=model_name,
                                     fields=[(table_name, f"'{table_name}'") for table_name in table_of_foreign])
            self.relationship_list.append(model_name)

        if is_foreign_tree:
            return {"column_name": 'relationship', "column_type": f"Optional[List[{model_name}]]",
                    "column_default": f"None",
                    "column_description": "'try to query the other table with foreign key'",
                    "include_in_schema": True}
        else:
            return {"column_name": 'relationship', "column_type": f"Optional[List[{model_name}]]",
                    "column_default": "None", "column_description": "'try to query the other table with foreign key'"}

    def _extra_relation_primary_key(self, relation_dbs: List[Table], default_class_name: Optional[str] = None, postfix: Optional[str] = "") -> Tuple[
        List[str], str, List[Tuple[str, str, Union[str, Type[Any]], str]]]:

        if default_class_name is None:
            default_class_name = self.class_name
        primary_key_columns = []
        primary_column_names = []
        for db_model_table in relation_dbs:
            table_name = db_model_table.key
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
        class_name = f'{default_class_name}{postfix}RelationshipPrimaryKeyModel'
        self.code_gen.build_dataclass(class_name=class_name,
                                      fields=[(primary_key_column[0],
                                               primary_key_column[1],
                                               f"Query({primary_key_column[2]}, description={primary_key_column[3]})"
                                               ) for primary_key_column in primary_key_columns],
                                      value_of_list_to_str_columns=self.uuid_type_columns,
                                      filter_none=self.uuid_type_columns)

        return primary_column_names, class_name, primary_key_columns

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

    def foreign_tree_get_many(self, foreign_tree: dict = None, path: str = None, pk_list: List[str] = None,
                              class_name: str = None,
                              included_model_list: List[Table] = None) -> Tuple:

        foreign_tree_api_list: List[dict] = []
        if foreign_tree is None:
            foreign_tree = self.foreign_tree

        if class_name is None:
            class_name = foreign_tree["model"].__name__
        else:
            class_name += "To" + foreign_tree["model"].__name__

        table_name = foreign_tree["table_name"]
        table_detail = self.foreign_mapper[table_name]
        _all_fields = table_detail["all_fields"]
        _primary_key = table_detail["primary_key"]
        _db_name = table_detail["db_name"]
        _db_model = table_detail["db_model"]
        _db_model_table = table_detail["db_model_table"]

        if path is None:
            path = '/' + self.db_name + '/{' + _db_name + FOREIGN_PATH_PARAM_KEYWORD + _primary_key + '}'
        else:
            if _db_name == self.db_name:
                return foreign_tree_api_list



        if pk_list is None:
            pk_list = []

        if included_model_list is None:
            included_model_list = []
        foreign_included_model_list = [*included_model_list]


        foreign_tree_pk_list = [*pk_list]

        if _db_name + "." + _primary_key in foreign_tree_pk_list:
            return foreign_tree_api_list
        if _db_model_table in foreign_included_model_list:
            return foreign_tree_api_list
        foreign_included_model_list.append(_db_model_table)
        foreign_tree_pk_list.append(_db_name + "." + _primary_key)

        if not foreign_tree["foreign"]:
            # use pk_list to build url
            for index, pk in enumerate(foreign_tree_pk_list[1::]):
                foreign_table_name, foreign_column_name = pk.split(".")
                path += '/' + foreign_table_name
                if foreign_table_name != _db_name:
                    path += '/{' + foreign_table_name + FOREIGN_PATH_PARAM_KEYWORD + foreign_column_name + '}'
                else:
                    break

            _primary_key_dataclass_model = self._extra_relation_primary_key(foreign_included_model_list[:-1:], class_name, postfix="FindMany")
            _query_param: List[dict] = self._get_fizzy_query_param(foreign_tree_pk_list, _all_fields)
            _query_param: List[Tuple] = self._assign_pagination_param(_query_param, _all_fields)

            table_of_foreign, reference_mapper = self._extra_foreign_find_table_from_declarative_base(_db_model,
                                                                                                      is_foreign_tree=True,
                                                                                                      is_gen_code=True)

            foreign_join_common_column: Union[dict, None] = self._assign_foreign_join(table_of_foreign,
                                                                                      model_name=_db_model.__name__,
                                                                                      is_foreign_tree=True)
            if foreign_join_common_column is not None:
                _query_param += [foreign_join_common_column]
            response_fields = []
            all_field = deepcopy(_all_fields)

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
                                           f"Query({i['column_default']}, description={i['column_description']} {', include_in_schema=False' if 'include_in_schema' in i and i['include_in_schema'] is False else ''})"))
            if self.foreign_table_response_model_sets_get_many:
                relationship_table_list = []
                for local_column, refer_table_info in reference_mapper.items():
                    if refer_table_info['foreign_table'] in self.foreign_table_response_model_sets_get_many:
                        relationship_table_list.append(
                            self.foreign_table_response_model_sets_get_many[refer_table_info['foreign_table']][
                                "class_name"])
                if not relationship_table_list:
                    pass
                response_fields.append((
                    "relationship",
                    f"Dict[str, List[Union[{', '.join(relationship_table_list)}]]]",
                    None
                ))

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
            _response_model["function_name"] = "get_many_by_"+ "_".join([pk.split(".")[0] for pk in pk_list]) +"_foreign_key"
            foreign_tree_api_list.append(_response_model)
            return foreign_tree_api_list

        foreign_list_of_this_table = foreign_tree["foreign"]
        for foreign_table in foreign_list_of_this_table:
            if not foreign_table:
                continue
            foreign_tree_api_list += self.foreign_tree_get_many(foreign_table, path, foreign_tree_pk_list, class_name,
                                                                foreign_included_model_list)

        if _db_name != self.root_table_name:
            # use pk_list to build url
            for index, pk in enumerate(foreign_tree_pk_list[1::]):
                foreign_table_name, foreign_column_name = pk.split(".")
                path += '/' + foreign_table_name
                if foreign_table_name != _db_name:
                    path += '/{' + foreign_table_name + FOREIGN_PATH_PARAM_KEYWORD + foreign_column_name + '}'
                else:
                    break

            _primary_key_dataclass_model = self._extra_relation_primary_key(foreign_included_model_list[:-1:], class_name, postfix="FindMany")
            _query_param: List[dict] = self._get_fizzy_query_param(foreign_tree_pk_list, _all_fields)
            _query_param: List[Tuple] = self._assign_pagination_param(_query_param, _all_fields)

            table_of_foreign, reference_mapper = self._extra_foreign_find_table_from_declarative_base(_db_model,
                                                                                                      is_foreign_tree=True,
                                                                                                      is_gen_code=True)

            foreign_join_common_column: Union[dict, None] = self._assign_foreign_join(table_of_foreign,
                                                                                      model_name=_db_model.__name__,
                                                                                      is_foreign_tree=True)
            if foreign_join_common_column is not None:
                _query_param += [foreign_join_common_column]
            response_fields = []
            all_field = deepcopy(_all_fields)

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
                                           f"Query({i['column_default']}, description={i['column_description']} {', include_in_schema=False' if 'include_in_schema' in i and i['include_in_schema'] is False else ''})"))
            if self.foreign_table_response_model_sets_get_many:
                relationship_table_list = []
                for local_column, refer_table_info in reference_mapper.items():
                    if refer_table_info['foreign_table'] in self.foreign_table_response_model_sets_get_many:
                        relationship_table_list.append(
                            self.foreign_table_response_model_sets_get_many[refer_table_info['foreign_table']][
                                "class_name"])
                if not relationship_table_list:
                    pass
                response_fields.append((
                    "relationship",
                    f"Dict[str, List[Union[{', '.join(relationship_table_list)}]]]",
                    None
                ))

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
            _response_model["function_name"] = "get_many_by_foreign_key"
            foreign_tree_api_list.append(_response_model)
        return foreign_tree_api_list

    def foreign_tree_get_one(self, foreign_tree: dict = None, path: str = None, pk_list: List[str] = None,
                             class_name: str = None,
                             included_model_list: List[Table] = None) -> Tuple:

        foreign_tree_api_list: List[dict] = []
        if foreign_tree is None:
            foreign_tree = self.foreign_tree

        if class_name is None:
            class_name = foreign_tree["model"].__name__
        else:
            class_name += "To" + foreign_tree["model"].__name__

        table_name = foreign_tree["table_name"]
        table_detail = self.foreign_mapper[table_name]
        _all_fields = table_detail["all_fields"]
        _primary_key = table_detail["primary_key"]
        _db_name = table_detail["db_name"]
        _db_model = table_detail["db_model"]
        _db_model_table = table_detail["db_model_table"]

        if path is None:
            path = '/' + self.db_name + '/{' + _db_name + FOREIGN_PATH_PARAM_KEYWORD + _primary_key + '}'
        else:
            if _db_name == self.db_name:
                return foreign_tree_api_list

        if pk_list is None:
            pk_list = []

        if included_model_list is None:
            included_model_list = []
        foreign_included_model_list = [*included_model_list]

        foreign_tree_pk_list = [*pk_list]

        if _db_name + "." + _primary_key in foreign_tree_pk_list:
            return foreign_tree_api_list
        if _db_model_table in foreign_included_model_list:
            return foreign_tree_api_list
        foreign_included_model_list.append(_db_model_table)
        foreign_tree_pk_list.append(_db_name + "." + _primary_key)

        if not foreign_tree["foreign"]:
            # use pk_list to build url
            for index, pk in enumerate(foreign_tree_pk_list[1::]):
                foreign_table_name, foreign_column_name = pk.split(".")
                path += '/' + foreign_table_name + '/{' + foreign_table_name + FOREIGN_PATH_PARAM_KEYWORD + foreign_column_name + '}'
            foreign_included_list = []
            path_include_table_regex = re.compile(r'\/([^\/]+)+/')
            path_included_list = path_include_table_regex.findall(path)
            for table in foreign_included_model_list:
                if table.name in path_included_list:
                    foreign_included_list.append(table)
            _primary_key_dataclass_model = self._extra_relation_primary_key(foreign_included_list,
                                                                            class_name, postfix="FindOne")
            _query_param: List[dict] = self._get_fizzy_query_param(foreign_tree_pk_list, _all_fields)
            table_of_foreign, reference_mapper = self._extra_foreign_find_table_from_declarative_base(_db_model,
                                                                                                      is_foreign_tree=True,
                                                                                                      is_gen_code=True,
                                                                                                      is_get_many=False
                                                                                                      )
            foreign_join_common_column: Union[dict, None] = self._assign_foreign_join(table_of_foreign,
                                                                                      model_name=_db_model.__name__,
                                                                                      is_foreign_tree=True)
            if foreign_join_common_column is not None:
                _query_param += [foreign_join_common_column]
            response_fields = []
            all_field = deepcopy(_all_fields)
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
                                           f"Query({i['column_default']}, description={i['column_description']} {', include_in_schema=False' if 'include_in_schema' in i and i['include_in_schema'] is False else ''})"))
            if self.foreign_table_response_model_sets_get_one:
                relationship_table_list = []
                for local_column, refer_table_info in reference_mapper.items():
                    if refer_table_info['foreign_table'] in self.foreign_table_response_model_sets_get_one:
                        relationship_table_list.append(
                            self.foreign_table_response_model_sets_get_one[refer_table_info['foreign_table']][
                                "class_name"])
                if not relationship_table_list:
                    pass
                response_fields.append((
                    "relationship",
                    f"Dict[str, List[Union[{', '.join(relationship_table_list)}]]]",
                    None
                ))
            self.code_gen.build_dataclass(class_name=class_name + "FindOneForeignTreeRequestBody",
                                          fields=request_fields,
                                          value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)
            self.code_gen.build_base_model(class_name=class_name + "FindOneForeignTreeResponseModel",
                                           fields=response_fields,
                                           value_of_list_to_str_columns=self.uuid_type_columns)

            _response_model = {}
            _response_model["primary_key_dataclass_model"] = _primary_key_dataclass_model[1]
            _response_model["request_query_model"] = class_name + "FindOneForeignTreeRequestBody"
            _response_model["response_model"] = class_name + "FindOneForeignTreeResponseModel"
            _response_model["path"] = path
            _response_model['class_name'] = class_name
            _response_model["function_name"] = "get_one_by_" + "_".join(
                [pk.split(".")[0] for pk in pk_list]) + "_foreign_key"
            foreign_tree_api_list.append(_response_model)
            return foreign_tree_api_list

        foreign_list_of_this_table = foreign_tree["foreign"]
        for foreign_table in foreign_list_of_this_table:
            if not foreign_table:
                continue
            foreign_tree_api_list += self.foreign_tree_get_one(foreign_table, path, foreign_tree_pk_list, class_name,
                                                                foreign_included_model_list)

        if _db_name != self.root_table_name:
            # use pk_list to build url
            for index, pk in enumerate(foreign_tree_pk_list[1::]):
                foreign_table_name, foreign_column_name = pk.split(".")
                path += '/' + foreign_table_name + '/{' + foreign_table_name + FOREIGN_PATH_PARAM_KEYWORD + foreign_column_name + '}'
            foreign_included_list = []
            path_include_table_regex = re.compile(r'\/([^\/]+)+/')
            path_included_list = path_include_table_regex.findall(path)
            for table in foreign_included_model_list:
                if table.name in path_included_list:
                    foreign_included_list.append(table)
            _primary_key_dataclass_model = self._extra_relation_primary_key(foreign_included_list,
                                                                            class_name, postfix="FindOne")
            _query_param: List[dict] = self._get_fizzy_query_param(foreign_tree_pk_list, _all_fields)
            table_of_foreign, reference_mapper = self._extra_foreign_find_table_from_declarative_base(_db_model,
                                                                                                      is_foreign_tree=True,
                                                                                                      is_gen_code=True,
                                                                                                      is_get_many=False)
            foreign_join_common_column: Union[dict, None] = self._assign_foreign_join(table_of_foreign,
                                                                                      model_name=_db_model.__name__,
                                                                                      is_foreign_tree=True)
            if foreign_join_common_column is not None:
                _query_param += [foreign_join_common_column]
            response_fields = []
            all_field = deepcopy(_all_fields)
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
                                           f"Query({i['column_default']}, description={i['column_description']} {', include_in_schema=False' if 'include_in_schema' in i and i['include_in_schema'] is False else ''})"))
            if self.foreign_table_response_model_sets_get_one:
                relationship_table_list = []
                for local_column, refer_table_info in reference_mapper.items():
                    if refer_table_info['foreign_table'] in self.foreign_table_response_model_sets_get_one:
                        relationship_table_list.append(
                            self.foreign_table_response_model_sets_get_one[refer_table_info['foreign_table']][
                                "class_name"])
                if not relationship_table_list:
                    pass
                response_fields.append((
                    "relationship",
                    f"Dict[str, List[Union[{', '.join(relationship_table_list)}]]]",
                    None
                ))
            self.code_gen.build_dataclass(class_name=class_name + "FindOneForeignTreeRequestBody",
                                          fields=request_fields,
                                          value_of_list_to_str_columns=self.uuid_type_columns, filter_none=True)
            self.code_gen.build_base_model(class_name=class_name + "FindOneForeignTreeResponseModel",
                                           fields=response_fields,
                                           value_of_list_to_str_columns=self.uuid_type_columns)
            _response_model = {}
            _response_model["primary_key_dataclass_model"] = _primary_key_dataclass_model[1]
            _response_model["request_query_model"] = class_name + "FindOneForeignTreeRequestBody"
            _response_model["response_model"] = class_name + "FindOneForeignTreeResponseModel"
            _response_model["path"] = path
            _response_model['class_name'] = class_name
            _response_model["function_name"] = "get_one_by_foreign_key"
            foreign_tree_api_list.append(_response_model)
        return foreign_tree_api_list

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

        if self.foreign_table_response_model_sets_get_many:
            relationship_list = []
            for table_mode, info_dict in self.foreign_table_response_model_sets_get_many.items():
                if table_mode.__tablename__ in self.table_of_foreign:
                    relationship_list.append(info_dict["class_name"])
            response_fields.append((
                "relationship",
                f"Dict[str, List[Union[{', '.join(relationship_list)}]]]",
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
        if self.foreign_table_response_model_sets_get_one:

            relationship_list = []
            for table_mode, info_dict in self.foreign_table_response_model_sets_get_one.items():
                if table_mode.__tablename__ in self.table_of_foreign:
                    relationship_list.append(info_dict["class_name"])
            response_fields.append((
                "relationship",
                f"Dict[str, List[Union[{', '.join(relationship_list)}]]]",
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
