from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ALUNOS_PATH = "data/alunos.json"
AULAS_PATH = "data/aulas.json"
os.makedirs("data", exist_ok=True)

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
    graus = request.form.getlist("graus")

    novo_aluno = {
        "nome": nome,
        "faixa": faixa,
        "professor": professor,
        "graus": graus
    }

    alunos = []
    if os.path.exists(ALUNOS_PATH):
        with open(ALUNOS_PATH, "r", encoding="utf-8") as f:
            alunos = json.load(f)

    alunos.append(novo_aluno)
    with open(ALUNOS_PATH, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

    return redirect("/alunos")

@app.route("/aulas")
def aulas():
    alunos = []
    if os.path.exists(ALUNOS_PATH):
        with open(ALUNOS_PATH, "r", encoding="utf-8") as f:
            alunos = json.load(f)
    return render_template("aulas.html", alunos=alunos)

@app.route("/registrar_aula", methods=["POST"])
def registrar_aula():
    data = request.form["data"]
    tecnica = request.form["tecnica"]
    presentes = request.form.getlist("presentes")

    nova_aula = {
        "data": data,
        "tecnica": tecnica,
        "presentes": presentes
    }

    aulas = []
    if os.path.exists(AULAS_PATH):
        with open(AULAS_PATH, "r", encoding="utf-8") as f:
            aulas = json.load(f)

    aulas.append(nova_aula)
    with open(AULAS_PATH, "w", encoding="utf-8") as f:
        json.dump(aulas, f, ensure_ascii=False, indent=2)

    return redirect("/aulas")

@app.route("/calendario")
def calendario():
    aulas = []
    if os.path.exists(AULAS_PATH):
        with open(AULAS_PATH, "r", encoding="utf-8") as f:
            aulas = json.load(f)
    return render_template("calendario.html", aulas=aulas)

if __name__ == "__main__":
    app.run(debug=True)