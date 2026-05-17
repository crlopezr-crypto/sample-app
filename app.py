import requests
import json
import os

class RestCountriesAPI:
    """Cliente para interactuar con la API de REST Countries"""

    def __init__(self):
        # Lectura de configuración mediante variables de entorno (obligatorio por seguridad)
        self.base_url = os.getenv("BASE_URL", "https://restcountries.com/v3.1")
        self.timeout = int(os.getenv("TIMEOUT", "10"))

    def _get(self, endpoint):
        """Método interno con manejo robusto de ≥4 tipos de errores"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, timeout=self.timeout)

            # Error 404: recurso no encontrado
            if response.status_code == 404:
                print(f"❌ Error 404: No se encontró el recurso solicitado en '{url}'")
                return None

            # Otros errores HTTP (500, 403, etc.)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.ConnectionError:
            # Error de conexión: sin red o servidor caído
            print("❌ Error de Conexión: No se pudo establecer conexión con la API.")
            print("   Verifique su conexión a internet o que BASE_URL sea correcta.")
            return None

        except requests.exceptions.Timeout:
            # Error de timeout: el servidor tardó demasiado
            print(f"❌ Error de Timeout: La solicitud superó los {self.timeout} segundos.")
            print("   Puede aumentar el valor con: export TIMEOUT=20")
            return None

        except requests.exceptions.HTTPError as e:
            # Errores HTTP distintos al 404 (403, 500, etc.)
            print(f"❌ Error HTTP {response.status_code}: {e}")
            return None

        except requests.exceptions.RequestException as e:
            # Cualquier otro error de requests no capturado arriba
            print(f"❌ Error inesperado de red: {e}")
            return None

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            # Error al procesar la respuesta JSON
            print(f"❌ Error al procesar la respuesta de la API: {e}")
            return None

    # ── Métodos de consulta ──────────────────────────────────────────────────

    def get_country_by_name(self, name):
        """Busca un país por nombre"""
        return self._get(f"name/{name}")

    def get_country_by_code(self, code):
        """Busca un país por código ISO (ej: 'cl' para Chile)"""
        return self._get(f"alpha/{code}")

    def get_countries_by_region(self, region):
        """Obtiene países por región (americas, europe, asia, africa, oceania)"""
        return self._get(f"region/{region}")

    def get_countries_by_language(self, language):
        """Obtiene países por idioma (ej: 'spanish', 'english')"""
        return self._get(f"lang/{language}")

    def get_countries_by_currency(self, currency):
        """Obtiene países por moneda (ej: 'clp', 'usd', 'eur')"""
        return self._get(f"currency/{currency}")

    # ── Presentación de datos ────────────────────────────────────────────────

    def print_country_info(self, country_data):
        """Imprime información formateada de un país (procesa ≥3 campos)"""
        if not country_data:
            print("No hay datos para mostrar")
            return

        # Si es una lista, toma el primer elemento
        if isinstance(country_data, list):
            country_data = country_data[0]

        print("\n" + "=" * 50)

        # Campo 1: Nombre común y oficial
        name = country_data.get("name", {})
        print(f"País:           {name.get('common', 'N/A')}")
        print(f"Nombre oficial: {name.get('official', 'N/A')}")

        # Campo 2: Capital
        print(f"Capital:        {', '.join(country_data.get('capital', ['N/A']))}")

        # Campo 3: Región y subregión
        print(f"Región:         {country_data.get('region', 'N/A')}")
        print(f"Subregión:      {country_data.get('subregion', 'N/A')}")

        # Campo 4: Población
        print(f"Población:      {country_data.get('population', 'N/A'):,}")

        # Campo 5: Área
        print(f"Área:           {country_data.get('area', 'N/A'):,} km²")

        # Campo 6: Idiomas
        languages = country_data.get("languages", {})
        if languages:
            print(f"Idiomas:        {', '.join(languages.values())}")

        # Campo 7: Monedas
        currencies = country_data.get("currencies", {})
        if currencies:
            currency_names = [
                f"{v.get('name', 'N/A')} ({v.get('symbol', '')})"
                for v in currencies.values()
            ]
            print(f"Monedas:        {', '.join(currency_names)}")

        # Campo 8: Bandera y código ISO
        print(f"Bandera:        {country_data.get('flag', 'N/A')}")
        print(f"Código ISO:     {country_data.get('cca2', 'N/A')}")
        print("=" * 50 + "\n")


# ── Lógica principal ─────────────────────────────────────────────────────────

def main():
    api = RestCountriesAPI()

    auto_mode = os.getenv("AUTO_MODE", "0") == "1"

    print("=" * 50)
    print("  🌍 GeoOps Intelligence — REST Countries API")
    print(f"  Base URL : {api.base_url}")
    print(f"  Timeout  : {api.timeout}s")
    if auto_mode:
        print("  Modo     : Automático (AUTO_MODE=1)")
    print("=" * 50 + "\n")

    if auto_mode:
        consultas = [
            ("nombre",  "Chile"),
            ("codigo",  "cl"),
            ("region",  "americas"),
            ("idioma",  "spanish"),
            ("moneda",  "clp"),
        ]
        for tipo, valor in consultas:
            print(f"\n🔍 Consultando por {tipo}: \'{valor}\'...")
            if tipo == "nombre":
                resultado = api.get_country_by_name(valor)
                api.print_country_info(resultado)
            elif tipo == "codigo":
                resultado = api.get_country_by_code(valor)
                api.print_country_info(resultado)
            elif tipo == "region":
                resultado = api.get_countries_by_region(valor)
                if resultado:
                    print(f"Se encontraron {len(resultado)} países en {valor}:")
                    for c in resultado[:5]:
                        print(f"  - {c.get('name', {}).get('common', 'N/A')}")
            elif tipo == "idioma":
                resultado = api.get_countries_by_language(valor)
                if resultado:
                    print(f"Se encontraron {len(resultado)} países que hablan {valor}:")
                    for c in resultado[:5]:
                        print(f"  - {c.get('name', {}).get('common', 'N/A')}")
            elif tipo == "moneda":
                resultado = api.get_countries_by_currency(valor)
                if resultado:
                    print(f"Países que usan {valor.upper()}:")
                    for c in resultado:
                        print(f"  - {c.get('name', {}).get('common', 'N/A')}")
        print("\n✅ Consulta automática finalizada. ¡GeoOps Intelligence ejecutado correctamente!")
        return

    # ── 1. Buscar por nombre ─────────────────────────────────────────────────
    while True:
        pais = input("Ingrese el nombre del país que desea buscar: ").strip()
        if not pais:
            print("❌ Error: No puede estar vacío.\n")
            continue
        if len(pais) < 3:
            print("❌ Error: Mínimo 3 caracteres.\n")
            continue
        print(f"\n1. Buscando información de '{pais}'...")
        resultado = api.get_country_by_name(pais)
        if resultado is None:
            print(f"❌ No se encontró '{pais}'. Intente nuevamente.\n")
            continue
        api.print_country_info(resultado)
        break

    # ── 2. Buscar por código ─────────────────────────────────────────────────
    while True:
        codigo = input("Ingrese el código ISO del país (ej: 'cl', 'us', 'ar'): ").strip().lower()
        if not codigo:
            print("❌ Error: No puede estar vacío.\n")
            continue
        if not (2 <= len(codigo) <= 3):
            print("❌ Error: Debe tener 2 o 3 caracteres.\n")
            continue
        if not codigo.isalpha():
            print("❌ Error: Solo letras.\n")
            continue
        print(f"\n2. Buscando país por código '{codigo}'...")
        resultado = api.get_country_by_code(codigo)
        if resultado is None:
            print(f"❌ Código '{codigo}' no encontrado. Intente nuevamente.\n")
            continue
        api.print_country_info(resultado)
        break

    # ── 3. Buscar por región ─────────────────────────────────────────────────
    regiones_validas = ["africa", "americas", "asia", "europe", "oceania"]
    while True:
        print(f"\nRegiones disponibles: {', '.join(regiones_validas)}")
        region = input("Ingrese la región: ").strip().lower()
        if not region:
            print("❌ Error: No puede estar vacío.\n")
            continue
        if region not in regiones_validas:
            print(f"❌ Región inválida. Use: {', '.join(regiones_validas)}\n")
            continue
        print(f"\n3. Buscando países en '{region}'...")
        resultado = api.get_countries_by_region(region)
        if resultado is None:
            print("❌ Error al buscar la región. Intente nuevamente.\n")
            continue
        print(f"Se encontraron {len(resultado)} países en {region}:")
        for c in resultado[:5]:
            print(f"  - {c.get('name', {}).get('common', 'N/A')}")
        if len(resultado) > 5:
            print(f"  ... y {len(resultado) - 5} más")
        break

    # ── 4. Buscar por idioma ─────────────────────────────────────────────────
    while True:
        idioma = input("\nIngrese el idioma (ej: 'spanish', 'english', 'french'): ").strip().lower()
        if not idioma:
            print("❌ Error: No puede estar vacío.\n")
            continue
        if len(idioma) < 3 or not idioma.isalpha():
            print("❌ Error: Mínimo 3 letras, sin números ni símbolos.\n")
            continue
        print(f"\n4. Buscando países que hablan '{idioma}'...")
        resultado = api.get_countries_by_language(idioma)
        if resultado is None:
            print(f"❌ Idioma '{idioma}' no encontrado. Intente nuevamente.\n")
            continue
        print(f"Se encontraron {len(resultado)} países:")
        for c in resultado[:10]:
            print(f"  - {c.get('name', {}).get('common', 'N/A')}")
        if len(resultado) > 10:
            print(f"  ... y {len(resultado) - 10} más")
        break

    # ── 5. Buscar por moneda ─────────────────────────────────────────────────
    while True:
        moneda = input("\nIngrese el código de moneda (ej: 'clp', 'usd', 'eur'): ").strip().lower()
        if not moneda:
            print("❌ Error: No puede estar vacío.\n")
            continue
        if len(moneda) != 3 or not moneda.isalpha():
            print("❌ Error: Exactamente 3 letras (ej: 'usd').\n")
            continue
        print(f"\n5. Buscando países que usan '{moneda.upper()}'...")
        resultado = api.get_countries_by_currency(moneda)
        if resultado is None:
            print(f"❌ Moneda '{moneda}' no encontrada. Intente nuevamente.\n")
            continue
        print(f"Países que usan {moneda.upper()}:")
        for c in resultado:
            print(f"  - {c.get('name', {}).get('common', 'N/A')}")
        break

    print("\n✅ Consulta finalizada. ¡Gracias por usar GeoOps Intelligence!")


if __name__ == "__main__":
    main()