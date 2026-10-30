from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_pipeline
import datetime

scheduler = BlockingScheduler()

# Programa la ejecución automática del pipeline cada 60 minutos
@scheduler.scheduled_job('interval', minutes=60)
def timed_job():
    print(f"[{datetime.datetime.now()}] Ejecutando actualización automática del pipeline...")
    run_pipeline()

if __name__ == "__main__":
    print("[+] Servidor de tareas programadas iniciado. Ejecutando pipeline cada 60 minutos...")
    # Ejecución inicial al arrancar
    run_pipeline()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("[-] Servidor de tareas detenido.")