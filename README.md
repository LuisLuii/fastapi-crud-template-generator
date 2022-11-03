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
            "exclude_columns": ['bytea_value'],
            "crud_methods":[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_ONE, CrudMethods.UPDATE_MANY, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE],

        },

        {
            "db_model": SampleTableTwo,
            "prefix": "/my_second_api",
            "tags": ["sample api"],
            "exclude_columns": ['bytea_value'],
        }
    ],
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


**crud_router_builder args**
- db_model_list `[Required] `
    >  Model list of dict for code generate
  - `List[]`
    - `Dict[]`
      - db_model `[Required[SQLALchemy Declarative Base Class]]`
      - prefix `[Required[str]]`
         > prefix for Fastapi's end point 
      - tags `[Required[List[str]]]`
         > list of tag for Fastapi's end point 
      - exclude_columns `[Optional[str]]`
         > set the columns that not to be operated but the columns should nullable or set the default value)
      - crud_methods `[Opional[str]]`
        > - Create the following apis for that model, but default: [CrudMethods.FIND_MANY, CrudMethods.FIND_ONE, CrudMethods.CREATE_MANY, CrudMethods.PATCH_ONE, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE, CrudMethods.UPDATE_MANY, CrudMethods.UPDATE_ONE, CrudMethods.DELETE_MANY, CrudMethods.DELETE_ONE] 
        ```
        - CrudMethods.FIND_ONE
        - CrudMethods.FIND_MANY
        - CrudMethods.UPDATE_ONE
        - CrudMethods.UPDATE_MANY
        - CrudMethods.PATCH_ONE
        - CrudMethods.PATCH_MANY
        - CrudMethods.CREATE_ONE
        - CrudMethods.CREATE_MANY
        - CrudMethods.DELETE_ONE
        - CrudMethods.DELETE_MANY
        ```
      
- is_async `[Required]`
    
    >  True for async; False for sync
    
- database_url  `[Optional (str)]`
    >  A database URL. The URL is passed directly to SQLAlchemy's create_engine() method so please refer to SQLAlchemy's documentation for instructions on how to construct a proper URL.
    

# Design:
The model generation part and api router part refer to my another [project](https://github.com/LuisLuii/FastAPIQuickCRUD); The code generation part is using Jinja

## How to contribute more api?
1. Model generation
   1. Prepare Jinja template to `fastapi-crud-project-generator/src/fastapi_quickcrud_codegen/model/template`
   2. Prepare model code generation method from `fastapi_quickcrud_codegen.utils.schema_builder.ApiParameterSchemaBuilder`
   3. Generate the code from `fastapi_quickcrud_codegen/model/model_builder.py` 
2. CRUD Method Generation
   1. After the model generation, you can try to build your own api by your own model
   2. Modify `fastapi_quickcrud_codegen.utils.sqlalchemy_to_pydantic.sqlalchemy_to_pydantic`, `fastapi_quickcrud_codegen.misc.type.CrudMethods` and `fastapi_quickcrud_codegen.misc.crud_model.CRUDModel` to let project supports your api
   3. Prepare your api router Jinja template from `src/fastapi_quickcrud_codegen/model/template/route`
   4. Generate the code from `fastapi_quickcrud_codegen/model/crud_builder.py` 
   5. Update the api_register from `src/fastapi_quickcrud_codegen/crud_generator.py`
