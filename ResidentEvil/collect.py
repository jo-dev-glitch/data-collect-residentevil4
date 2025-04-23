import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from tqdm import tqdm
import time

URL_PRINCIPAL = 'https://www.residentevildatabase.com/personagens/'
DB_PATH = r"C:\dataengineer\web-scrapping\residentevil.db"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'accept': 'text/html',
}

# === 1. Coleta os links dos personagens ===
def extrair_links_personagens(url_principal):
    response = requests.get(url_principal, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar página principal. Status: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    links_personagens = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        nome = a.text.strip()
        if (
            "residentevildatabase.com" in href
            and nome
            and "/personagens/" not in href
            and not nome.lower().startswith(("notícias", "arquivo", "horror database", "crossovers", "[arquivo]", "resident evil database"))
        ):
            links_personagens.append({"nome": nome, "url": href})

    return list({link["url"]: link for link in links_personagens}.values())

# === 2. Extrai dados individuais ===
def extrair_dados_personagem(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[ERRO] Falha ao acessar {url} (status {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        texto = soup.get_text(separator="\n")

        dados = {
            "nome": soup.find("h1").text.strip() if soup.find("h1") else "N/A",
            "url": url,
            "ano_nascimento": "N/A",
            "tipo_sanguineo": "N/A",
            "altura": "N/A",
            "peso": "N/A",
            "aparicoes": []
        }

        linhas = texto.split("\n")
        for i, linha in enumerate(linhas):
            if "ano de nascimento" in linha.lower():
                dados["ano_nascimento"] = linha.split(":")[-1].strip()
            elif "tipo sanguíneo" in linha.lower():
                dados["tipo_sanguineo"] = linha.split(":")[-1].strip()
            elif "altura" in linha.lower():
                dados["altura"] = linha.split(":")[-1].strip()
            elif "peso" in linha.lower():
                dados["peso"] = linha.split(":")[-1].strip()

        # Aparições (busca <h4>Aparições</h4> e lista seguinte)
        aparicoes = []
        header = soup.find("h4", string=lambda x: x and "aparições" in x.lower())
        if header:
            ul = header.find_next_sibling("ul")
            if ul:
                for li in ul.find_all("li"):
                    aparicoes.append(li.get_text(strip=True))
        dados["aparicoes"] = aparicoes

        return dados

    except Exception as e:
        print(f"[EXCEPTION] Erro ao processar {url}: {e}")
        return None

# === 3. Coleta completa com progresso ===
print("[INFO] Coletando links de personagens...")
links = extrair_links_personagens(URL_PRINCIPAL)

dados_personagens = []
dados_aparicoes = []

for personagem in tqdm(links, desc="Coletando dados"):
    resultado = extrair_dados_personagem(personagem["url"])
    if resultado:
        dados_personagens.append({
            "nome": resultado["nome"],
            "url": resultado["url"],
            "ano_nascimento": resultado["ano_nascimento"],
            "tipo_sanguineo": resultado["tipo_sanguineo"],
            "altura": resultado["altura"],
            "peso": resultado["peso"]
        })
        for jogo in resultado["aparicoes"]:
            dados_aparicoes.append({
                "personagem": resultado["nome"],
                "aparicao": jogo
            })
    time.sleep(1)

# === 4. DataFrames e persistência ===
df_personagens = pd.DataFrame(dados_personagens)
df_aparicoes = pd.DataFrame(dados_aparicoes)

print("\n[INFO] Primeiros personagens:")
print(df_personagens.head())
print("\n[INFO] Primeiras aparições:")
print(df_aparicoes.head())

# === 5. Salvar no banco SQLite ===
try:
    conn = sqlite3.connect(DB_PATH, timeout=30)
    df_personagens.to_sql("personagens", conn, if_exists="replace", index=False)
    df_aparicoes.to_sql("aparicoes", conn, if_exists="replace", index=False)
    print(f"[SUCESSO] Dados salvos no banco: {DB_PATH}")
except Exception as e:
    print(f"[ERRO] Falha ao salvar no banco: {e}")
finally:
    if conn:
        conn.close()
