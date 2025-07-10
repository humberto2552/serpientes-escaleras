
function construirTablero(data) {
    const grid = document.querySelector(".board-grid");
    grid.innerHTML = "";

    for (let fila = 9; fila >= 0; fila--) {
        const row = document.createElement("div");
        row.className = "board-row";
        if (fila % 2 === 1) row.classList.add("reverse");

        for (let col = 0; col < 10; col++) {
            let i;
            if (fila % 2 === 0) {
                i = fila * 10 + col + 1;
            } else {
                i = (fila + 1) * 10 - col;
            }

            let clase = "board-cell";
            if (data.serpientes[i]) clase += " snake";
            if (data.escaleras[i]) clase += " ladder";
            if (data.posiciones[data.turno] === i) clase += " actual";
            if (i === 1) clase += " start";
            if (i === 100) clase += " goal";

            const cell = document.createElement("div");
            cell.className = clase;
            cell.dataset.number = i;
            cell.innerHTML = i;

            if (i === 1) {
                const inicio = document.createElement("div");
                inicio.className = "inicio";
                inicio.textContent = "INICIO";
                cell.appendChild(inicio);
            }

            if (i === 100) {
                const meta = document.createElement("div");
                meta.className = "meta";
                meta.textContent = "META";
                cell.appendChild(meta);
            }

            if (data.serpientes[i]) {
                const img = document.createElement("img");
                img.src = "/static/img/serpiente.png";
                img.style = "position:absolute;top:5px;left:5px;width:30px;";
                cell.appendChild(img);
            }

            if (data.escaleras[i]) {
                const img = document.createElement("img");
                img.src = "/static/img/escalera.png";
                img.style = "position:absolute;bottom:5px;right:5px;width:30px;";
                cell.appendChild(img);
            }

            const jugadoresEnCasilla = data.jugadores
                .map((nombre, idx) => ({
                    nombre,
                    pos: data.posiciones[idx],
                    ficha: data.fichas[idx]
                }))
                .filter(j => j.pos === i);

            if (jugadoresEnCasilla.length > 0) {
                const divJugadores = document.createElement("div");
                divJugadores.className = "jugador";
                jugadoresEnCasilla.forEach(j => {
                    const img = document.createElement("img");
                    img.src = `/static/img/${j.ficha}`;
                    img.width = 25;
                    img.style.transition = "transform 0.4s ease";
                    img.style.transform = "scale(1.2)";
                    divJugadores.appendChild(img);
                });
                cell.appendChild(divJugadores);
            }

            row.appendChild(cell);
        }

        grid.appendChild(row);
    }
}
