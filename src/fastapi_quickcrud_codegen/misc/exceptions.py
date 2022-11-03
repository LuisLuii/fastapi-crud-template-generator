from fastapi import HTTPException


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


class UnknownColumn(CRUDBuilderException):
    pass


class SchemaException(CRUDBuilderException):
    pass


class ColumnTypeNotSupportedException(CRUDBuilderException):
    pass


#
# class NotFoundError(MongoQueryError):
#     def __init__(self, Collection: Type[ModelType], model: BaseModel):
#         detail = "does not exist"
#         super().__init__(Collection, model, detail)
#
#
#
# class DuplicatedError(MongoQueryError):
#     def __init__(self, Collection: Type[ModelType], model: BaseModel):
#         detail = "was already existed"
#         super().__init__(Collection, model, detail)

class FDDRestHTTPException(HTTPException):
    """Baseclass for all HTTP exceptions in FDD Rest API.  This exception can be called as WSGI
        application to render a default error page or you can catch the subclasses
        of it independently and render nicer error messages.
        """
