# Fastapi CRUD Project Generator

## Quick Start

### Install
```python
pip install fastapi-crud-code-generator
```
### Prepare your Sqlalchemy schema

```
from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class SampleTable(Base):
    __tablename__ = 'test_build_myself_memory'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10, collation='NOCASE'))
    date_value = Column(Date)
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, default=10.10)
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, default=99)
    text_value = Column(Text)
    varchar_value = Column(String)

class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_memory_two'
    __table_args__ = (
        UniqueConstraint('primary_key'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
```

### Use `crud_router_builder()` to generate the project from the executing folder (using in-memory sqlite db here)

```python

from fastapi_quickcrud_codegen import crud_router_builder, CrudMethods

crud_router_builder(
    db_model_list=[
        {
            "db_model": SampleTable,
            "prefix": "/my_first_api",
            "tags": ["sample api"],
            "exclude_columns": ['bytea_value']
        },

        {
            "db_model": SampleTableTwo,
            "prefix": "/my_second_api",
            "tags": ["sample api"],
            "exclude_columns": ['bytea_value']
        }
    ],
    crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE, CrudMethods.UPDATE_MANY, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE],
    #is_async=True,
    #database_url="sqlite+aiosqlite://",
    is_async=False,
    database_url="sqlite://"
)
```

# Support


This project will generate CRUD code from you Sqlalchemy model. Which supports following api:

- Get one
- Get many
- Insert one
- Insert many
- Update one
- Update many
- Patch one
- Patch many
- Delete one
- Delete many
