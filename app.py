from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from modelo import Agendamento, Base, Produtos, Espacos, Pacotes, Usuario
import os
from dotenv import load_dotenv
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Banco de dados SQL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
print('criando tabela')
Base.metadata.create_all(engine)
print('tabela adicionada')
Session = sessionmaker(bind=engine)
session = Session()
# -------------------- ROTAS --------------------

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/servicos')
def addServico():
    return render_template('addServico.html')
@app.route('/consultar')
def consultar():
    return render_template('consultar.html')
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        data = request.form['data']        # Vem como string 'YYYY-MM-DD'
        hora = request.form['hora']        # Vem como string 'HH:MM'
        servico = request.form['servico']
        jogadores = int(request.form['jogadores'])

        # Cria um novo objeto Agendamento
        novo_agendamento = Agendamento(
            nome=nome,
            data=data,
            hora=hora,
            servico=servico,
            jogadores=jogadores
        )

        # Salva no banco
        session.add(novo_agendamento)
        session.commit()

        # Redireciona para a página de agendamentos
        return redirect(url_for('mostrar_agendamentos'))

    # Se for GET, só renderiza a página do formulário
    return render_template('agendar.html')

@app.route('/agendamentos')
def mostrar_agendamentos():
    agendamentos = session.query(Agendamento).all()
    return render_template('agendamentos.html', agendamentos=agendamentos)

@app.route('/agendamento/editar/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    ag = session.query(Agendamento).get(id)
    if request.method == 'POST':
        ag.nome = request.form['nome']
        ag.data = request.form['data']
        ag.hora = request.form['hora']
        ag.servico = request.form['servico']
        ag.jogadores = request.form['jogadores']
        session.commit()
        return redirect(url_for('mostrar_agendamentos'))
    return render_template('editar_agendamento.html', agendamento=ag)

# Deletar agendamento
@app.route('/agendamento/deletar/<int:id>')
def deletar_agendamento(id):
    ag = session.query(Agendamento).get(id)
    session.delete(ag)
    session.commit()
    return redirect(url_for('mostrar_agendamentos'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()
        if senha == "123":
            return redirect(url_for('cadastro'))
        else:
            flash("Usuário ou senha inválidos!", "error")
    return render_template('login.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    session = Session()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()

        # Redireciona ou mostra uma mensagem de sucesso
        return render_template('cadastrarUser.html', mensagem='Usuário cadastrado com sucesso!')

    # Se for GET, só exibe o HTML do formulário
    return render_template('cadastrarUser.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastroProdutos():
    produtos = session.query(Produtos).all()
    espacos = session.query(Espacos).all()
    pacotes = session.query(Pacotes).all()
    return render_template('cadastro.html', produtos=produtos, espacos=espacos, pacotes=pacotes)

# Rotas CRUD de Produtos
@app.route('/produto/add', methods=['GET','POST'])
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