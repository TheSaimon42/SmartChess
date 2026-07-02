import tkinter as tk
import chess
import chess.engine

# =========================
# CONFIG
# =========================

STOCKFISH_PATH = "C:/Users/Saimon/Desktop/ajejed/stockfish/stockfish.exe"

# =========================
# MOTOR Y TABLERO
# =========================

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# =========================
# FUNCIONES
# =========================

def actualizar_tablero():
    tablero_texto.config(state="normal")
    tablero_texto.delete(1.0, tk.END)
    tablero_texto.insert(tk.END, str(board))
    tablero_texto.config(state="disabled")


def evaluar():
    result = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = result["score"].white()

    if score.is_mate():
        mate = score.mate()
        if mate > 0:
            texto_eval.set(f"Mate en {mate} para BLANCAS")
        else:
            texto_eval.set(f"Mate en {abs(mate)} para NEGRAS")
    else:
        cp = score.score()
        if cp is not None:
            valor = cp / 100
            texto_eval.set(f"Eval: {valor:.2f}")
        else:
            texto_eval.set("Sin evaluación")


def hacer_movimiento():
    mov = entrada.get()

    try:
        move = chess.Move.from_uci(mov)

        if move in board.legal_moves:
            board.push(move)
            actualizar_tablero()
            evaluar()
        else:
            texto_eval.set("Movimiento ilegal")

    except:
        texto_eval.set("Formato inválido")

    entrada.delete(0, tk.END)


def resetear():
    global board
    board = chess.Board()
    actualizar_tablero()
    texto_eval.set("Tablero reiniciado")

# =========================
# INTERFAZ
# =========================

ventana = tk.Tk()
ventana.title("Ajedrez con IA")

# Tablero
tablero_texto = tk.Text(ventana, height=10, width=30)
tablero_texto.pack()

# Input
entrada = tk.Entry(ventana)
entrada.pack()

# Botón mover
btn_mover = tk.Button(ventana, text="Mover", command=hacer_movimiento)
btn_mover.pack()

# Botón reset
btn_reset = tk.Button(ventana, text="Reset", command=resetear)
btn_reset.pack()

# Evaluación
texto_eval = tk.StringVar()
label_eval = tk.Label(ventana, textvariable=texto_eval)
label_eval.pack()

# Inicializar
actualizar_tablero()

# Ejecutar
ventana.mainloop()

# Cerrar engine al salir
engine.quit()