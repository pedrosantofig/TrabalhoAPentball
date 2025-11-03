from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Base, Produtos, Espacos, Pacotes
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Banco de dados SQLite
DATABASE_URL= os.path.join(os.path.dirname(__file__), "locaplay.db")
engine = create_engine(f"sqlite:///{DATABASE_URL}", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# -------------------- ROTAS --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if senha == "123":
            return redirect(url_for('cadastro'))
        else:
            flash("Usuário ou senha inválidos!", "error")
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    produtos = session.query(Produtos).all()
    espacos = session.query(Espacos).all()
    pacotes = session.query(Pacotes).all()
    return render_template('cadastro.html', produtos=produtos, espacos=espacos, pacotes=pacotes)

# Rotas CRUD de Produtos
@app.route('/produto/add', methods=['POST'])
def add_produto():
    nome = request.form['nome_produto']
    preco = float(request.form['preco'])
    novo = Produtos(nome_produto=nome, preco=preco)
    session.add(novo)
    session.commit()
    flash("Produto adicionado!", "success")
    return redirect(url_for('cadastro'))

# Rotas CRUD de Espaços
@app.route('/espaco/add', methods=['POST'])
def add_espaco():
    nome = request.form['nome_espaco']
    preco = float(request.form['preco_espaco'])
    local = request.form['localizacao']
    novo = Espacos(nome=nome, preco=preco, localizacao=local)
    session.add(novo)
    session.commit()
    flash("Espaço adicionado!", "success")
    return redirect(url_for('cadastro'))

# Rotas CRUD de Pacotes
@app.route('/pacote/add', methods=['POST'])
def add_pacote():
    nome = request.form['nome_pacote']
    preco_total = float(request.form['preco_total'])
    produto_id = int(request.form['produto_id'])
    espaco_id = int(request.form['espaco_id'])
    novo = Pacotes(nome_pacote=nome, preco_total=preco_total, produto_id=produto_id, espaco_id=espaco_id)
    session.add(novo)
    session.commit()
    flash("Pacote adicionado!", "success")
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)