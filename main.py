from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Aula
class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    tecnica = db.Column(db.String(120), nullable=False)
    presentes = db.Column(db.Text, nullable=False)

# Criar tabelas antes do primeiro request
@app.before_first_request
def create_tables():
    db.create_all()

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Rota para alunos
@app.route("/alunos")
def alunos():
    return render_template("alunos.html")

# Rota para aulas
@app.route("/aulas")
def aulas():
    return render_template("aulas.html")

# Rota para calendário
@app.route("/calendario")
def calendario():
    aulas = Aula.query.all()
    return render_template("calendario.html", aulas=aulas)

# Execução local ou via Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
