import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, \
    Numeric, SmallInteger, String, Text, Time, UniqueConstraint, LargeBinary, text, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INTERVAL, JSON, UUID
from sqlalchemy.orm import declarative_base

from fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
from fastapi_quickcrud_codegen.misc.type import SqlType


Base = declarative_base()
metadata = Base.metadata

'''
-- public.test_uuid_primary_sync definition

-- Drop table

-- DROP TABLE public.test_uuid_primary_sync;

CREATE TABLE public.test_uuid_primary_sync (
	primary_key uuid NOT NULL,
	bool_value bool NOT NULL DEFAULT false,
	char_value bpchar(10) NULL,
	date_value date NULL DEFAULT now(),
	float4_value float8 NOT NULL,
	float8_value float8 NOT NULL DEFAULT 10.10,
	int2_value int2 NOT NULL,
	int4_value int4 NOT NULL,
	int8_value int8 NULL DEFAULT 99,
	interval_value interval NULL,
	json_value json NULL,
	jsonb_value jsonb NULL,
	numeric_value numeric NULL,
	text_value text NULL,
	time_value time NULL,
	timestamp_value timestamp NULL,
	timestamptz_value timestamptz NULL,
	timetz_value timetz NULL,
	varchar_value varchar NULL,
	array_value _int4 NULL,
	array_str__value _varchar NULL,
	CONSTRAINT test_uuid_primary_sync_pkey PRIMARY KEY (primary_key),
	CONSTRAINT test_uuid_primary_sync_primary_key_int4_value_float4_value_key UNIQUE (primary_key, int4_value, float4_value)
);
'''
class TestUuidPrimarySync(Base):
    __tablename__ = 'test_uuid_primary_sync'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )

    primary_key = Column(UUID(as_uuid=True), primary_key=True)
    bool_value = Column(Boolean, nullable=False, server_default=text('false'))
    float4_value = Column(Float(53), nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text('10.10'))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text('now()'))
    int8_value = Column(BigInteger, server_default=text('99'))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB)
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


crud_router_builder(
    db_model_list=[
        {
            "db_model": TestUuidPrimarySync,
            "prefix": "/uuid_pk_api",
            "tags": ["sample api"],
        }
    ],
    crud_methods=[CrudMethods.FIND_ONE, CrudMethods.FIND_MANY, CrudMethods.CREATE_MANY, CrudMethods.UPDATE_ONE, CrudMethods.PATCH_ONE, CrudMethods.DELETE_ONE, CrudMethods.DELETE_MANY],
    is_async=False,
    database_url="postgresql://postgres:1234@127.0.0.1:5432/postgres"
)
