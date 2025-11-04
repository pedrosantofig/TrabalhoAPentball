from sqlalchemy.orm import sessionmaker
from modelo import Aluno, Base
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