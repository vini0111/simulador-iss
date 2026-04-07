async function simular() {

    let copia = JSON.parse(JSON.stringify(jogos));

    const casas = document.querySelectorAll(".placar-casa");
    const foras = document.querySelectorAll(".placar-fora");

    casas.forEach((input, i) => {

        const idx = parseInt(input.dataset.idx);
        const valorCasa = input.value;
        const valorFora = foras[i].value;

        if (copia[idx].gols_casa === null) {

            if (valorCasa !== "" && valorFora !== "") {
                copia[idx].gols_casa = parseInt(valorCasa);
                copia[idx].gols_fora = parseInt(valorFora);
            }

        }
    });

    const res = await fetch("/simular", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(copia)
    });

    const data = await res.json();

    if (!data.A || !data.B) return;

renderTabela("tabelaA", data.A, data.posA, data.probA);
renderTabela("tabelaB", data.B, data.posB, data.probB);
}

function renderTabela(id, dados, posicoes, probabilidades) {

    let html = `
    <tr>
        <th>Jogador</th>
        <th>P</th>
        <th>J</th>
        <th>V</th>
        <th>E</th>
        <th>D</th>
        <th>GP</th>
        <th>GC</th>
        <th>SG</th>
        <th>%</th>
    </tr>
    `;

    dados.forEach((t) => {

        let status = posicoes[t.time];
        let prob = probabilidades[t.time] ?? 0;

        let classe = "";

        if (status.max <= 1) {
            classe = "classificado";
        } else if (status.min > 1) {
            classe = "eliminado";
        } else {
            classe = "disputa";
        }

        html += `
        <tr class="${classe}">
            <td>${t.time}</td>
            <td>${t.pontos}</td>
            <td>${t.jogos}</td>
            <td>${t.vitorias}</td>
            <td>${t.empates}</td>
            <td>${t.derrotas}</td>
            <td>${t.gp}</td>
            <td>${t.gc}</td>
            <td>${t.saldo}</td>
            <td><b>${prob}%</b></td>
        </tr>
        `;
    });

    document.getElementById(id).innerHTML = html;
}

function resetar() {
    location.reload();
}

// 🚀 Executa automaticamente ao carregar a página
window.onload = function() {
    simular();
}

let timeout;

function autoSimular() {
    clearTimeout(timeout);
    timeout = setTimeout(simular, 300);
}

function ativarAutoSimulacao() {

    const inputs = document.querySelectorAll("input");

    inputs.forEach(input => {
        input.addEventListener("input", autoSimular);
    });
}

window.onload = function() {
    simular();
    ativarAutoSimulacao();
}
