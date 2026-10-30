import pandas as pd
from typing import List, Dict

class DataCleaner:
    @staticmethod
    def process_and_save(data: List[Dict[str, str]], output_filename: str = "output_data.csv") -> pd.DataFrame:
        if not data:
            print("[-] No hay datos para procesar.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        # Limpieza básica de espacios en blanco sobrantes
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        # Exportación a CSV
        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"[+] Datos procesados y guardados exitosamente en '{output_filename}' ({len(df)} registros).")
        return df
        from bs4 import BeautifulSoup
from typing import List, Dict

class TenderParser:
    @staticmethod
    def parse_html(html_content: str) -> List[Dict[str, str]]:
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        items = []
        
        # Selección de filas o tarjetas de licitaciones (Estructura Genérica Adaptable)
        rows = soup.find_all("tr", class_="tender-row") or soup.find_all("div", class_="quote")

        for row in rows:
            # Extracción de campos clave
            title_node = row.find("span", class_="text") or row.find("a", class_="tender-title")
            entity_node = row.find("small", class_="author") or row.find("td", class_="entity")

            if title_node:
                items.append({
                    "titulo": title_node.get_text(strip=True),
                    "dependencia": entity_node.get_text(strip=True) if entity_node else "N/A",
                    "estado": "Abierta"
                })

        return items
        import pandas as pd
from typing import List, Dict

class DataCleaner:
    @staticmethod
    def process_and_save(data: List[Dict[str, str]], output_filename: str = "output_data.csv") -> pd.DataFrame:
        if not data:
            print("[-] No hay datos para procesar.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"[+] Datos procesados y guardados exitosamente en '{output_filename}' ({len(df)} registros).")
        return df
        