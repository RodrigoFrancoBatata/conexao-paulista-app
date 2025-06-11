from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    faixa = db.Column(db.String(50), nullable=False)
    professor = db.Column(db.String(120), nullable=False)
    grau1 = db.Column(db.Boolean, default=False)
    grau2 = db.Column(db.Boolean, default=False)
    grau3 = db.Column(db.Boolean, default=False)
    grau4 = db.Column(db.Boolean, default=False)
    data_grau1 = db.Column(db.Date)
    data_grau2 = db.Column(db.Date)
    data_grau3 = db.Column(db.Date)
    data_grau4 = db.Column(db.Date)

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    tecnica = db.Column(db.String(120), nullable=False)
    presentes = db.Column(db.Text, nullable=False)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página de alunos (formulário de cadastro)
@app.route("/alunos", methods=["GET", "POST"])
def alunos():
    if request.method == "POST":
        nome = request.form["nome"]
        faixa = request.form["faixa"]
        professor = request.form["professor"]
        grau1 = 'grau1' in request.form
        grau2 = 'grau2' in request.form
        grau3 = 'grau3' in request.form
        grau4 = 'grau4' in request.form
        data_grau1 = request.form.get("data_grau1") or None
        data_grau2 = request.form.get("data_grau2") or None
        data_grau3 = request.form.get("data_grau3") or None
        data_grau4 = request.form.get("data_grau4") or None

        novo = Aluno(
            nome=nome,
            faixa=faixa,
            professor=professor,
            grau1=grau1, grau2=grau2, grau3=grau3, grau4=grau4,
            data_grau1=data_grau1,
            data_grau2=data_grau2,
            data_grau3=data_grau3,
            data_grau4=data_grau4
        )
        db.session.add(novo)
        db.session.commit()
        return redirect("/listar_alunos")
    return render_template("alunos.html")

# Página de aulas
@app.route("/aulas", methods=["GET", "POST"])
def aulas():
    if request.method == "POST":
        data = request.form["data"]
        tecnica = request.form["tecnica"]
        presentes = request.form["presentes"]
        nova_aula = Aula(data=data, tecnica=tecnica, presentes=presentes)
        db.session.add(nova_aula)
        db.session.commit()
        return redirect("/calendario")
    return render_template("aulas.html")

# Calendário de aulas
@app.route("/calendario")
def calendario():
    aulas = Aula.query.order_by(Aula.data.desc()).all()
    return render_template("calendario.html", aulas=aulas)

# Lista de alunos cadastrados
@app.route("/listar_alunos")
def listar_alunos():
    lista = Aluno.query.order_by(Aluno.nome.asc()).all()
    return render_template("listar_alunos.html", alunos=lista)

# Editar aluno
@app.route("/editar_aluno/<int:id>", methods=["GET", "POST"])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)

    if request.method == "POST":
        aluno.nome = request.form["nome"]
        aluno.faixa = request.form["faixa"]
        aluno.professor = request.form["professor"]
        aluno.grau1 = 'grau1' in request.form
        aluno.grau2 = 'grau2' in request.form
        aluno.grau3 = 'grau3' in request.form
        aluno.grau4 = 'grau4' in request.form
        aluno.data_grau1 = request.form.get("data_grau1") or None
        aluno.data_grau2 = request.form.get("data_grau2") or None
        aluno.data_grau3 = request.form.get("data_grau3") or None
        aluno.data_grau4 = request.form.get("data_grau4") or None

        db.session.commit()
        return redirect("/listar_alunos")

    return render_template("editar_aluno.html", aluno=aluno)

# Criação das tabelas (caso necessário)
with app.app_context():
    db.create_all()

# Execução local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
