from flask import Flask, render_template, request, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Variables globales para mantener el estado entre dispositivos
jugadores = []
fichas = []
posiciones = []
seleccionados = []
turno = 0
serpientes, escaleras = {}, {}

fichas_disponibles = {
    "cazadores": ["cazador1.png", "cazador2.png", "cazador3.png", "cazador4.png", "cazador5.png", "cazador6.png", "cazador7.png", "cazador8.png"],
    "animales": ["animal1.png", "animal2.png", "animal3.png", "animal4.png", "animal5.png", "animal6.png", "animal7.png", "animal8.png"]
}

def generar_tablero():
    serp = {}
    esc = {}

    while len(serp) < 5:
        cabeza = random.randint(2, 99)
        cola = random.randint(1, cabeza - 1)
        if cabeza not in esc and cabeza not in serp and cabeza != 100 and cabeza != 1:
            serp[cabeza] = cola

    while len(esc) < 5:
        inicio = random.randint(2, 98)
        fin = random.randint(inicio + 1, 99)
        if inicio not in serp and inicio not in esc and fin != 100:
            esc[inicio] = fin

    return serp, esc


@app.route("/", methods=["GET", "POST"])
def seleccion():
    global jugadores, fichas, posiciones, seleccionados

    if request.method == "POST":
        nombre = request.form["nombre"]
        ficha = request.form["ficha"]

        if ficha not in seleccionados and nombre not in jugadores:
            jugadores.append(nombre)
            fichas.append(ficha)
            posiciones.append(1)
            seleccionados.append(ficha)

        return redirect(url_for("seleccion"))

    return render_template("seleccion.html",
                           cazadores=fichas_disponibles["cazadores"],
                           animales=fichas_disponibles["animales"],
                           seleccionados=seleccionados,
                           jugadores=jugadores)


@app.route("/jugar")
def juego():
    global jugadores, posiciones, fichas, turno, serpientes, escaleras
    combinados = list(zip(jugadores, posiciones, fichas))

    return render_template("juego.html",
                           jugadores=jugadores,
                           posiciones=posiciones,
                           turno=turno,
                           fichas=fichas,
                           combinados=combinados,
                           serpientes=serpientes,
                           escaleras=escaleras)

@app.route("/lanzar")
def lanzar():
    global posiciones, turno, jugadores, serpientes, escaleras

    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    total_dado = dado1 + dado2

    jugador_actual = jugadores[turno]
    nueva_pos = posiciones[turno] + total_dado

    if nueva_pos >= 100:
        posiciones[turno] = 100
        return {"ganador": jugador_actual, "dado1": dado1, "dado2": dado2}

    if nueva_pos in serpientes:
        nueva_pos = serpientes[nueva_pos]
    elif nueva_pos in escaleras:
        nueva_pos = escaleras[nueva_pos]

    posiciones[turno] = nueva_pos
    turno = (turno + 1) % len(jugadores)

    return {
        "estado": "ok",
        "dado1": dado1,
        "dado2": dado2,
        "jugador": jugador_actual
    }


@app.route("/reiniciar")
def reiniciar():
    global jugadores, fichas, posiciones, seleccionados, turno, serpientes, escaleras
    jugadores.clear()
    fichas.clear()
    posiciones.clear()
    seleccionados.clear()
    turno = 0
    serpientes, escaleras = {}, {}
    return redirect(url_for("seleccion"))


@app.route("/iniciar", methods=["POST"])
def iniciar():
    global turno, serpientes, escaleras
    if len(jugadores) >= 2:
        turno = 0
        serpientes, escaleras = generar_tablero()
        return redirect(url_for("juego"))
    return redirect(url_for("seleccion"))


@app.route("/estado")
def estado():
    return {
        "jugadores": jugadores,
        "fichas": fichas,
        "posiciones": posiciones,
        "turno": turno,
        "serpientes": serpientes,
        "escaleras": escaleras
    }

@app.route("/seleccion_estado")
def seleccion_estado():
    return {
        "seleccionados": seleccionados
    }



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)