from .db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship

class Categories(Base):
    __tablename__ = 'categories'
    
    category_id = Column('id', Integer, primary_key=True)
    name = Column(String(length=100), nullable=False, unique=True)
    description = Column(Text)
    
    products = relationship('Products', back_populates='category')
    

class Products(Base):
    __tablename__ = 'products'
    
    product_id = Column('id', Integer, primary_key=True)
    name = Column(String(length=200), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True, server_default='true')
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    
    category = relationship('Categories', back_populates='products')