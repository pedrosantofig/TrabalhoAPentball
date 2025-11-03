from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class Produto(Base):
    __tablename__ = 'Produtos '
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String(100), nullable=False)
    preco = Column(Integer(100), nullable=False)

class Espaço(Base):
    __tablename__ = 'Espaço'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)