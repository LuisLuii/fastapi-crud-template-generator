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


def account_many():
    import requests
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

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    # Get Many paging
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
        'limit': '1',
        'offset': '0',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
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
        'limit': '1',
        'offset': '1',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 1,
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
        'limit': '1',
        'offset': '2',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
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
        'limit': '2',
        'offset': '0',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
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
        'limit': '2',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
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
        'offset': '2',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
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
        'id____to': '1',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'case_sensitive',
        'name____str': 'string1',
        'name____list_____comparison_operator': 'Not_in',
        'name____list': 'string12',
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '1',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'case_sensitive',
        'name____str': 'string1',
        'name____list_____comparison_operator': 'Not_in',
        'name____list': 'string12',
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '1',
        'offset': '1',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 0,
                            "account_id": 0
                        },
                        {
                            "id": 1,
                            "account_id": 0
                        }
                    ]
                }
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 3,
                            "account_id": 1
                        },
                        {
                            "id": 4,
                            "account_id": 1
                        }
                    ]
                }
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 2,
                            "account_id": 2
                        }
                    ]
                }
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '1',
        'offset': '0',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 0,
                            "account_id": 0
                        },
                        {
                            "id": 1,
                            "account_id": 0
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '1',
        'offset': '1',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 3,
                            "account_id": 1
                        },
                        {
                            "id": 4,
                            "account_id": 1
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '1',
        'offset': '2',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 2,
                            "account_id": 2
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'order_by_columns': 'id: DESC',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 2,
                            "account_id": 2
                        }
                    ]
                }
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 3,
                            "account_id": 1
                        },
                        {
                            "id": 4,
                            "account_id": 1
                        }
                    ]
                }
            },
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 0,
                            "account_id": 0
                        },
                        {
                            "id": 1,
                            "account_id": 0
                        }
                    ]
                }
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'order_by_columns': 'id: ASC',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 0,
                            "account_id": 0
                        },
                        {
                            "id": 1,
                            "account_id": 0
                        }
                    ]
                }
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 3,
                            "account_id": 1
                        },
                        {
                            "id": 4,
                            "account_id": 1
                        }
                    ]
                }
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 2,
                            "account_id": 2
                        }
                    ]
                }
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '10',
        'offset': '0',
        'order_by_columns': 'id: ASC',
        'relationship': 'blog_post',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 0,
                            "account_id": 0
                        },
                        {
                            "id": 1,
                            "account_id": 0
                        }
                    ]
                }
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 3,
                            "account_id": 1
                        },
                        {
                            "id": 4,
                            "account_id": 1
                        }
                    ]
                }
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {
                    "blog_post": [
                        {
                            "id": 2,
                            "account_id": 2
                        }
                    ]
                }
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    import requests

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'order_by_columns': 'id: ASC',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200
    import requests

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'order_by_columns': 'id: DESC',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '100',
        'offset': '0',
        'order_by_columns': 'id: DESC',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'name____str_____matching_pattern': 'contains',
        'name____str': 'string',
        'name____list_____comparison_operator': 'In',
        'name____list': [
            'string',
            'string1',
            'string2',
        ],
        'age____from_____comparison_operator': 'Greater_than_or_equal_to',
        'age____to_____comparison_operator': 'Less_than_or_equal_to',
        'age____from': '0',
        'age____to': '100',
        'age____list_____comparison_operator': 'In',
        'email____str_____matching_pattern': 'case_sensitive',
        'email____str': 'string',
        'email____list_____comparison_operator': 'In',
        'email____list': 'string',
        'limit': '100',
        'offset': '0',
        'order_by_columns': 'id: ASC',
    }

    response = requests.get('http://localhost:8000/v1/account', params=params, headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 0,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 1,
                "name": "string1",
                "age": 0,
                "email": "string",
                "relationship": {}
            },
            {
                "id": 2,
                "name": "string2",
                "age": 0,
                "email": "string",
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

def account_blog_post_many():
    # basic find many without any param
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____list_____comparison_operator': 'In',
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____list_____comparison_operator': 'In',
    }

    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 0,
                "account_id": 0,
                "relationship": {}
            },
            {
                "id": 1,
                "account_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____list_____comparison_operator': 'In',
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____list_____comparison_operator': 'In',
    }

    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 3,
                "account_id": 1,
                "relationship": {}
            },
            {
                "id": 4,
                "account_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    # find many with query param
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 3,
                "account_id": 1,
                "relationship": {}
            },
            {
                "id": 4,
                "account_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 0,
                "account_id": 0,
                "relationship": {}
            },
            {
                "id": 1,
                "account_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    # find many with query param and paging
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '1',
        'offset': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 0,
                "account_id": 0,
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '1',
        'offset': '1',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
                "account_id": 0,
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
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '1',
        'offset': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '1',
        'offset': '1',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with query param and paging and order by
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 0,
                "account_id": 0,
                "relationship": {}
            },
            {
                "id": 1,
                "account_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [

            {
                "id": 1,
                "account_id": 0,
                "relationship": {}
            },
            {
                "id": 0,
                "account_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'order_by_columns': 'id:DESC',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [

            {
                "id": 1,
                "account_id": 0,
                "relationship": {}
            },
            {
                "id": 0,
                "account_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'order_by_columns': 'id:ASC',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'order_by_columns': 'id:DESC',
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    # find many with query param and paging and order by and relationship
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }

    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }

    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }

    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}], 'blog_comment': []}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {'account': [
                                                          {'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}],
                                                          'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}], 'blog_comment': []}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {'account': [
                                                          {'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}],
                                                          'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}], 'blog_comment': []}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {'account': [
                                                          {'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}],
                                                          'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
        'relationship': [
            'account',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '10',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '0',
            '1',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '10',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:ASC',
        'relationship': [
            'account',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}]}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {'account': [
                                                          {'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}]}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'limit': '2',
        'offset': '0',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {'blog_comment': []}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'order_by_columns': 'id:DESC',
        'relationship': [
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 4, 'account_id': 1, 'relationship': {'blog_comment': []}},
                                                      {'id': 3, 'account_id': 1, 'relationship': {'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    # find many with relationship and query param
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'relationship': [
            'account'
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
                    ]
                }
            },
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
                    ]
                }
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '1',
            '0',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '0',
        'relationship': [
            'blog_comment'
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post', params=params, headers=headers)
    assert response.json() == {
        "total": 2,
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
            },
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
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'relationship': [
            'account',
            'blog_comment',
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}], 'blog_comment': []}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {'account': [
                                                          {'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}],
                                                          'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'relationship': [
            'blog_comment'
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {'blog_comment': []}},
                                                      {'id': 4, 'account_id': 1, 'relationship': {'blog_comment': []}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '6',
        'id____list_____comparison_operator': 'In',
        'id____list': [
            '3',
            '4',
        ],
        'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'account_id____from': '0',
        'account_id____to': '4',
        'account_id____list_____comparison_operator': 'In',
        'account_id____list': '1',
        'relationship': [
            'account'
        ],
    }
    response = requests.get('http://localhost:8000/v1/account/1/blog_post', params=params, headers=headers)
    assert response.json() == {'total': 2, 'result': [{'id': 3, 'account_id': 1, 'relationship': {
        'account': [{'id': 1, 'name': 'string1', 'age': 0, 'email': 'string'}]}}, {'id': 4, 'account_id': 1,
                                                                                   'relationship': {'account': [
                                                                                       {'id': 1, 'name': 'string1',
                                                                                        'age': 0,
                                                                                        'email': 'string'}]}}]}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

def account_blog_post_blog_comment():
    # basic find many without any param
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____list_____comparison_operator': 'In',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____list_____comparison_operator': 'In',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/0/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 0,
                "blog_id": 0,
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
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____list_____comparison_operator': 'In',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 3,
        "result": [
            {
                "id": 1,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 4,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "3"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____list_____comparison_operator': 'In',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____list_____comparison_operator': 'In',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/2/blog_comment', params=params,
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
        'id____list_____comparison_operator': 'In',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____list_____comparison_operator': 'In',
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 2,
                "blog_id": 2,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with query param
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/0/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 0,
                "blog_id": 0,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '3',
        'id____to': '4',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 4,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/2/blog_comment', params=params,
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
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 2,
                "blog_id": 2,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with query param and paging
    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '1',
        'offset': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/0/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 0,
                "blog_id": 0,
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
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '1',
        'offset': '1',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/0/blog_comment', params=params,
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
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '1',
        'offset': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '1',
        'offset': '1',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '2',
        'offset': '0',
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "0",
        "offset": "0"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/2/blog_comment', params=params,
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
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "1",
        "offset": "0",
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 2,
                "blog_id": 2,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with query param and paging and order by

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'id:ASC'
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 2,
        "result": [
            {
                "id": 1,
                "blog_id": 1,
                "relationship": {}
            },
            {
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'id:DESC'
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1, 'id': 3, 'relationship': {}},
                                          {'blog_id': 1, 'id': 1, 'relationship': {}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'blog_id:ASC'
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1, 'id': 1, 'relationship': {}},
                                          {'blog_id': 1, 'id': 3, 'relationship': {}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'blog_id:DESC'
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1, 'id': 1, 'relationship': {}},
                                          {'blog_id': 1, 'id': 3, 'relationship': {}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "1",
        "offset": "0",
        'order_by_columns': 'blog_id:DESC'
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 2,
                "blog_id": 2,
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
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "1",
        "offset": "0",
        'order_by_columns': 'blog_id:ASC'
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {
        "total": 1,
        "result": [
            {
                "id": 2,
                "blog_id": 2,
                "relationship": {}
            }
        ]
    }
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with query param and paging and order by and relationship

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'id:ASC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 1,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'id:DESC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 1,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'blog_id:ASC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 1,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        'limit': '3',
        'offset': '0',
        'order_by_columns': 'blog_id:DESC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 1,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "1",
        "offset": "0",
        'order_by_columns': 'blog_id:DESC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 2,
                                           'id': 2,
                                           'relationship': {'blog_post': [{'account_id': 2, 'id': 2}]}}],
                               'total': 1}
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "limit": "1",
        "offset": "0",
        'order_by_columns': 'blog_id:ASC',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 2,
                                           'id': 2,
                                           'relationship': {'blog_post': [{'account_id': 2, 'id': 2}]}}],
                               'total': 1}
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    # find many with relationship and query param

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "relationship": "blog_post"

    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/0/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 0,
                                           'id': 0,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 0}]}}],
                               'total': 1}

    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '1',
        'id____to': '3',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "relationship": "blog_post"

    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 1,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '3',
        'id____to': '4',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/1/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 1,
                                           'id': 3,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}},
                                          {'blog_id': 1,
                                           'id': 4,
                                           'relationship': {'blog_post': [{'account_id': 0, 'id': 1}]}}],
                               'total': 2}
    assert response.headers["x-total-count"] == "2"
    assert response.status_code == 200

    params = {
        'id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'id____to_____comparison_operator': 'Less_than_or_equal_to',
        'id____from': '0',
        'id____to': '100',
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/0/blog_post/2/blog_comment', params=params,
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
        'id____list_____comparison_operator': 'Not_in',
        'id____list': '900',
        'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
        'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
        'blog_id____from': '0',
        'blog_id____to': '100',
        'blog_id____list_____comparison_operator': 'Not_equal',
        'blog_id____list': '900',
        "relationship": "blog_post"
    }
    response = requests.get('http://localhost:8000/v1/account/2/blog_post/2/blog_comment', params=params,
                            headers=headers)
    assert response.json() == {'result': [{'blog_id': 2,
                                           'id': 2,
                                           'relationship': {'blog_post': [{'account_id': 2, 'id': 2}]}}],
                               'total': 1}
    assert response.headers["x-total-count"] == "1"
    assert response.status_code == 200


def blog_post_many():
    def basic_find_many_without_any_param():
        # basic find many without any param
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        # find many with query param
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging():
        # find many with query param and paging
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '2'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by():
        # find many with query param and paging and order by and relationship
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "id"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "id:ASC"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "id:DESC"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 4,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "account_id": 2,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                },
                {
                    "id": 0,
                    "account_id": 0,
                    "relationship": {}
                },
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "account_id"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}},
                                              {'account_id': 1, 'id': 3, 'relationship': {}},
                                              {'account_id': 1, 'id': 4, 'relationship': {}},
                                              {'account_id': 2, 'id': 2, 'relationship': {}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "account_id:ASC"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}},
                                              {'account_id': 1, 'id': 3, 'relationship': {}},
                                              {'account_id': 1, 'id': 4, 'relationship': {}},
                                              {'account_id': 2, 'id': 2, 'relationship': {}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            "order_by_columns": "account_id:DESC"
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2, 'id': 2, 'relationship': {}},
                                              {'account_id': 1, 'id': 3, 'relationship': {}},
                                              {'account_id': 1, 'id': 4, 'relationship': {}},
                                              {'account_id': 0, 'id': 0, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1, 'id': 4, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 1, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1, 'id': 3, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2, 'id': 2, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2, 'id': 2, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1, 'id': 4, 'relationship': {}}], 'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1, 'id': 3, 'relationship': {}},
                                              {'account_id': 2, 'id': 2, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}},
                                              {'account_id': 0, 'id': 0, 'relationship': {}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}},
                                              {'account_id': 2, 'id': 2, 'relationship': {}},
                                              {'account_id': 1, 'id': 3, 'relationship': {}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 0, 'relationship': {}},
                                              {'account_id': 0, 'id': 1, 'relationship': {}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '2',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0, 'id': 1, 'relationship': {}},
                                              {'account_id': 0, 'id': 0, 'relationship': {}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '2',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 3,
                    "account_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by_and_relationship():
        # find many with query param and paging and order by
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '10',
            'offset': '0',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '0',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '1',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '2',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4',
            'relationship': ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4',
            'relationship': ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'limit': '1',
            'offset': '4',
            'relationship': ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 4,
                                               'relationship': {'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0',
            'relationship': ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0',
            'relationship': ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '4',
            'offset': '0',
            'relationship': ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '0',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '0',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '0',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '2',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '2',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'limit': '2',
            'offset': '2',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "2"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '0',
            'relationship': ["account", "blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '0',
            'relationship': ["account"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '0',
            'relationship': ["blog_comment"]

        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '0',
            'offset': '0',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'limit': '1',
            'offset': '1',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_relationship_and_query_param():
        # find many with relationship and query param
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '5',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'In',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}},
                                              {'account_id': 1,
                                               'id': 4,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 5}
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}],
                                                                'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                                 {'blog_id': 1, 'id': 3},
                                                                                 {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}],
                                                                'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 0,
                                                                             'name': 'string1'}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 2,
                                                                             'name': 'string2'}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '2',
            'account_id____list_____comparison_operator': 'Not_in',
            'account_id____list': '100',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 0,
                                               'id': 0,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 0, 'id': 0}]}},
                                              {'account_id': 0,
                                               'id': 1,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 1, 'id': 1},
                                                                    {'blog_id': 1, 'id': 3},
                                                                    {'blog_id': 1, 'id': 4}]}},
                                              {'account_id': 2,
                                               'id': 2,
                                               'relationship': {
                                                   'blog_comment': [{'blog_id': 2, 'id': 2}]}},
                                              {'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 4}
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account", "blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}],
                                                                'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["account"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {'account': [{'age': 0,
                                                                             'email': 'string',
                                                                             'id': 1,
                                                                             'name': 'string1'}]}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '4',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '100',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____from': '0',
            'account_id____to': '1',
            'account_id____list_____comparison_operator': 'In',
            'account_id____list': '1',
            'relationship': ["blog_comment"]
        }
        response = requests.get('http://localhost:8000/v1/blog_post', params=params, headers=headers)
        assert response.json() == {'result': [{'account_id': 1,
                                               'id': 3,
                                               'relationship': {
                                                   'blog_comment': []}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    basic_find_many_without_any_param()
    find_many_with_query_param_and_paging()
    find_many_with_query_param_and_paging_and_order_by()
    find_many_with_query_param_and_paging_and_order_by_and_relationship()
    find_many_with_relationship_and_query_param()

def blog_post_account():
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

        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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

        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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

        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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

    def basic_find_many_with_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string9090',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string@gmail.com',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 0,
            'offset': 0,
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string9090',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string9090',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string9090',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string@gmail.com',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string@gmail.com',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string@gmail.com',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '0',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'name:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'age:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'email:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'name'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'age'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'email'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'name:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'age:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 0,
            'order_by_columns': 'email:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'name',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'age',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            "limit": 1,
            'offset': 1,
            'order_by_columns': 'email',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
            ]
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    def find_many_with_relationship_and_query_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "name": "string1",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
                            },
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string9090',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/account', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "name": "string2",
                    "age": 0,
                    "email": "string",
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
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
            'id____list_____comparison_operator': 'Not_in',
            'id____list': '99',
            'name____str_____matching_pattern': 'contains',
            'name____str': 'string',
            'name____list_____comparison_operator': 'In',
            'name____list': [
                'string',
                'string1',
                'string2',
                'string3',
            ],
            'age____from_____comparison_operator': 'Greater_than_or_equal_to',
            'age____to_____comparison_operator': 'Less_than_or_equal_to',
            'age____from': '0',
            'age____to': '100',
            'age____list_____comparison_operator': 'In',
            'email____str_____matching_pattern': 'case_sensitive',
            'email____str': 'string@gmail.com',
            'email____list_____comparison_operator': 'In',
            'email____list': 'string',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/account', params=params, headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    basic_find_many_without_any_param()
    basic_find_many_with_param()
    find_many_with_query_param_and_paging()
    find_many_with_query_param_and_paging_and_order_by()
    find_many_with_query_param_and_paging_and_order_by_and_relationship()
    find_many_with_relationship_and_query_param()

def blog_post_comment():
    def basic_find_many_without_any_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        response = requests.get('http://localhost:8000/v1/blog_post/3/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
        }
        response = requests.get('http://localhost:8000/v1/blog_post/3/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 2
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 0,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 0,
            'offset': 0
        }
        response = requests.get('http://localhost:8000/v1/blog_post/3/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [{
                "id": 3,
                "blog_id": 1,
                "relationship": {}
            },
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 2,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [{

                "id": 4,
                "blog_id": 1,
                "relationship": {}

            },
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 2,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [{"id": 0, "blog_id": 0, "relationship": {"blog_post": [{"id": 0, "account_id": 0}]}}]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 0,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 3,
            'offset': 0,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [{
                "id": 3,
                "blog_id": 1,
                "relationship": {
                    "blog_post": [
                        {
                            "id": 1,
                            "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 2,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [{
                "id": 4,
                "blog_id": 1,
                "relationship": {
                    "blog_post": [
                        {
                            "id": 1,
                            "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 1,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 2,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'limit': 1,
            'offset': 0,
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    def find_many_with_query_param_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/0/blog_comment', params=params, headers=headers)
        assert response.json() == {'result': [{'blog_id': 0,
                                               'id': 0,
                                               'relationship': {'blog_post': [{'account_id': 0, 'id': 0}]}}],
                                   'total': 1}
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 3,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "3"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____from': '0',
            'id____to': '100',
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/2/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
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
            'id____list_____comparison_operator': 'Not_equal',
            'id____list': '872',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '100',
            'blog_id____list_____comparison_operator': 'Not_in',
            'blog_id____list': '1723',
            'order_by_columns': 'id',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_post/3/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 0,
            "result": []
        }
        assert response.headers["x-total-count"] == "0"
        assert response.status_code == 200

    basic_find_many_without_any_param()
    basic_find_many_with_param()
    find_many_with_query_param_and_paging()
    find_many_with_query_param_and_paging_and_order_by()
    find_many_with_query_param_and_paging_and_order_by_and_relationship()
    find_many_with_query_param_and_order_by_and_relationship()


def blog_comment():
    def basic_find_many_without_any_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____list_____comparison_operator': 'In',
        }

        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 5,
            "result": [
                {
                    "id": 0,
                    "blog_id": 0,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "5"
        assert response.status_code == 200

    def basic_find_many_with_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
        }

        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging():
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

    def find_many_with_query_param_and_paging_and_order_by():
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }

            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'blog_id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'blog_id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'blog_id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'blog_id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'blog_id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'blog_id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'blog_id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'blog_id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'blog_id:ASC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'blog_id:DESC'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {}
                },
            ]
        }
        assert response.headers["x-total-count"] == "1"

    def find_many_with_query_param_and_paging_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '10',
            'offset': '0',
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '0',
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '1',
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '2',
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'limit': '1',
            'offset': '3',
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"

    def find_many_with_query_param_and_order_by_and_relationship():
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'order_by_columns': 'id:ASC',
            'relationship': 'blog_post'

        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'order_by_columns': 'id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'order_by_columns': 'blog_id:ASC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200
        params = {
            'id____from_____comparison_operator': 'Greater_than',
            'id____to_____comparison_operator': 'Less_than',
            'id____from': '0',
            'id____to': '10',
            'id____list_____comparison_operator': 'In',
            'id____list': [
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
            ],
            'blog_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'blog_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'blog_id____from': '0',
            'blog_id____to': '10',
            'blog_id____list_____comparison_operator': 'In',
            'blog_id____list': [
                '0',
                '1',
                '2',
            ],
            'order_by_columns': 'blog_id:DESC',
            'relationship': 'blog_post'
        }
        response = requests.get('http://localhost:8000/v1/blog_comment', params=params, headers=headers)
        assert response.json() == {
            "total": 4,
            "result": [
                {
                    "id": 2,
                    "blog_id": 2,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 2,
                                "account_id": 2
                            }
                        ]
                    }
                },
                {
                    "id": 1,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 3,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                },
                {
                    "id": 4,
                    "blog_id": 1,
                    "relationship": {
                        "blog_post": [
                            {
                                "id": 1,
                                "account_id": 0
                            }
                        ]
                    }
                }
            ]
        }
        assert response.headers["x-total-count"] == "4"
        assert response.status_code == 200

    basic_find_many_without_any_param()
    basic_find_many_with_param()
    find_many_with_query_param_and_paging()
    find_many_with_query_param_and_paging_and_order_by()
    find_many_with_query_param_and_paging_and_order_by_and_relationship()
    find_many_with_query_param_and_order_by_and_relationship()


def blog_comment_blog_post_account():
    def basic_find_many_without_any_param():
        params = {
            'id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'id____to_____comparison_operator': 'Less_than_or_equal_to',
            'id____list_____comparison_operator': 'In',
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____list_____comparison_operator': 'In',
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____list_____comparison_operator': 'In',
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____list_____comparison_operator': 'In',
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
            'account_id____from_____comparison_operator': 'Greater_than_or_equal_to',
            'account_id____to_____comparison_operator': 'Less_than_or_equal_to',
            'account_id____list_____comparison_operator': 'In',
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    def basic_find_many_with_param():
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
        }

        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
                    "relationship": {}
                }
            ]
        }
        assert response.headers["x-total-count"] == "1"
        assert response.status_code == 200

    def find_many_with_query_param_and_paging():
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
            "offset": 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
            "offset": 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
            "offset": 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
            "offset": 0
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
            "offset": 1
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
            "offset": 1
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
            "offset": 1
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
            "offset": 1
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/0/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 0,
                    "account_id": 0,
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

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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

        }
        response = requests.get('http://localhost:8000/v1/blog_comment/1/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/2/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 2,
                    "account_id": 2,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "account_id": 0,
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
        }
        response = requests.get('http://localhost:8000/v1/blog_comment/3/blog_post', params=params, headers=headers)
        assert response.json() == {
            "total": 1,
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


account_many()
account_blog_post_many()
account_blog_post_blog_comment()

blog_post_many()
blog_post_account()
blog_post_comment()

blog_comment()
blog_comment_blog_post_account()
