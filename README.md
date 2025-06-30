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


Para la obtencion de datos mediante excel se necesitan los siguientes links de sharepoint y excel

https://smartforcecom.sharepoint.com/:f:/s/TELCEL747/EnXkhJ2w4cZDsGdYIoshXvUBnTOoSocCbFa8KKZ3VWVy9g?e=DYlabh

https://smartforcecom.sharepoint.com/:x:/s/TELCEL747/EZcIDUrkNkpFs4bKHnZ9uAoB1qZtSbHUigp2lBtmGmgUGw?e=ve4OVP

Para el segundo link 

1. Hoja Cifras control columnas K - Y

2. Hoja Datos operativos Columnas C - G

3. Hoja Incidentes Completa

