async function simular() {

    let copia = JSON.parse(JSON.stringify(jogos));

    copia.forEach((j, i) => {
        if (j.gols_casa === null) {
            let c = document.getElementById("c"+(i+1)).value;
            let f = document.getElementById("f"+(i+1)).value;

            if (c !== "" && f !== "") {
                j.gols_casa = parseInt(c);
                j.gols_fora = parseInt(f);
            }
        }
    });

    const res = await fetch("/simular", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(copia)
    });

    const data = await res.json();

    console.log("RETORNO BACKEND:", data);

    if (!data.A || !data.B) {
        alert("Erro: backend não retornou os grupos corretamente");
        return;
    }

    renderTabela("tabelaA", data.A);
    renderTabela("tabelaB", data.B);
}


// 🔥 FUNÇÃO QUE ESTAVA FALTANDO
function renderTabela(id, dados) {

    let tabela = document.getElementById(id);

    tabela.innerHTML = `
        <tr>
            <th>Jogador</th>
            <th>Pts</th>
            <th>J</th>
            <th>V</th>
            <th>E</th>
            <th>D</th>
            <th>GP</th>
            <th>GC</th>
            <th>SG</th>
        </tr>
    `;

    dados.forEach((t, i) => {

        let classe = i < 2 ? "classificado" : "";

        tabela.innerHTML += `
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
            </tr>
        `;
    });
}

function resetar() {
    location.reload();
}

// 🚀 Executa automaticamente ao carregar a página
window.onload = function() {
    simular();
}