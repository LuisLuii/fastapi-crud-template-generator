"""
from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TestingTable(Base):
    __tablename__ = 'test_build_myself_memory'
    primary_key = Column(Integer, primary_key=True, autoincrement=True, comment="hello")
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10, collation='NOCASE'), unique=True)
    date_value = Column(Date)
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, default=10.10)
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, default=99)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)


class TestingTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_memory_two'
    __table_args__ = (
        UniqueConstraint('primary_key', 'bool_value' ),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)


from fastapi_quickcrud_codegen import crud_router_builder, CrudMethods

crud_router_builder(
    db_model_list=[
        {
            "db_model": TestingTable,
            "prefix": "/my_first_api/test_build_myself_memory",
            "tags": ["sample api"],
            "exclude_columns": ['bytea_value']
        },

        {
            "db_model": TestingTableTwo,
            "prefix": "/my_second_api",
            "tags": ["sample api"],
            "exclude_columns": ['bytea_value'],
            "crud_methods": []
        }
    ],
    is_async=True,
    database_url="sqlite+aiosqlite://"
)

"""

import requests

data = [
    {
        "primary_key": 0,
        "bool_value": False,
        "char_value": "0",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "0",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "0",
        "varchar_value": "string"
    },
    {
        "primary_key": 1,
        "bool_value": False,
        "char_value": "1",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "1",
        "varchar_value": "string"
    },
    {
        "primary_key": 2,
        "bool_value": True,
        "char_value": "2",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "2",
        "varchar_value": "string"
    }
]
x = requests.post('http://localhost:8000/my_first_api/test_build_myself_memory', json=data)

assert x.text == '[{"primary_key":0,"bool_value":false,"char_value":"0","date_value":"2022-11-05","float4_value":0.0,"float8_value":10.1,"int2_value":0,"int4_value":0,"int8_value":99,"text_value":"string","time_value":"00:00:00","timestamp_value":"2022-11-05T05:13:59.616000+00:00","timestamptz_value":"2022-11-05T05:13:59.616000+00:00","timetz_value":"00:00:00","varchar_value":"string"},{"primary_key":1,"bool_value":false,"char_value":"1","date_value":"2022-11-05","float4_value":0.0,"float8_value":10.1,"int2_value":0,"int4_value":0,"int8_value":99,"text_value":"string","time_value":"00:00:01","timestamp_value":"2022-11-05T05:13:59.616000+00:00","timestamptz_value":"2022-11-05T05:13:59.616000+00:00","timetz_value":"00:00:01","varchar_value":"string"},{"primary_key":2,"bool_value":true,"char_value":"2","date_value":"2022-11-05","float4_value":0.0,"float8_value":10.1,"int2_value":0,"int4_value":0,"int8_value":99,"text_value":"string","time_value":"00:00:01","timestamp_value":"2022-11-05T05:13:59.616000+00:00","timestamptz_value":"2022-11-05T05:13:59.616000+00:00","timetz_value":"00:00:02","varchar_value":"string"}]'
assert x.status_code == 201

# try insert again
x = requests.post('http://localhost:8000/my_first_api/test_build_myself_memory', json=data)
assert x.status_code == 409

data = [
    {
        "primary_key": 0,
        "bool_value": False,
        "char_value": "0",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "0",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "0",
        "varchar_value": "string"
    },
    {
        "primary_key": 1,
        "bool_value": False,
        "char_value": "0",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "1",
        "varchar_value": "string"
    },
    {
        "primary_key": 2,
        "bool_value": True,
        "char_value": "2",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "2",
        "varchar_value": "string"
    }
]

# try insert again
x = requests.post('http://localhost:8000/my_first_api/test_build_myself_memory', json=data)
assert x.status_code == 409

# without params
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____list_____comparison_operator=In&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In')
assert x.status_code == 200
assert x.json()["total"] == 3
assert x.json()["result"] == [{'primary_key': 0, 'bool_value': False, 'char_value': '0', 'date_value': '2022-11-05', 'float4_value': 0.0, 'float8_value': 10.1, 'int2_value': 0, 'int4_value': 0, 'int8_value': 99, 'text_value': 'string', 'time_value': '00:00:00', 'timestamp_value': '2022-11-05T05:13:59.616000', 'timestamptz_value': '2022-11-05T05:13:59.616000', 'timetz_value': '00:00:00', 'varchar_value': 'string'}, {'primary_key': 1, 'bool_value': False, 'char_value': '1', 'date_value': '2022-11-05', 'float4_value': 0.0, 'float8_value': 10.1, 'int2_value': 0, 'int4_value': 0, 'int8_value': 99, 'text_value': 'string', 'time_value': '00:00:01', 'timestamp_value': '2022-11-05T05:13:59.616000', 'timestamptz_value': '2022-11-05T05:13:59.616000', 'timetz_value': '00:00:01', 'varchar_value': 'string'}, {'primary_key': 2, 'bool_value': True, 'char_value': '2', 'date_value': '2022-11-05', 'float4_value': 0.0, 'float8_value': 10.1, 'int2_value': 0, 'int4_value': 0, 'int8_value': 99, 'text_value': 'string', 'time_value': '00:00:01', 'timestamp_value': '2022-11-05T05:13:59.616000', 'timestamptz_value': '2022-11-05T05:13:59.616000', 'timetz_value': '00:00:02', 'varchar_value': 'string'}]



# test  query param
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____from=0&primary_key____to=1&primary_key____list_____comparison_operator=In&primary_key____list=0&primary_key____list=1&bool_value____list_____comparison_operator=In&bool_value____list=false&char_value____str_____matching_pattern=case_sensitive&char_value____str=0&char_value____list_____comparison_operator=In&char_value____list=0&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____from=2022-11-04&date_value____to=2022-11-05&date_value____list_____comparison_operator=In&date_value____list=2022-11-05&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____from=0.0&float4_value____to=0.0&float4_value____list_____comparison_operator=In&float4_value____list=0.0&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____from=10.1&float8_value____to=10.1&float8_value____list_____comparison_operator=In&float8_value____list=10.1&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____from=0&int2_value____to=0&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____from=0&int4_value____to=0&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____from=99&int8_value____to=99&int8_value____list_____comparison_operator=In&int8_value____list=99&text_value____str_____matching_pattern=case_sensitive&text_value____str=string&text_value____list_____comparison_operator=Not_equal&text_value____list=string111&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____from=00%3A00%3A00&time_value____to=00%3A00%3A00&time_value____list_____comparison_operator=In&time_value____list=00%3A00%3A00&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____from=2022-11-05T05%3A13%3A59.616000&timestamp_value____to=2022-11-05T05%3A13%3A59.616000&timestamp_value____list_____comparison_operator=In&timestamp_value____list=2022-11-05T05%3A13%3A59.616000&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____from=2022-11-05T05%3A13%3A59.616000&timestamptz_value____to=2022-11-05T05%3A13%3A59.616000&timestamptz_value____list_____comparison_operator=In&timestamptz_value____list=2022-11-05T05%3A13%3A59.616000&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____from=00%3A00%3A00&timetz_value____to=00%3A00%3A00&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____str=string&varchar_value____list_____comparison_operator=In&varchar_value____list=string')
assert x.status_code == 200
assert x.json()["total"] == 1
assert x.json()["result"] == [
    {
      "primary_key": 0,
      "bool_value": False,
      "char_value": "0",
      "date_value": "2022-11-05",
      "float4_value": 0,
      "float8_value": 10.1,
      "int2_value": 0,
      "int4_value": 0,
      "int8_value": 99,
      "text_value": "string",
      "time_value": "00:00:00",
      "timestamp_value": "2022-11-05T05:13:59.616000",
      "timestamptz_value": "2022-11-05T05:13:59.616000",
      "timetz_value": "00:00:00",
      "varchar_value": "string"
    }
  ]


# test  query param
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____from=0&primary_key____to=1&primary_key____list_____comparison_operator=In&primary_key____list=0&primary_key____list=1&bool_value____list_____comparison_operator=In&bool_value____list=false&char_value____str_____matching_pattern=case_sensitive&char_value____str=0&char_value____list_____comparison_operator=In&char_value____list=0&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____from=2022-11-04&date_value____to=2022-11-05&date_value____list_____comparison_operator=In&date_value____list=2022-11-05&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____from=0.0&float4_value____to=0.0&float4_value____list_____comparison_operator=In&float4_value____list=0.0&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____from=10.1&float8_value____to=10.1&float8_value____list_____comparison_operator=In&float8_value____list=10.1&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____from=0&int2_value____to=0&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____from=0&int4_value____to=0&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____from=99&int8_value____to=99&int8_value____list_____comparison_operator=In&int8_value____list=99&text_value____str_____matching_pattern=case_sensitive&text_value____str=string&text_value____list_____comparison_operator=Not_equal&text_value____list=string111&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____from=00%3A00%3A00&time_value____to=00%3A00%3A00&time_value____list_____comparison_operator=In&time_value____list=00%3A00%3A00&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____from=2022-11-05T05%3A13%3A59.616000&timestamp_value____to=2022-11-05T05%3A13%3A59.616000&timestamp_value____list_____comparison_operator=In&timestamp_value____list=2022-11-05T05%3A13%3A59.616000&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____from=2022-11-05T05%3A13%3A59.616000&timestamptz_value____to=2022-11-05T05%3A13%3A59.616000&timestamptz_value____list_____comparison_operator=In&timestamptz_value____list=2022-11-05T05%3A13%3A59.616000&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____from=00%3A00%3A00&timetz_value____to=00%3A00%3A00&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____str=string&varchar_value____list_____comparison_operator=Not_in&varchar_value____list=string')
assert x.status_code == 200
assert x.json()["total"] == 0
assert x.json()["result"] == []

# paginate
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____list_____comparison_operator=In&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In&limit=1&offset=0&order_by_columns=primary_key%3A%20ASC')
assert x.status_code == 200
assert x.json()["total"] == 3
assert x.json()["result"] == [
    {
      "primary_key": 0,
      "bool_value": False,
      "char_value": "0",
      "date_value": "2022-11-05",
      "float4_value": 0,
      "float8_value": 10.1,
      "int2_value": 0,
      "int4_value": 0,
      "int8_value": 99,
      "text_value": "string",
      "time_value": "00:00:00",
      "timestamp_value": "2022-11-05T05:13:59.616000",
      "timestamptz_value": "2022-11-05T05:13:59.616000",
      "timetz_value": "00:00:00",
      "varchar_value": "string"
    }
  ]

# paginate
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____list_____comparison_operator=In&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In&limit=1&offset=1&order_by_columns=primary_key%3A%20ASC')
assert x.status_code == 200
assert x.json()["total"] == 3
assert x.json()["result"] == [
    {
      "primary_key": 1,
      "bool_value": False,
      "char_value": "1",
      "date_value": "2022-11-05",
      "float4_value": 0,
      "float8_value": 10.1,
      "int2_value": 0,
      "int4_value": 0,
      "int8_value": 99,
      "text_value": "string",
      "time_value": "00:00:01",
      "timestamp_value": "2022-11-05T05:13:59.616000",
      "timestamptz_value": "2022-11-05T05:13:59.616000",
      "timetz_value": "00:00:01",
      "varchar_value": "string"
    }
  ]


# update
# update data
x = requests.put('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____from=0&primary_key____to=0&primary_key____list_____comparison_operator=In&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In', json={
    "bool_value": True,
    "char_value": "10",
    "date_value": "2022-11-05",
    "float4_value": 0,
    "float8_value": 0,
    "int2_value": 0,
    "int4_value": 0,
    "int8_value": 0,
    "text_value": "string",
    "time_value": "00:00:01",
    "timestamp_value": "2022-11-05T05:39:51.894000+00:00",
    "timestamptz_value": "2022-11-05T05:39:51.894000+00:00",
    "timetz_value": "00:00:01",
    "varchar_value": "string"
  })
assert x.status_code == 200
assert x.json() == [
  {
    "primary_key": 0,
    "bool_value": True,
    "char_value": "10",
    "date_value": "2022-11-05",
    "float4_value": 0,
    "float8_value": 0,
    "int2_value": 0,
    "int4_value": 0,
    "int8_value": 0,
    "text_value": "string",
    "time_value": "00:00:01",
    "timestamp_value": "2022-11-05T05:39:51.894000+00:00",
    "timestamptz_value": "2022-11-05T05:39:51.894000+00:00",
    "timetz_value": "00:00:01",
    "varchar_value": "string"
  }
]

# validate
data = [
    {
        "primary_key": 0,
        "bool_value": False,
        "char_value": "0",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "0",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "0",
        "varchar_value": "string"
    },
    {
        "primary_key": 1,
        "bool_value": False,
        "char_value": "1",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "1",
        "varchar_value": "string"
    },
    {
        "primary_key": 2,
        "bool_value": True,
        "char_value": "2",
        "date_value": "2022-11-05",
        "float4_value": 0,
        "float8_value": 10.1,
        "int2_value": 0,
        "int4_value": 0,
        "int8_value": 99,
        "text_value": "string",
        "time_value": "1",
        "timestamp_value": "2022-11-05T05:13:59.616Z",
        "timestamptz_value": "2022-11-05T05:13:59.616Z",
        "timetz_value": "2",
        "varchar_value": "string"
    }
]
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory/0?bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In', json=data)

assert x.json() == {
  "primary_key": 0,
  "bool_value": True,
  "char_value": "10",
  "date_value": "2022-11-05",
  "float4_value": 0,
  "float8_value": 0,
  "int2_value": 0,
  "int4_value": 0,
  "int8_value": 0,
  "text_value": "string",
  "time_value": "00:00:01",
  "timestamp_value": "2022-11-05T05:39:51.894000",
  "timestamptz_value": "2022-11-05T05:39:51.894000",
  "timetz_value": "00:00:01",
  "varchar_value": "string"
}
assert x.status_code == 200

# patch
# patch data
x = requests.patch('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____from=0&primary_key____to=0&primary_key____list_____comparison_operator=Not_equal&primary_key____list=1&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In', json= {"varchar_value": "gg"})

assert x.json() == [
  {
    "primary_key": 0,
    "bool_value": True,
    "char_value": "10",
    "date_value": "2022-11-05",
    "float4_value": 0,
    "float8_value": 0,
    "int2_value": 0,
    "int4_value": 0,
    "int8_value": 0,
    "text_value": "string",
    "time_value": "00:00:01",
    "timestamp_value": "2022-11-05T05:39:51.894000",
    "timestamptz_value": "2022-11-05T05:39:51.894000",
    "timetz_value": "00:00:01",
    "varchar_value": "gg"
  }
]
assert x.status_code == 200
#
# validate
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory/0?bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In')
assert x.json() == {
  "primary_key": 0,
  "bool_value": True,
  "char_value": "10",
  "date_value": "2022-11-05",
  "float4_value": 0,
  "float8_value": 0,
  "int2_value": 0,
  "int4_value": 0,
  "int8_value": 0,
  "text_value": "string",
  "time_value": "00:00:01",
  "timestamp_value": "2022-11-05T05:39:51.894000",
  "timestamptz_value": "2022-11-05T05:39:51.894000",
  "timetz_value": "00:00:01",
  "varchar_value": "gg"
}
assert x.status_code == 200


# delete
# delete data
x = requests.delete('http://localhost:8000/my_first_api/test_build_myself_memory?primary_key____from_____comparison_operator=Greater_than_or_equal_to&primary_key____to_____comparison_operator=Less_than_or_equal_to&primary_key____from=0&primary_key____to=0&primary_key____list_____comparison_operator=In&bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In')
assert x.json() == [
  {
    "primary_key": 0,
    "bool_value": True,
    "char_value": "10",
    "date_value": "2022-11-05",
    "float4_value": 0,
    "float8_value": 0,
    "int2_value": 0,
    "int4_value": 0,
    "int8_value": 0,
    "text_value": "string",
    "time_value": "00:00:01",
    "timestamp_value": "2022-11-05T05:39:51.894000",
    "timestamptz_value": "2022-11-05T05:39:51.894000",
    "timetz_value": "00:00:01",
    "varchar_value": "gg"
  }
]
assert x.status_code == 200
#
# validate
x = requests.get('http://localhost:8000/my_first_api/test_build_myself_memory/0?bool_value____list_____comparison_operator=In&char_value____str_____matching_pattern=case_sensitive&char_value____list_____comparison_operator=In&date_value____from_____comparison_operator=Greater_than_or_equal_to&date_value____to_____comparison_operator=Less_than_or_equal_to&date_value____list_____comparison_operator=In&float4_value____from_____comparison_operator=Greater_than_or_equal_to&float4_value____to_____comparison_operator=Less_than_or_equal_to&float4_value____list_____comparison_operator=In&float8_value____from_____comparison_operator=Greater_than_or_equal_to&float8_value____to_____comparison_operator=Less_than_or_equal_to&float8_value____list_____comparison_operator=In&int2_value____from_____comparison_operator=Greater_than_or_equal_to&int2_value____to_____comparison_operator=Less_than_or_equal_to&int2_value____list_____comparison_operator=In&int4_value____from_____comparison_operator=Greater_than_or_equal_to&int4_value____to_____comparison_operator=Less_than_or_equal_to&int4_value____list_____comparison_operator=In&int8_value____from_____comparison_operator=Greater_than_or_equal_to&int8_value____to_____comparison_operator=Less_than_or_equal_to&int8_value____list_____comparison_operator=In&text_value____str_____matching_pattern=case_sensitive&text_value____list_____comparison_operator=In&time_value____from_____comparison_operator=Greater_than_or_equal_to&time_value____to_____comparison_operator=Less_than_or_equal_to&time_value____list_____comparison_operator=In&timestamp_value____from_____comparison_operator=Greater_than_or_equal_to&timestamp_value____to_____comparison_operator=Less_than_or_equal_to&timestamp_value____list_____comparison_operator=In&timestamptz_value____from_____comparison_operator=Greater_than_or_equal_to&timestamptz_value____to_____comparison_operator=Less_than_or_equal_to&timestamptz_value____list_____comparison_operator=In&timetz_value____from_____comparison_operator=Greater_than_or_equal_to&timetz_value____to_____comparison_operator=Less_than_or_equal_to&timetz_value____list_____comparison_operator=In&varchar_value____str_____matching_pattern=case_sensitive&varchar_value____list_____comparison_operator=In')
assert x.status_code == 404


