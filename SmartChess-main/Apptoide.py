from flask import Flask, request, jsonify, render_template
import chess
import chess.engine

app = Flask(__name__)

STOCKFISH_PATH = "C:/Users/Saimon/Desktop/ajejed/stockfish/stockfish.exe"

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    movimiento = data.get("move")

    try:
        move = chess.Move.from_uci(movimiento)

        if move in board.legal_moves:
            board.push(move)

            result = engine.analyse(board, chess.engine.Limit(time=0.1))
            score = result["score"].white()

            return jsonify({
                "ok": True,
                "board": str(board),
                "eval": str(score)
            })

        else:
            return jsonify({"ok": False, "error": "Movimiento ilegal"})

    except:
        return jsonify({"ok": False, "error": "Formato inválido"})


@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = chess.Board()
    return jsonify({"ok": True})


app.run(host="0.0.0.0", port=5000)