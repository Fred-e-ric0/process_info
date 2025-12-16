from flask import Flask, request, jsonify
from flask_cors import CORS

from .rng import RNG
from .spin_engine import SpinEngine
from . import config

app = Flask(__name__)
CORS(app)  # permite pedidos do front-end (http://127.0.0.1:5500, etc.)

# cria um motor de roleta único para o servidor
rng = RNG()
spin_engine = SpinEngine(rng, config)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "backend OK"})


@app.route("/spin", methods=["POST"])
def spin():
    """
    Espera um JSON do tipo:
    {
      "amount": 10,
      "number": 17
    }
    """

    data = request.get_json(force=True) or {}
    amount = float(data.get("amount", 0))
    chosen_number = int(data.get("number", -1))

    # 1) simular a roleta
    slot_index = spin_engine.simulate()           # índice 0..36
    landing_number = config.WHEEL[slot_index]     # número real da roleta

    # 2) calcular payout simples: acerta número -> 36x, senão 0
    if chosen_number == landing_number:
        payout = amount * 36
        win = True
    else:
        payout = 0.0
        win = False

    return jsonify({
        "chosen_number": chosen_number,
        "landing_slot_index": slot_index,
        "landing_number": landing_number,
        "bet_amount": amount,
        "payout": payout,
        "win": win
    })


if __name__ == "__main__":
    # correr como módulo: python -m backend.server
    app.run(debug=True)
