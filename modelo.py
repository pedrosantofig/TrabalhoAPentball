<<<<<<< HEAD
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
=======
from sqlalchemy.orm import sessionmaker
from main import Aluno, Base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
aluno1 = Aluno(nome="Lucas", idade=17)
aluno2 = Aluno(nome="Amanda", idade=16)

session.add_all([aluno1, aluno2])
session.commit()
print("Alunos inseridos com sucesso!")
>>>>>>> 033394d278788563f9c0761dc1aa2a2912d8c117
