from flask import Flask, render_template, request, jsonify
import itertools
import pandas as pd
from dados import jogos

app = Flask(__name__)

def calcular_classificacao(jogos):
    grupos = {"A": {}, "B": {}}

    # 🔹 Monta tabela base
    for j in jogos:
        if j["gols_casa"] is None:
            continue

        g = j["grupo"]

        for time in [j["casa"], j["fora"]]:
            if time not in grupos[g]:
                grupos[g][time] = {
                    "time": time,
                    "pontos": 0,
                    "jogos": 0,
                    "vitorias": 0,
                    "empates": 0,
                    "derrotas": 0,
                    "gp": 0,
                    "gc": 0
                }

        casa = grupos[g][j["casa"]]
        fora = grupos[g][j["fora"]]

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

    # 🔹 Monta resultado final
    resultado = {}

    for g in ["A", "B"]:
        lista = list(grupos[g].values())

        for t in lista:
            t["saldo"] = t["gp"] - t["gc"]

        lista.sort(key=lambda x: (-x["pontos"], -x["vitorias"], -x["saldo"]))

        resultado[g] = lista

    return resultado

def analisar_possibilidades(jogos, grupo):

    jogos_grupo = [j for j in jogos if j["grupo"] == grupo]
    jogos_pendentes = [j for j in jogos_grupo if j["gols_casa"] is None]

    resultados_possiveis = [(0,0),(1,0),(0,1),(1,1)]

    classificacoes = []

    for combinacao in itertools.product(resultados_possiveis, repeat=len(jogos_pendentes)):

        copia = [j.copy() for j in jogos]

        idx = 0
        for j in copia:
            if j["grupo"] == grupo and j["gols_casa"] is None:
                j["gols_casa"], j["gols_fora"] = combinacao[idx]
                idx += 1

        tabela = calcular_classificacao(copia)[grupo]

        classificacoes.append([t["time"] for t in tabela])

    posicoes = {}

    for ordem in classificacoes:
        for i, time in enumerate(ordem):

            if time not in posicoes:
                posicoes[time] = {"min": 999, "max": -1}

            posicoes[time]["min"] = min(posicoes[time]["min"], i)
            posicoes[time]["max"] = max(posicoes[time]["max"], i)

    return posicoes

def calcular_probabilidades(jogos, grupo):

    jogos_grupo = [j for j in jogos if j["grupo"] == grupo]
    jogos_pendentes = [j for j in jogos_grupo if j["gols_casa"] is None]

    resultados_possiveis = [(0,0),(1,0),(0,1),(1,1)]

    classificacoes = []

    for combinacao in itertools.product(resultados_possiveis, repeat=len(jogos_pendentes)):

        copia = [j.copy() for j in jogos]

        idx = 0
        for j in copia:
            if j["grupo"] == grupo and j["gols_casa"] is None:
                j["gols_casa"], j["gols_fora"] = combinacao[idx]
                idx += 1

        tabela = calcular_classificacao(copia)[grupo]

        classificacoes.append([t["time"] for t in tabela])

    total = len(classificacoes)

    contagem = {}

    for ordem in classificacoes:
        for i, time in enumerate(ordem):

            if time not in contagem:
                contagem[time] = 0

            if i < 2:  # top 2
                contagem[time] += 1

    probabilidades = {}

    for time in contagem:
        probabilidades[time] = round((contagem[time] / total) * 100, 1)

    return probabilidades

@app.route("/")
def index():
    try:
        return render_template("index.html", jogos=jogos)
    except Exception as e:
        return f"Erro ao carregar página: {e}"


@app.route("/simular", methods=["POST"])
def simular():
    jogos = request.json

    classificacao = calcular_classificacao(jogos)

    posA = analisar_possibilidades(jogos, "A")
    posB = analisar_possibilidades(jogos, "B")

    probA = calcular_probabilidades(jogos, "A")
    probB = calcular_probabilidades(jogos, "B")

    return jsonify({
        "A": classificacao["A"],
        "B": classificacao["B"],
        "posA": posA,
        "posB": posB,
        "probA": probA,
        "probB": probB
    })


if __name__ == "__main__":
    print("Servidor iniciando...")
    app.run(debug=True)
