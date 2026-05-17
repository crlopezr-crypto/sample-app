# 🌍 GeoOps Intelligence — REST Countries API Client

> Consulta centralizada de información geográfica, operativa y monetaria de países para profesionales de TI y operaciones internacionales.

---

## A. Contexto y Narrativa

### Stakeholder

**Analista de Operaciones TI / Coordinador de Infraestructura Internacional**

Un profesional que gestiona contratos, despliegues de infraestructura o relaciones con proveedores distribuidos en múltiples países. Trabaja con equipos de soporte multinacionales, administra nodos de red en distintas regiones y necesita contextualizar rápidamente información geopolítica y operativa de un país determinado.

### Propuesta de Valor

**Problema:** Un analista de TI que opera con infraestructura distribuida globalmente pierde tiempo navegando entre múltiples fuentes (Wikipedia, XE.com, Google Maps, sitios gubernamentales) para obtener datos básicos de un país antes de tomar decisiones operativas: coordinar con un proveedor en Asia, verificar la moneda local antes de procesar una factura internacional, o determinar el idioma oficial para escalar un ticket de soporte.

**Solución:** GeoOps Intelligence centraliza en una sola consulta toda la información crítica de un país: capital, región geográfica, subregión, población, idiomas oficiales, monedas vigentes y código ISO. El analista puede buscar por nombre, código de país, región, idioma o moneda, eliminando la fragmentación de fuentes y reduciendo el tiempo de consulta de minutos a segundos.

**Ejemplo de uso real:**
> *"Necesito escalar un incidente a nuestro proveedor en Malasia. En lugar de buscar en tres sitios distintos, ejecuto una consulta por nombre y obtengo de inmediato: capital Kuala Lumpur, idioma Malayo, moneda Ringgit (MYR), región Asia — todo lo que necesito para preparar la comunicación."*

---

## B. Documentación del Repositorio

### Requisitos del Sistema

- Python 3.8 o superior
- Docker (para ejecución en contenedor)
- Acceso a internet (la aplicación consume la API pública [REST Countries v3.1](https://restcountries.com))

### Variables de Entorno

La aplicación no requiere autenticación, ya que REST Countries es una API pública y gratuita. Sin embargo, se exponen las siguientes variables de entorno opcionales para configuración:

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `BASE_URL` | URL base de la API de REST Countries | `https://restcountries.com/v3.1` |
| `TIMEOUT` | Tiempo máximo de espera por respuesta (segundos) | `10` |
| `AUTO_MODE` | Modo de ejecución: `1` = automático, `0` = interactivo | `0` |

### Estructura del Proyecto

```
sample-app/
│
├── app.py              # Script principal que consulta la API
├── build.sh            # Script de automatización (genera Dockerfile, build y run)
├── requirements.txt    # Dependencias Python
├── .gitignore          # Archivos excluidos del repositorio
├── README.md           # Este archivo
└── evidencias/
    ├── docker/
    │   ├── output.txt        # docker ps -a + logs con datos reales de la API
    │   └── screenshot.png    # Captura de la salida en consola
    └── jenkins/
        ├── stage_view.png
        ├── console_output_build.png
        ├── credentials.png
        └── pipeline_script.txt
```

### Dependencias Python

Archivo `requirements.txt`:

```
requests==2.31.0
```

### Instrucciones de Ejecución con Docker

#### 1. Ejecución automática mediante build.sh (recomendada)

```bash
bash build.sh
```

El script genera el Dockerfile, construye la imagen y ejecuta el contenedor automáticamente.

#### 2. Ejecución manual paso a paso

```bash
docker build -t geoops-intelligence .
docker run -it --name samplerunning geoops-intelligence
```

#### 3. Ejecución directa sin Docker

```bash
pip install -r requirements.txt
python app.py
```

---

### Variable AUTO_MODE

#### ¿Por qué existe AUTO_MODE?

La aplicación fue diseñada originalmente con entradas interactivas (`input()`) para uso en terminal por parte del analista. Sin embargo, en un entorno CI/CD como Jenkins, no existe un usuario interactuando en tiempo real — Jenkins ejecuta los procesos en background sin terminal asignada (sin TTY).

Cuando Python intenta ejecutar `input()` sin una terminal disponible, lanza un `EOFError` y el contenedor termina con código de salida 1 (error), lo que haría fallar el pipeline.

`AUTO_MODE=1` resuelve esto de forma limpia: la aplicación detecta mediante `os.getenv()` si está corriendo en un entorno automatizado y, en ese caso, ejecuta un conjunto de consultas predefinidas directamente contra la API sin esperar input del usuario. El contenedor termina con código de salida 0 (éxito).

Esta es una práctica estándar en desarrollo profesional: separar el comportamiento interactivo del automatizado mediante variables de entorno, manteniendo el mismo código base para ambos entornos.

| Valor | Comportamiento |
|---|---|
| `AUTO_MODE=0` (default) | Modo interactivo — solicita inputs al usuario |
| `AUTO_MODE=1` | Modo automático — ejecuta consultas predefinidas y termina |

En entorno local:

```bash
# Windows PowerShell
$env:AUTO_MODE = "1"
python app.py

# Linux/Mac
export AUTO_MODE=1
python app.py
