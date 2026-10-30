import httpx
from core.parser import TenderParser
from pipeline.cleaner import DataCleaner
from services.notifier import TelegramNotifier
from config import Config

def run_pipeline():
    # Endpoint global de productos garantizado (15 registros)
    target_url = "https://dummyjson.com/products?limit=15"
    
    print(f"[1/4] Consultando origen de datos: {target_url}")
    extracted_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        with httpx.Client(timeout=10.0, follow_redirects=True, headers=headers) as client:
            response = client.get(target_url)
            response.raise_for_status()
            raw_data = response.json()
            
            # Formateo directo de datos extraídos
            for item in raw_data.get("products", []):
                brand_name = item.get("brand") or "Proveedor Industrial"
                extracted_data.append({
                    "titulo": item.get("title", "Sin Título"),
                    "dependencia": f"Marca: {brand_name}",
                    "monto": f"${item.get('price', 0):,.2f} USD",
                    "estado": "Disponible" if item.get("stock", 0) > 0 else "Agotado"
                })
            print(f"[+] Datos remotos obtenidos exitosamente: {len(extracted_data)} registros.")
    except Exception as e:
        print(f"[!] Alerta de red ({e}). Activando fallback de respaldo local...")
        extracted_data = TenderParser.get_fallback_data()
        print(f"[+] Registros cargados desde el módulo de respaldo: {len(extracted_data)}")

    # 2. Limpieza y guardado
    print("[2/4] Ejecutando pipeline de limpieza y estructuración...")
    df = DataCleaner.process_and_save(extracted_data, output_filename="licitaciones_extraidas.csv")

    # 3. Notificación
    print("[3/4] Verificando canal de alertas...")
    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        notifier = TelegramNotifier(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
        msg = f"🔔 *Pipeline Actualizado*\nSe procesaron {len(df)} registros."
        notifier.send_alert(msg)
    else:
        print("[!] Notificación omitida: Credenciales no detectadas en .env")

if __name__ == "__main__":
    run_pipeline()