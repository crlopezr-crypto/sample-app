import requests
import json

class RestCountriesAPI:
    """Cliente para interactuar con la API de REST Countries"""
    
    def __init__(self):
        self.base_url = "https://restcountries.com/v3.1"
    
    def get_all_countries(self):
        """Obtiene todos los países"""
        try:
            response = requests.get(f"{self.base_url}/all")
            response.raise_for_status()  # Identificador de errores
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener países: {e}")
            return None
    
    def get_country_by_name(self, name):
        """Busca un país por nombre"""
        try:
            response = requests.get(f"{self.base_url}/name/{name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar '{name}': {e}")
            return None
    
    def get_country_by_code(self, code):
        """Busca un país por código (ej: 'cl' para Chile)"""
        try:
            response = requests.get(f"{self.base_url}/alpha/{code}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar código '{code}': {e}")
            return None
    
    def get_countries_by_region(self, region):
        """Obtiene países por región (ej: 'americas', 'europe', 'asia', 'africa', 'oceania')"""
        try:
            response = requests.get(f"{self.base_url}/region/{region}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar región '{region}': {e}")
            return None
    
    def get_countries_by_language(self, language):
        """Obtiene países por idioma (ej: 'spanish', 'english')"""
        try:
            response = requests.get(f"{self.base_url}/lang/{language}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar idioma '{language}': {e}")
            return None
    
    def get_countries_by_currency(self, currency):
        """Obtiene países por moneda (ej: 'clp', 'usd', 'eur')"""
        try:
            response = requests.get(f"{self.base_url}/currency/{currency}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar moneda '{currency}': {e}")
            return None
    
    def print_country_info(self, country_data):
        """Imprime información formateada de un país"""
        if not country_data:
            print("No hay datos para mostrar")
            return
        
        # Si es una lista, toma el primer elemento
        if isinstance(country_data, list):
            country_data = country_data[0]
        
        print("\n" + "="*50)
        print(f"País: {country_data.get('name', {}).get('common', 'N/A')}")
        print(f"Nombre oficial: {country_data.get('name', {}).get('official', 'N/A')}")
        print(f"Capital: {', '.join(country_data.get('capital', ['N/A']))}")
        print(f"Región: {country_data.get('region', 'N/A')}")
        print(f"Subregión: {country_data.get('subregion', 'N/A')}")
        print(f"Población: {country_data.get('population', 'N/A'):,}")
        print(f"Área: {country_data.get('area', 'N/A'):,} km²")
        
        # Idiomas
        languages = country_data.get('languages', {})
        if languages:
            print(f"Idiomas: {', '.join(languages.values())}")
        
        # Monedas
        currencies = country_data.get('currencies', {})
        if currencies:
            currency_names = [f"{curr.get('name')} ({curr.get('symbol', '')})" 
                            for curr in currencies.values()]
            print(f"Monedas: {', '.join(currency_names)}")
        
        # Bandera
        print(f"Bandera: {country_data.get('flag', 'N/A')}")
        print(f"Código: {country_data.get('cca2', 'N/A')}")
        print("="*50 + "\n")


def main():
    """Ejemplos de uso de la API"""
    api = RestCountriesAPI()
    
    print("🌍 EJEMPLOS DE USO - REST COUNTRIES API\n")
    
    # Ejemplo 1: Buscar país por nombre con validación
    while True:
        pais = input("Ingrese el nombre del país que desea buscar: ").strip()
        
        if not pais:
            print("❌ Error: No puede estar vacío. Intente nuevamente.\n")
            continue
        
        if len(pais) < 3:
            print("❌ Error: El nombre debe tener al menos 3 caracteres.\n")
            continue
        
        print(f"\n1. Buscando información de {pais}...")
        resultado = api.get_country_by_name(pais)
        
        if resultado is None:
            print(f"❌ No se encontró el país '{pais}'. Intente nuevamente.\n")
            continue
        
        api.print_country_info(resultado)
        break
    
    # Ejemplo 2: Buscar por código con validación
    while True:
        codigo_pais = input("Ingrese el código del país que desea buscar (ej: 'us', 'cl', 'ar'): ").strip().lower()
        
        if not codigo_pais:
            print("❌ Error: No puede estar vacío. Intente nuevamente.\n")
            continue
        
        if len(codigo_pais) < 2 or len(codigo_pais) > 3:
            print("❌ Error: El código debe tener 2 o 3 caracteres (ej: 'cl', 'usa').\n")
            continue
        
        if not codigo_pais.isalpha():
            print("❌ Error: El código solo debe contener letras.\n")
            continue
        
        print(f"\n2. Buscando país por código '{codigo_pais}'...")
        codigo = api.get_country_by_code(codigo_pais)
        
        if codigo is None:
            print(f"❌ No se encontró el código '{codigo_pais}'. Intente nuevamente.\n")
            continue
        
        api.print_country_info(codigo)
        break
    
    # Ejemplo 3: Países por región con validación
    regiones_validas = ['africa', 'americas', 'asia', 'europe', 'oceania']
    
    while True:
        print("\nRegiones disponibles: africa, americas, asia, europe, oceania")
        pais_region = input("Ingrese la región que desea buscar: ").strip().lower()
        
        if not pais_region:
            print("❌ Error: No puede estar vacío. Intente nuevamente.\n")
            continue
        
        if pais_region not in regiones_validas:
            print(f"❌ Error: '{pais_region}' no es una región válida.")
            print(f"Regiones válidas: {', '.join(regiones_validas)}\n")
            continue
        
        print(f"\n3. Buscando países en {pais_region}...")
        region = api.get_countries_by_region(pais_region)
        
        if region is None:
            print(f"❌ Error al buscar la región. Intente nuevamente.\n")
            continue
        
        if region:
            print(f"Se encontraron {len(region)} países en {pais_region}:")
            for country in region[:5]:
                print(f"  - {country.get('name', {}).get('common', 'N/A')}")
            if len(region) > 5:
                print(f"  ... y {len(region) - 5} más\n")
        break
    
    # Ejemplo 4: Países por idioma con validación
    while True:
        lenguaje = input("\nIngrese el idioma que desea buscar (ej: 'spanish', 'english', 'french'): ").strip().lower()
        
        if not lenguaje:
            print("❌ Error: No puede estar vacío. Intente nuevamente.\n")
            continue
        
        if len(lenguaje) < 3:
            print("❌ Error: El idioma debe tener al menos 3 caracteres.\n")
            continue
        
        if not lenguaje.isalpha():
            print("❌ Error: El idioma solo debe contener letras.\n")
            continue
        
        print(f"\n4. Buscando países que hablan {lenguaje}...")
        paises = api.get_countries_by_language(lenguaje)
        
        if paises is None:
            print(f"❌ No se encontró el idioma '{lenguaje}'. Intente nuevamente.\n")
            continue
        
        if paises:
            print(f"Se encontraron {len(paises)} países:")
            for country in paises[:10]:
                print(f"  - {country.get('name', {}).get('common', 'N/A')}")
            if len(paises) > 10:
                print(f"  ... y {len(paises) - 10} más\n")
        break
    
    # Ejemplo 5: Países por moneda con validación
    while True:
        pais_segun_moneda = input("\nIngrese la moneda que desea buscar (ej: 'clp', 'usd', 'eur'): ").strip().lower()
        
        if not pais_segun_moneda:
            print("❌ Error: No puede estar vacío. Intente nuevamente.\n")
            continue
        
        if len(pais_segun_moneda) != 3:
            print("❌ Error: El código de moneda debe tener exactamente 3 caracteres (ej: 'usd', 'clp').\n")
            continue
        
        if not pais_segun_moneda.isalpha():
            print("❌ Error: El código de moneda solo debe contener letras.\n")
            continue
        
        print(f"\n5. Buscando países que usan {pais_segun_moneda.upper()}...")
        currency = api.get_countries_by_currency(pais_segun_moneda)
        
        if currency is None:
            print(f"❌ No se encontró la moneda '{pais_segun_moneda}'. Intente nuevamente.\n")
            continue
        
        if currency:
            print(f"Países que usan {pais_segun_moneda.upper()}:")
            for country in currency:
                print(f"  - {country.get('name', {}).get('common', 'N/A')}")
        break
    
    print("\n✅ Consulta finalizada. ¡Gracias por usar REST Countries API!")


if __name__ == "__main__":
    main()