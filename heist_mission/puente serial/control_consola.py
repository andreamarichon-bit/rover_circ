# control_consola_base.py
# CORRE EN LA LAPTOP (ESTACIÓN TERRENA)
import socket
import sys
import threading
import time

def escuchar_rover(sock):
    """Función en segundo plano para recibir y mostrar lo que envía el Rover."""
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            # Imprime directo la respuesta (prompt, textos, etc.)
            print(data.decode('utf-8', errors='ignore'), end='', flush=True)
        except Exception:
            break

def iniciar_control_base():
    IP_DESTINO = "127.0.0.1"
    PUERTO = 5007
    
    if len(sys.argv) > 1:
        IP_DESTINO = sys.argv[1]
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("==================================================")
    print("   💻 TERMINAL REMOTA - INTERFAZ DE CONSOLA       ")
    print(f"   Conectado al puente inalámbrico: {IP_DESTINO}:{PUERTO}")
    print("   (Escribe tus comandos de Linux aquí)           ")
    print("==================================================")
    
    # 1. Lanzamos el hilo receptor primero
    hilo_receptor = threading.Thread(target=escuchar_rover, args=(sock,), daemon=True)
    hilo_receptor.start()
    
    # 2. AUTOMÁTICO: Forzar un envío inicial para despertar al Rover y vincular la IP
    # Le mandamos un salto de línea para que el Rover reaccione inmediatamente
    time.sleep(0.2) # Pequeña pausa de estabilidad
    sock.sendto(b"\n", (IP_DESTINO, PUERTO))

    # 3. Bucle de comandos continuo
    while True:
        try:
            comando = input()
            if comando.lower() == "exit": break
            
            # Mandamos lo que teclees con su salto de línea reglamentario
            sock.sendto(f"{comando}\n".encode('utf-8'), (IP_DESTINO, PUERTO))
        except (KeyboardInterrupt, SystemExit):
            break

if __name__ == "__main__":
    iniciar_control_base()