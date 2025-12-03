import decimal

from sqlalchemy import Column, String, BIGINT, Numeric, Boolean
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DrugEmbedding(Base):
    __tablename__ = "drug_embedding"

    id = Column(BIGINT, primary_key=True, index=True)
    company_name = Column(String)
    product_name = Column(String)
    embedding = Column(Vector(1024))

class Drug(Base):
    __tablename__ = "drug"

    id = Column(BIGINT, primary_key=True, index=True)
    company_name = Column(String)
    product_name = Column(String)
    efficacy = Column(String)
    use = Column(String)
    caution_warn = Column(String)
    caution = Column(String)
    interaction = Column(String)
    side_effect = Column(String)

class Review(Base):
    __tablename__ = "review"

    id = Column(BIGINT, primary_key=True, index=True)
    author_id = Column(BIGINT, index=True)
    product_name = Column(String)
    review = Column(String)
    rating = Column(Numeric)
    public_data = Column(Boolean)
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)

