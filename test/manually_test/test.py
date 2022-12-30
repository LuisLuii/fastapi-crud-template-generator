"""
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    age = Column(Integer)
    email = Column(VARCHAR)
    blog_post = relationship("BlogPost", back_populates="account")


class BlogPost(Base):
    __tablename__ = "blog_post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    account = relationship("Account", back_populates="blog_post")
    blog_comment = relationship("BlogComment", back_populates="blog_post")


class BlogComment(Base):
    __tablename__ = "blog_comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    blog_post = relationship("BlogPost", back_populates="blog_comment")


from fastapi_quickcrud_codegen.db_model import DbModel
from fastapi_quickcrud_codegen.misc.type import CrudMethods

from fastapi_quickcrud_codegen import crud_router_builder

model_list = [

    DbModel(db_model=Account, prefix="/v1", tags=["account"], foreign_include=[BlogPost, BlogComment],
            crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_MANY]),
    DbModel(db_model=BlogPost, prefix="/v1", tags=["Blog post"], foreign_include=[Account, BlogComment],
            crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_MANY]),
    # build the foreign_include table if not presented
    DbModel(db_model=BlogComment, prefix="/v1", tags=["Blog Comment"], foreign_include=[BlogPost, Account],
            crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_MANY])]
crud_router_builder(
    db_model_list=model_list,
    # is_async=True,
    # database_url="sqlite+aiosqlite://./test.db",
    is_async=False,
    database_url="sqlite:////Users/luilui/Documents/test.db"
)


"""

import requests

headers = {
    'accept': 'application/json',
}


def blog_comment_blog_post_account():
    def basic_find_many_without_any_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def basic_find_many_with_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id'
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'name:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'email:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'email:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post/0/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'age:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'age:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'email:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'email:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'name:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'age:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'age:DESC'

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'name:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'email:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'email:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'name:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:DESC'
        }


        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'name:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'case_sensitive',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/1/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____list_____comparison_operator': 'In',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/4/blog_post/2/account', params=params,
                                headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],

                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 0,
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "limit": 1,
            "offset": 1,
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 0,
                                "blog_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "account": [
                            {
                                "id": 2,
                                "name": "string2",
                                "age": 0,
                                "email": "string"
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 2,
                                "blog_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:ASC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "account": [
                            {
                                "id": 0,
                                "name": "string1",
                                "age": 0,
                                "email": "string"
                            }
                        ],

                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '100',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
            ],
            "order_by_columns": "id:DESC",
            "relationship": ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {
                        "blog_comment": [
                            {
                                "id": 1,
                                "blog_id": 1
                            },
                            {
                                "id": 3,
                                "blog_id": 1
                            },
                            {
                                "id": 4,
                                "blog_id": 1
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200


    basic_find_many_without_any_param()
    basic_find_many_with_param()
    find_many_with_query_param_and_paging()
    find_many_with_query_param_and_paging_and_order_by()
    find_many_with_query_param_and_paging_and_order_by_and_relationship()
    find_many_with_query_param_and_order_by_and_relationship()

blog_comment_blog_post_account()
