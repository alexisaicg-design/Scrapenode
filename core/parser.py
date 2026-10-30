from typing import List, Dict, Any

class TenderParser:
    @staticmethod
    def parse_json_api(json_data: Dict[str, Any]) -> List[Dict[str, str]]:
        if not json_data:
            return []

        # Soporte para API de datos.gob.mx
        if "results" in json_data:
            items = []
            for record in json_data.get("results", []):
                title = record.get("title", "Sin Título")
                buyer = record.get("buyer", {}).get("name", "Dependencia Desconocida")
                status = record.get("status", "N/A")
                amount = record.get("value", {}).get("amount", "N/A")
                currency = record.get("value", {}).get("currency", "MXN")

                items.append({
                    "titulo": title,
                    "dependencia": buyer,
                    "monto": f"{amount} {currency}" if amount != "N/A" else "Por Definir",
                    "estado": status
                })
            return items

        # Soporte para API de MercadoLibre (Monitoreo de Precios B2B)
        elif "results" in json_data and len(json_data["results"]) > 0 and "price" in json_data["results"][0]:
            items = []
            for record in json_data.get("results", []):
                items.append({
                    "titulo": record.get("title", "Sin Título"),
                    "dependencia": "MercadoLibre B2B",
                    "monto": f"${record.get('price', 0):,.2f} MXN",
                    "estado": "Disponible" if record.get("available_quantity", 0) > 0 else "Agotado"
                })
            return items

        return []

    @staticmethod
    def get_fallback_data() -> List[Dict[str, str]]:
        """Datos de respaldo en caso de que las APIs externas expiren por timeout."""
        return [
            {"titulo": "Adquisición de Laptops y Equipo de Cómputo", "dependencia": "SEDECO Michoacán", "monto": "$450,000.00 MXN", "estado": "Abierta"},
            {"titulo": "Mantenimiento Preventivo de Planta Eléctrica", "dependencia": "IMSS Michoacán", "monto": "$180,000.00 MXN", "estado": "En Evaluación"},
            {"titulo": "Suministro de Material Eléctrico e Hidráulico", "dependencia": "Ayuntamiento de Morelia", "monto": "$320,000.00 MXN", "estado": "Abierta"},
            {"titulo": "Servicio de Limpieza y Sanitización Industrial", "dependencia": "Secretaría de Salud", "monto": "$600,000.00 MXN", "estado": "Adjudicada"},
            {"titulo": "Servicios de Consultoría e Infraestructura Cloud", "dependencia": "Gobierno del Estado", "monto": "$850,000.00 MXN", "estado": "Abierta"}
        ]