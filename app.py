from flask import Flask, render_template, request, jsonify
import pandas as pd
from dados import jogos

app = Flask(__name__)

def calcular_classificacao(jogos):
    grupos = {"A": {}, "B": {}}

    for j in jogos:
        if j["gols_casa"] is None:
            continue

        grupo = j["grupo"]

        for time in [j["casa"], j["fora"]]:
            if time not in grupos[grupo]:
                grupos[grupo][time] = {
                    "time": time,
                    "pontos": 0,
                    "jogos": 0,
                    "vitorias": 0,
                    "empates": 0,
                    "derrotas": 0,
                    "gp": 0,
                    "gc": 0
                }

        casa = grupos[grupo][j["casa"]]
        fora = grupos[grupo][j["fora"]]

        casa["jogos"] += 1
        fora["jogos"] += 1

        casa["gp"] += j["gols_casa"]
        casa["gc"] += j["gols_fora"]

        fora["gp"] += j["gols_fora"]
        fora["gc"] += j["gols_casa"]

        if j["gols_casa"] > j["gols_fora"]:
            casa["pontos"] += 3
            casa["vitorias"] += 1
            fora["derrotas"] += 1
        elif j["gols_casa"] < j["gols_fora"]:
            fora["pontos"] += 3
            fora["vitorias"] += 1
            casa["derrotas"] += 1
        else:
            casa["pontos"] += 1
            fora["pontos"] += 1
            casa["empates"] += 1
            fora["empates"] += 1

    resultado = {}

    for grupo in ["A", "B"]:
        lista = list(grupos[grupo].values())

        for t in lista:
            t["saldo"] = t["gp"] - t["gc"]

        lista.sort(key=lambda x: (-x["pontos"], -x["vitorias"], -x["saldo"]))

        resultado[grupo] = lista

    return resultado


@app.route("/")
def index():
    try:
        return render_template("index.html", jogos=jogos)
    except Exception as e:
        return f"Erro ao carregar página: {e}"


@app.route("/simular", methods=["POST"])
def simular():
    dados = request.json
    resultado = calcular_classificacao(dados)
    return jsonify(resultado)


if __name__ == "__main__":
    print("Servidor iniciando...")
    app.run(debug=True)