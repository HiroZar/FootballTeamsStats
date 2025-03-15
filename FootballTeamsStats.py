import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import pandas as pd

def get_team_id(team_name):
    search_url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={team_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    team_links = soup.select("a[href*='/startseite/verein/']")
    teams = []

    for team_link in team_links:
        team_url = team_link["href"]
        team_name_found = team_link["title"].strip()
        team_id = team_url.split("/")[-1]

        teams.append((team_name_found, team_id))

    if not teams:
        print(f"No se encontraron equipos con el nombre de '{team_name}'.")
        return None

    print("\n Lista de equipos encontrados:")
    for idx, (name, _) in enumerate(teams, start=1):
        print(f"{idx}. {name}")

    while True:
        try:
            choice = int(input("\nIngrese el número del equipo deseado (1, 2, 3...): "))
            if 1 <= choice <= len(teams):
                return teams[choice - 1][1]
            else:
                print("Número fuera de lista")
        except ValueError:
            print("Debe ingresar un número")

def get_players(team_name):
    """Obtiene la lista de jugadores del equipo"""
    team_id = get_team_id(team_name)
    if not team_id:
        return
    
    url = f"https://www.transfermarkt.com/fc-brentford/startseite/verein/{team_id}"
    print(url)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table.items tbody tr")
    
    players_data = []

    for row in rows:
        try:
            number = row.select_one("div.rn_nummer").text.strip() if row.select_one("div.rn_nummer") else "N/A"
            name = row.select_one("td.hauptlink a").text.strip() if row.select_one("td.hauptlink a") else "N/A"
            position = row.select_one("td.posrela table tr:nth-of-type(2) td").text.strip() if row.select_one("td.posrela table tr:nth-of-type(2) td") else "N/A"
            dob_column = row.select_one("td.zentriert:nth-of-type(3)").text.strip() if row.select_one("td.zentriert:nth-of-type(3)") else "N/A"
            nationality = row.select_one("td.zentriert img.flaggenrahmen")["title"] if row.select_one("td.zentriert img.flaggenrahmen") else None
        
            if nationality:
              height, weight, best_foot, rating = get_fifa_data(name)
              players_data.append((number, name, position, dob_column, nationality, height, weight, best_foot, rating))

        except Exception as e:
            print(f"⚠️ Error al procesar un jugador: {e}")
    save_to_excel(players_data, team_name)

def save_to_excel(players_data, team_name):
    df = pd.DataFrame(players_data, columns=["Número", "Nombre", "Posición", "Fecha Nac.", "Nacionalidad", "Altura (cm)", "Peso (kg)", "Pie Hábil", "Valoración FIFA"])
    file_name = f"{team_name}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Archivo '{file_name}' creado exitosamente.")


def format_name_for_fifa(name):
    replacements = {
        'ø': 'o', 'æ': 'ae', 'å': 'a', 'ü': 'u', 'ö': 'o', 'é': 'e', 'ñ': 'n', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ç': 'c', 'ğ': 'g', 'ş': 's', 'đ': 'd', 'ß': 'ss'
    }
    name = name.lower()
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = name.replace(' ', '-')
    return name


def get_fifa_data(player_name):
    formatted_name = format_name_for_fifa(player_name)
    url = f"https://www.fifaratings.com/{formatted_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "N/A", "N/A", "N/A", "N/A"

    soup = BeautifulSoup(response.text, "html.parser")

    height_weight_text = soup.select_one("p.mb-0:contains('Height')")
    if height_weight_text:
        height_weight = height_weight_text.text
        height_match = re.search(r'(\d+)cm', height_weight)
        weight_match = re.search(r'(\d+)kg', height_weight)
        height = height_match.group(1) if height_match else "N/A"
        weight = weight_match.group(1) if weight_match else "N/A"
    else:
        height, weight = "N/A", "N/A"
    p_tags = soup.find_all("p", class_="mb-0")
    best_foot = "N/A"

    for tag in p_tags:
      if "Best Foot:" in tag.text:
          best_foot = tag.text.split(': ')[1]
    rating_tag = soup.select_one(".attribute-box-player")
    rating = rating_tag.text.strip() if rating_tag else "N/A"
    return height, weight, best_foot, rating

team_name = input("Ingrese el nombre del equipo: ")
get_players(team_name)
