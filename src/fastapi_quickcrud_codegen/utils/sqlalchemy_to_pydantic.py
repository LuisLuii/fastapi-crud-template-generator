from typing import Type, List

from ..misc.type import CrudMethods
from ..misc.crud_model import CRUDModel
from ..misc.exceptions import PrimaryMissing
from ..misc.type import SqlType, CRUDRequestMapping
from ..utils.schema_builder import ApiParameterSchemaBuilder


def sqlalchemy_to_pydantic(
        db_model: Type, *,
        crud_methods: List[CrudMethods],
        sql_type: str = SqlType.postgresql,
        exclude_columns: List[str] = None,
        constraints=None,
        # foreign_include: Optional[any] = None,
        ) -> CRUDModel:
    if exclude_columns is None:
        exclude_columns = []
    # if foreign_include is None:
    #     foreign_include = {}
    request_response_mode_set = {}
    model_builder = ApiParameterSchemaBuilder(db_model,
                                              constraints=constraints,
                                              exclude_column=exclude_columns,
                                              sql_type=sql_type,
                                              # foreign_include=foreign_include,
                                              )
    REQUIRE_PRIMARY_KEY_CRUD_METHOD = [CrudMethods.DELETE_ONE.value,
                                       CrudMethods.FIND_ONE.value,
                                       CrudMethods.PATCH_ONE.value,
                                       # CrudMethods.POST_REDIRECT_GET.value,
                                       CrudMethods.UPDATE_ONE.value]
    for crud_method in crud_methods:
        if crud_method.value in REQUIRE_PRIMARY_KEY_CRUD_METHOD and not model_builder.primary_key_str:
            raise PrimaryMissing(f"The generation of this API [{crud_method.value}] requires a primary key")

        # if crud_method.value == CrudMethods.UPSERT_ONE.value:
        #     model_builder.upsert_one()
        #     request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
        #     if request_method not in request_response_mode_set:
        #         request_response_mode_set[request_method] = {}
        #     request_response_mode_set[request_method][crud_method.value] = True
        # elif crud_method.value == CrudMethods.UPSERT_MANY.value:
        #     model_builder.upsert_many()
        #     request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
        #     if request_method not in request_response_mode_set:
        #         request_response_mode_set[request_method] = {}
        #     request_response_mode_set[request_method][crud_method.value] = True

        elif crud_method.value == CrudMethods.CREATE_ONE.value:
            model_builder.create_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True

        elif crud_method.value == CrudMethods.CREATE_MANY.value:
            model_builder.create_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.DELETE_ONE.value:
            model_builder.delete_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.DELETE_MANY.value:
            model_builder.delete_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.FIND_ONE.value:
            model_builder.find_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.FIND_MANY.value:
            model_builder.find_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        # elif crud_method.value == CrudMethods.POST_REDIRECT_GET.value:
        #     model_builder.post_redirect_get()
        #     request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
        #     if request_method not in request_response_mode_set:
        #         request_response_mode_set[request_method] = {}
        #     request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.PATCH_ONE.value:
            model_builder.patch_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.UPDATE_ONE.value:
            model_builder.update_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.UPDATE_MANY.value:
            model_builder.update_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.PATCH_MANY.value:
            model_builder.patch_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.FIND_ONE_WITH_FOREIGN_TREE.value:
            model_builder.foreign_tree_get_one()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
        elif crud_method.value == CrudMethods.FIND_MANY_WITH_FOREIGN_TREE.value:
            model_builder.foreign_tree_get_many()
            request_method = CRUDRequestMapping.get_request_method_by_crud_method(crud_method.value).value
            if request_method not in request_response_mode_set:
                request_response_mode_set[request_method] = {}
            request_response_mode_set[request_method][crud_method.value] = True
    model_builder.code_gen.gen()

    return CRUDModel(
        **{**request_response_mode_set,
           **{"PRIMARY_KEY_NAME": model_builder.primary_key_str,
              "UNIQUE_LIST": model_builder.unique_fields}})