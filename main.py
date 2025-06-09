from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    faixa = db.Column(db.String(50), nullable=False)
    professor = db.Column(db.String(120), nullable=False)
    graus = db.Column(db.String(10), default="")

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    tecnica = db.Column(db.String(120), nullable=False)
    presentes = db.Column(db.Text, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/alunos")
def alunos():
    return render_template("alunos.html")

@app.route("/adicionar_aluno", methods=["POST"])
def adicionar_aluno():
    nome = request.form["nome"]
    faixa = request.form["faixa"]
    professor = request.form["professor"]
    graus = ",".join(request.form.getlist("graus"))
    novo = Aluno(nome=nome, faixa=faixa, professor=professor, graus=graus)
    db.session.add(novo)
    db.session.commit()
    return redirect("/alunos")

@app.route("/aulas")
def aulas():
    alunos = Aluno.query.all()
    return render_template("aulas.html", alunos=alunos)

@app.route("/registrar_aula", methods=["POST"])
def registrar_aula():
    data = request.form["data"]
    tecnica = request.form["tecnica"]
    presentes = ",".join(request.form.getlist("presentes"))
    nova = Aula(data=data, tecnica=tecnica, presentes=presentes)
    db.session.add(nova)
    db.session.commit()
    return redirect("/aulas")

@app.route("/calendario")
def calendario():
    aulas = Aula.query.all()
    return render_template("calendario.html", aulas=aulas)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


