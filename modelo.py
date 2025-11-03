from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Produtos(Base):
    __tablename__ = 'Produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    pacotes = relationship("Pacotes", back_populates="produto")

class Espacos(Base):
    __tablename__ = 'Espacos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    localizacao = Column(String(100), nullable=False)
    pacotes = relationship("Pacotes", back_populates="espaco")

class Pacotes(Base):
    __tablename__ = 'Pacotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_pacote = Column(String(100), nullable=False)
    preco_total = Column(Float, nullable=False)
    produto_id = Column(Integer, ForeignKey('Produtos.id'))
    espaco_id = Column(Integer, ForeignKey('Espacos.id'))
    produto = relationship("Produtos", back_populates="pacotes")
    espaco = relationship("Espacos", back_populates="pacotes")