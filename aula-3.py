from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from modelo import Aluno
import os
from dotenv import load_dotenv
# Carrega variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") # Pegando a string de conexão
# Setup do Flask
app = Flask(__name__)
CORS(app) # Permite chamadas de fora (como de um HTML/JS)
# Conexão com o banco de dados
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    session = Session()
    alunos = session.query(Aluno).all()
    resultado = [ {"id": a.id, "nome": a.nome, "idade": a.idade} for a in alunos ]
    session.close()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)