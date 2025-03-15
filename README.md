# FootballTeamsStats
TeamsPlayersStats (BETA) es un script en Python que recopila información sobre jugadores de fútbol de distintos equipos usando Transfermarkt y FIFA Ratings. Actualmente, esta versión está en desarrollo y puede presentar algunas limitaciones o errores.

📌 Requisitos
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes librerías:
pip install requests beautifulsoup4 pandas openpyxl


🚀 Uso
Ejecuta el script en la terminal:
python scraper_transfermarkt.py

Cuando se te solicite, ingresa el nombre del equipo (Ejemplo: FC Brentford).

🔧 Notas
Si no se encuentra información en FIFA Ratings, los datos se mostrarán como "N/A".
Los nombres de los jugadores se formatean para coincidir con la URL de FIFA Ratings (ej. "Christian Nørgaard" → "christian-norgaard").
Si hay algún error al extraer datos de Transfermarkt, el script mostrará una advertencia en la consola.

📜 Licencia
Este proyecto es de código abierto y puede ser modificado libremente.

