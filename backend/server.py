from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

from .rng import RNG
from .spin_engine import SpinEngine
from . import config

# Path to the frontend directory (use absolute path to avoid access issues)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'front_end'

app = Flask(__name__)
CORS(app)  # permite pedidos do front-end (http://127.0.0.1:5500, etc.)

print(f"[DEBUG] Frontend directory: {FRONTEND_DIR}")
print(f"[DEBUG] Frontend exists: {FRONTEND_DIR.exists()}")

# cria um motor de roleta único para o servidor
rng = RNG()
spin_engine = SpinEngine(rng, config)


@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "backend OK"})


@app.route("/api/spin", methods=["POST"])
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


# Static file serving routes (defined after API routes to avoid conflicts)
@app.route("/")
def serve_index():
    """Serve the frontend index.html"""
    index_path = FRONTEND_DIR / 'index.html'
    print(f"[DEBUG] Serving index from: {index_path}")
    return send_file(index_path)


@app.route("/<path:path>")
def serve_static(path):
    """Serve static files from the frontend directory"""
    # Skip API routes (they're handled above)
    if path.startswith('api/'):
        return jsonify({"error": "Not found"}), 404
    file_path = FRONTEND_DIR / path
    print(f"[DEBUG] Serving static file: {file_path}")
    if file_path.exists() and file_path.is_file():
        return send_file(file_path)
    return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    # correr como módulo: python -m backend.server
    # Using port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000
    app.run(host='0.0.0.0', port=5001, debug=True)
