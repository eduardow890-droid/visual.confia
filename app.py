from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)

app.secret_key = "minha_chave_segura"

# ------------------ LOGIN ------------------

login_admin = "wagner"
senha_admin = "25806491"

login_usuario = "futebol"
senha_usuario = "bangucity"

# ------------------ BANCO ------------------

def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        nascimento TEXT,
        telefone TEXT
    )
    """)

    conexao.commit()
    conexao.close()


def criar_treinos():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos_futebol (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        data TEXT
    )
    """)

    conexao.commit()
    conexao.close()


def criar_registros():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        treino_id INTEGER,
        descricao TEXT,
        pontuacao INTEGER
    )
    """)

    conexao.commit()
    conexao.close()

# ------------------ LOGIN PÁGINA ------------------

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/autenticar", methods=["POST"])
def autenticar():

    login = request.form["login"]
    senha = request.form["senha"]

    if login == login_admin and senha == senha_admin:
        session["usuario"] = "admin"
        return redirect("/sistema")

    elif login == login_usuario and senha == senha_usuario:
        session["usuario"] = "user"
        return redirect("/sistema")

    else:
        return render_template("login.html", erro="Acesso negado")

# ------------------ PROTEÇÃO ------------------

def logado():
    return "usuario" in session

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ------------------ SISTEMA ------------------

@app.route("/sistema")
def sistema():

    if not logado():
        return redirect("/")

    return render_template("sistema.html")

# ------------------ CADASTRO ------------------

@app.route("/cadastro")
def cadastro():

    if not logado():
        return redirect("/")

    return render_template("cadastro.html")


@app.route("/salvar", methods=["POST"])
def salvar():

    nome = request.form["nome"]
    cpf = request.form["cpf"]
    nascimento = request.form["nascimento"]
    telefone = request.form["telefone"]

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO usuarios (nome, cpf, nascimento, telefone)
    VALUES (?, ?, ?, ?)
    """, (nome, cpf, nascimento, telefone))

    conexao.commit()
    conexao.close()

    return redirect("/sistema")

# ------------------ TREINOS ------------------

@app.route("/treinos")
def treinos():

    if not logado():
        return redirect("/")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT nome, descricao, data FROM treinos_futebol")
    treinos = cursor.fetchall()

    conexao.close()

    return render_template("treinos.html", treinos=treinos)


@app.route("/salvar_treino", methods=["POST"])
def salvar_treino():

    nome = request.form["nome_treino"]
    descricao = request.form["descricao"]
    data = request.form["data"]

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO treinos_futebol (nome, descricao, data)
    VALUES (?, ?, ?)
    """, (nome, descricao, data))

    conexao.commit()
    conexao.close()

    return redirect("/treinos")

# ------------------ REGISTRO ------------------

@app.route("/registro")
def registro():

    if not logado():
        return redirect("/")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome FROM usuarios")
    alunos = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM treinos_futebol")
    treinos = cursor.fetchall()

    cursor.execute("SELECT aluno_id, pontuacao FROM registros")
    registros = cursor.fetchall()

    conexao.close()

    return render_template(
        "registro.html",
        alunos=alunos,
        treinos=treinos,
        registros=registros
    )


@app.route("/salvar_registro", methods=["POST"])
def salvar_registro():

    aluno_id = request.form["aluno"]
    treino_id = request.form["treino"]
    descricao = request.form["descricao"]
    pontuacao = request.form["pontuacao"]

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO registros (aluno_id, treino_id, descricao, pontuacao)
    VALUES (?, ?, ?, ?)
    """, (aluno_id, treino_id, descricao, pontuacao))

    conexao.commit()
    conexao.close()

    return redirect("/registro")

# ------------------ START ------------------

if __name__ == "__main__":
    criar_banco()
    criar_treinos()
    criar_registros()
    app.run(debug=True)