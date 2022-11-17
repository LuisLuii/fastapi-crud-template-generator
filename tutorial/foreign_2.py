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


class BlogPost(Base):
    __tablename__ = "blog_post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, nullable=False)
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
    # DbModel(db_model=Account, prefix="/account", tags=["Account"], foreign_include=[BlogPost],
    #         crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_ONE]),
    DbModel(db_model=BlogPost, prefix="/blog", tags=["Blog Post"], foreign_include=[BlogComment],
            crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_ONE]),
    DbModel(db_model=BlogComment, prefix="/comment", tags=["Blog Comment"], foreign_include=[BlogPost],
            crud_methods=[CrudMethods.FOREIGN_FIND_MANY, CrudMethods.FIND_ONE])]
crud_router_builder(
    db_model_list=model_list,
    # is_async=True,
    # database_url="sqlite+aiosqlite://./test.db",
    is_async=False,
    database_url="sqlite:////Users/luilui/Documents/test.db"
)
