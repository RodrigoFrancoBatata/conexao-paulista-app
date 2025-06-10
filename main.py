from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELOS
class Aluno(db.Model):
    __tablename__ = 'aluno'

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

@app.route("/")
def index():
    return render_template("index.html")

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

        # Convertendo para tipo date se existir
        from datetime import datetime
        def parse_date(d): return datetime.strptime(d, "%Y-%m-%d").date() if d else None

        novo = Aluno(
            nome=nome,
            faixa=faixa,
            professor=professor,
            grau1=grau1,
            grau2=grau2,
            grau3=grau3,
            grau4=grau4,
            data_grau1=parse_date(data_grau1),
            data_grau2=parse_date(data_grau2),
            data_grau3=parse_date(data_grau3),
            data_grau4=parse_date(data_grau4)
        )

        db.session.add(novo)
        db.session.commit()
        return redirect("/alunos")

    lista = Aluno.query.all()
    return render_template("alunos.html", alunos=lista)


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

@app.route("/calendario")
def calendario():
    aulas = Aula.query.order_by(Aula.data.desc()).all()
    return render_template("calendario.html", aulas=aulas)

# Criação de tabelas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
