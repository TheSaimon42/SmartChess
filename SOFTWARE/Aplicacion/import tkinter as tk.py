import tkinter as tk
import chess
import serial
import time



PUERTO = "COM3"
BAUDIOS = 115200
TAM = 70

arduino = serial.Serial(PUERTO, BAUDIOS)
time.sleep(3)


board = chess.Board()

cursor_x = 0
cursor_y = 7

seleccionada = None
movimientos_posibles = []

leds = [(0,0,0)] * 64

simbolos = {
    'P':'♙',
    'N':'♘',
    'B':'♗',
    'R':'♖',
    'Q':'♕',
    'K':'♔',

    'p':'♟',
    'n':'♞',
    'b':'♝',
    'r':'♜',
    'q':'♛',
    'k':'♚'
}

# ---------------------------
# VENTANA
# ---------------------------

ventana = tk.Tk()
ventana.title("Tablero Ajedrez LED")

canvas = tk.Canvas(
    ventana,
    width=8*TAM,
    height=8*TAM
)

canvas.pack()

# ---------------------------
# CONVERSION XY -> LED
# ---------------------------

def xy_a_led(x, y):

    fila = 7 - y

    if fila % 2 == 0:
        return fila * 8 + x

    return fila * 8 + (7 - x)


def actualizar_leds():

    global leds

    leds = [(20,20,20)] * 64

    for y in range(8):
        for x in range(8):

            n = xy_a_led(x,y)

            pieza = board.piece_at(
                chess.square(x,7-y)
            )

            if pieza:

                if pieza.color == chess.WHITE:
                    leds[n] = (0,0,255)
                else:
                    leds[n] = (255,0,0)

    leds[xy_a_led(cursor_x,cursor_y)] = (255,255,0)

def enviar_a_tira():

    datos = bytearray()

    for r,g,b in leds:
        datos.extend([r,g,b])

    print("Bytes:", len(datos))
    print("Primer LED:", leds[0])

    print("LED 0:", leds[0])
    print("LED 1:", leds[1])
    print("LED 2:", leds[2])
    print("LED 3:", leds[3])
    print("LED 4:", leds[4])

    arduino.write(datos)

# ---------------------------
# DIBUJAR
# ---------------------------

def dibujar():

    print("Dibujando")

    canvas.delete("all")

    for y in range(8):

        for x in range(8):

            

            x1 = x*TAM
            y1 = y*TAM
            x2 = x1 + TAM
            y2 = y1 + TAM

            

            color = "#d9d9d9" if (x+y)%2 == 0 else "#606060"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color
            )

            # movimientos posibles
            if chess.square(x,7-y) in movimientos_posibles:

                canvas.create_rectangle(
                    x1+8,
                    y1+8,
                    x2-8,
                    y2-8,
                    outline="green",
                    width=4
                )

            # cursor
            if x == cursor_x and y == cursor_y:

                canvas.create_rectangle(
                    x1+3,
                    y1+3,
                    x2-3,
                    y2-3,
                    outline="yellow",
                    width=4
                )

            casilla_chess = chess.square(x,7-y)

            pieza = board.piece_at(casilla_chess)

            if pieza:

                simbolo = simbolos[pieza.symbol()]

                color_pieza = (
                    "blue"
                    if pieza.color == chess.WHITE
                    else "red"
                )

                canvas.create_text(
                    x1 + TAM//2,
                    y1 + TAM//2,
                    text=simbolo,
                    fill=color_pieza,
                    font=("Arial",32)
                )

# ---------------------------
# REFRESCAR
# ---------------------------

def refrescar():

    print("Refrescando")

    actualizar_leds()

    dibujar()

    enviar_a_tira()

# ---------------------------
# TECLADO
# ---------------------------

def tecla(event):

    global cursor_x
    global cursor_y
    global seleccionada
    global movimientos_posibles

    if event.keysym == "Left":
        cursor_x = max(0, cursor_x-1)

    elif event.keysym == "Right":
        cursor_x = min(7, cursor_x+1)

    elif event.keysym == "Up":
        cursor_y = max(0, cursor_y-1)

    elif event.keysym == "Down":
        cursor_y = min(7, cursor_y+1)

    elif event.keysym == "Escape":

        seleccionada = None
        movimientos_posibles = []

    elif event.keysym == "Return":

        casilla_actual = chess.square(
            cursor_x,
            7-cursor_y
        )

        # Seleccionar pieza
        if seleccionada is None:

            pieza = board.piece_at(
                casilla_actual
            )

            if pieza:

                seleccionada = casilla_actual

                movimientos_posibles = []

                for movimiento in board.legal_moves:

                    if movimiento.from_square == seleccionada:

                        movimientos_posibles.append(
                            movimiento.to_square
                        )

        # Intentar mover
        else:

            movimiento = chess.Move(
                seleccionada,
                casilla_actual
            )

            if movimiento in board.legal_moves:

                board.push(movimiento)

            seleccionada = None
            movimientos_posibles = []

    refrescar()

# ---------------------------
# INICIO
# ---------------------------

ventana.bind("<Key>", tecla)

refrescar()

ventana.mainloop()