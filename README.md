# Backend Cotizador
Es una app de Python que usa el framework Flask para servir solicitudes y las bibliotecas de Pandas y Pandas Natural Language Querying
para traducir preguntas en lenguaje natural a SQL, consultar un DataFrame con dicho query y luego generar una respuesta estructurada.

Pandas NQL soporta nativamente OpenAI, pero se incluyen en la carpeta new_nql los archivos necesarios para implementar soporte de AWS Bedrock.

## Instalación

1. Clonar el repositorio
2. Crear ambiente virtual
   ```bash
   python -m venv .venv
   ```
4. Instalar requerimientos
   ```bash
   pip install -r requirements.txt
   ```
5. Copiar archivos a la biblioteca
   ```bash
   cp new_nql/ .venv/lib/python/site-packages/pandas_nql/
   ```

Los Prompts sew pueden encontrar en el archivo de bedrock_sql_generator.
