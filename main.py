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

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    tecnica = db.Column(db.String(120), nullable=False)
    presentes = db.Column(db.Text, nullable=False)

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Alunos - visualizar e cadastrar
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
        novo = Aluno(nome=nome, faixa=faixa, professor=professor, grau1=grau1, grau2=grau2, grau3=grau3, grau4=grau4)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("alunos"))
    lista = Aluno.query.all()
    return render_template("alunos.html", alunos=lista)

# Aulas - visualizar e cadastrar
@app.route("/aulas", methods=["GET", "POST"])
def aulas():
    if request.method == "POST":
        data = request.form["data"]
        tecnica = request.form["tecnica"]
        presentes = ", ".join(request.form.getlist("presentes"))
        nova = Aula(data=data, tecnica=tecnica, presentes=presentes)
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for("aulas"))
    alunos = Aluno.query.all()
    lista = Aula.query.all()
    return render_template("aulas.html", aulas=lista, alunos=alunos)

# Calendário
@app.route("/calendario")
def calendario():
    aulas = Aula.query.order_by(Aula.data.desc()).all()
    return render_template("calendario.html", aulas=aulas)

# Criação de tabelas
with app.app_context():
    db.create_all()

# Execução local ou pelo Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


