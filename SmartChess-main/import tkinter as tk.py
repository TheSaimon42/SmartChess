import tkinter as tk
import chess
import serial


arduino = serial.Serial("COM3",115200)  # TODO: Update COM port and uncomment when Arduino is connected

leds = [(0,0,0)]*64

TAM = 70

ventana = tk.Tk()
ventana.title("Tablero LED")

canvas = tk.Canvas(
    ventana,
    width=8*TAM,
    height=8*TAM
)

canvas.pack()

cursor_x = 0
cursor_y = 7
board = chess.Board()

seleccionada = None
movimientos_posibles = []

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

def xy_a_led(x, y):

    if y % 2 == 0:
        return (7-y)*8 + x
    else:
        return (7-y)*8 + (7-x)
def actualizar_leds():
    global leds
    leds = [(0,0,0)]*64

    for y in range(8):
        for x in range(8):
            n = xy_a_led(x,y)
            if (x+y)%2 == 0:
                leds[n] = (20,20,20)
            if chess.square(x,7-y) in movimientos_posibles:
                leds[n] = (0,255,0)
            if x == cursor_x and y == cursor_y:
                leds[n] = (255,255,0)
            pieza = board.piece_at(chess.square(x,7-y))
            if pieza:
                leds[n] = (0,0,255) if pieza.color == chess.WHITE else (255,0,0)

    datos = bytearray()
    for r,g,b in leds:
        datos.extend([r,g,b])
    
    arduino.write(datos)  # ← esto envía 192 bytes (64 LEDs × 3 canales)

import os

def exportar_wokwi():

    nombre = "wokwi_leds.txt"

    with open(nombre, "w") as f:

        for i,(r,g,b) in enumerate(leds):
            f.write(f"leds[{i}] = CRGB({r},{g},{b});\n")

    print("Generado en:")
    print(os.path.abspath(nombre))

##def enviar_a_tira():

   # datos = bytearray()

    #for r,g,b in leds:

       # datos.extend([r,g,b])

    #arduino.write(datos)

def dibujar():

    canvas.delete("all")

    for y in range(8):

        for x in range(8):

            x1 = x*TAM
            y1 = y*TAM
            x2 = x1+TAM
            y2 = y1+TAM



            # Colores del tablero
            if (x+y)%2 == 0:
                color = "#d9d9d9"
            else:
                color = "#606060"


            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color
            )

            # Movimientos posibles
            if chess.square(x, 7-y) in movimientos_posibles:
                canvas.create_rectangle(
                    x1+8,
                    y1+8,
                    x2-8,
                    y2-8,
                    outline="green",
                    width=4
                )

            # Cursor amarillo
            if x == cursor_x and y == cursor_y:
                canvas.create_rectangle(
                    x1+3,
                    y1+3,
                    x2-3,
                    y2-3,
                    outline="yellow",
                    width=4
                )

            # Pieza en esa casilla
            casilla_chess = chess.square(x, 7-y)

            pieza = board.piece_at(casilla_chess)

            if pieza:

                simbolo = simbolos[pieza.symbol()]

                color_pieza = "blue" if pieza.color == chess.WHITE else "red"

                canvas.create_text(
                    x1+35,
                    y1+35,
                    text=simbolo,
                    fill=color_pieza,
                    font=("Arial", 32)
                )                
                


def tecla(event):

    global cursor_x, cursor_y
    global seleccionada, movimientos_posibles

    if event.keysym == "Left":
        cursor_x = max(0,cursor_x-1)

    elif event.keysym == "Right":
        cursor_x = min(7,cursor_x+1)

    elif event.keysym == "Up":
        cursor_y = max(0,cursor_y-1)

    elif event.keysym == "Down":
        cursor_y = min(7,cursor_y+1)

    elif event.keysym == "Return":

        casilla_actual = chess.square(cursor_x, 7-cursor_y)

        # Seleccionar pieza
        if seleccionada is None:

            pieza = board.piece_at(casilla_actual)

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

    elif event.keysym == "Escape":

        seleccionada = None
        movimientos_posibles = []

    refrescar()

def mostrar_leds():

    print()

    for i in range(64):
        print(leds[i], end=' ')

        if (i+1)%8 == 0:
            print()    

def refrescar():

    actualizar_leds()

    dibujar()

    mostrar_leds()

    exportar_wokwi()
ventana.bind("<Key>", tecla)

refrescar()

ventana.mainloop()