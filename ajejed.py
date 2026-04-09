import chess
import chess.engine

STOCKFISH_PATH = "C:/Users/Saimon/Desktop/ajejed/stockfish/stockfish.exe"



board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

print("=== TABLERO INICIAL ===")
print(board)



def movimientos_legales(origen): 
    print(f"\nMovimientos posibles desde {origen}:") 
    for move in board.legal_moves:
        if move.uci().startswith(origen):
            print(move.uci())


def evaluar_posicion():
    result = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = result["score"].white()
    
    if score.is_mate():
        mate = score.mate()
        
        if mate is not None:
            if mate > 0:
                print(f"\n♔ BLANCAS ganan en {mate} movimientos (mate)")
            else:
                print(f"\n♚ NEGRAS ganan en {abs(mate)} movimientos (mate)")
    
    # 🟢 CASO NORMAL
    else:
        cp = score.score()
        
        if cp is not None:
            valor = cp / 100
            
            if valor > 1:
                print(f"\n🟢 Blancas ganando claramente (+{valor:.2f})")
            elif valor > 0.3:
                print(f"\n🟡 Leve ventaja blancas (+{valor:.2f})")
            elif valor < -1:
                print(f"\n🔴 Negras ganando claramente ({valor:.2f})")
            elif valor < -0.3:
                print(f"\n🟡 Leve ventaja negras ({valor:.2f})")
            else:
                print("\n⚪ Posición equilibrada")
        
        else:
            print("\nNo se pudo evaluar la posición")

def hacer_movimiento(movimiento):
    try:
        move = chess.Move.from_uci(movimiento)
        
        if move in board.legal_moves:
            board.push(move)
            print("\nMovimiento realizado:", movimiento)
            return True
        else:
            print("\n Movimiento ilegal")
            return False
            
    except:
        print("\nFormato incorrecto ")
        return False


# =========================
# BUCLE PRINCIPAL
# =========================

while True:
    print("\n=========================")
    print(board)
    
    entrada = input("\nIngresá movimiento (ej: e2e4) o 'salir': ").strip()
    if board.is_stalemate:
     print("empate")
     break

    if entrada == "salir":
        break
    
    
    if len(entrada) >= 2:
        origen = entrada[:2]
        movimientos_legales(origen)
    
    
    if hacer_movimiento(entrada):
        evaluar_posicion()

    if board.is_checkmate():
        print("ayy kakmate")
        break

engine.quit()
print("Programa finalizado.")