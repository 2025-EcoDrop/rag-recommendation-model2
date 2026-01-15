import decimal

from sqlalchemy import Column, String, BIGINT, Numeric, Boolean, ForeignKey
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Drug(Base):
    __tablename__ = "drug"

    id = Column(BIGINT, primary_key=True, index=True)
    company_name = Column(String)
    product_name = Column(String)

class DrugEmbedding(Base):
    __tablename__ = "drug_embedding"

    id = Column(BIGINT, ForeignKey("drug.id", ondelete="CASCADE"), primary_key=True, index=True)
    embedding = Column(Vector(1024))

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

