import requests
import csv
import re
import time
from bs4 import BeautifulSoup

URL_BASE = "http://testphp.vulnweb.com/"

# Requisição e Parsing da Página
resposta = requests.get(URL_BASE)
soup = BeautifulSoup(resposta.text, "html.parser")

# Coleta de Links
links = soup.find_all("a")
links_externos = [link.get("href") for link in links if link.get("href", "").startswith("http")]
links_internos = [link.get("href") for link in links if link.get("href", "").startswith("/")]

# Exibição de Links
print("\nLinks Externos Encontrados:")
for externo in links_externos:
    print(externo)

print("\nLinks Internos Encontrados:")
for interno in links_internos:
    print(interno)

# Coleta de Parágrafos
print("\nParágrafos Encontrados:")
for p in soup.select("p"):
    print(p.text.strip())

# Coleta de Títulos H1
print("\nTítulos h1 Encontrados:")
for titulo in soup.select("h1"):
    print(titulo.text.strip())

# Armazenamento de Dados no CSV
with open("links_e_titulos.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerow(["URL", "Título", "H1", "H2"])

    print("\nArmazenando dados no arquivo CSV...\n")
    for interno in links_internos:
        url_completa = URL_BASE + interno.lstrip("/")
        try:
            resposta_interna = requests.get(url_completa)
            soup_interna = BeautifulSoup(resposta_interna.text, "html.parser")

            titulo = soup_interna.title.string if soup_interna.title else "Sem Título"
            h1_tags = soup_interna.find_all("h1")
            h2_tags = soup_interna.find_all("h2")

            h1_texto = ", ".join(tag.get_text(strip=True) for tag in h1_tags) or "Nenhum H1"
            h2_texto = ", ".join(tag.get_text(strip=True) for tag in h2_tags) or "Nenhum H2"

            escritor_csv.writerow([url_completa, titulo, h1_texto, h2_texto])
        except Exception as e:
            print(f"Erro ao acessar {url_completa}: {e}")

    print("\nDados armazenados com sucesso em 'links_e_titulos.csv'.")

# Análise de Tecnologias da Página Principal
print("\nAnalisando tecnologias da página principal...\n")
cabecalhos = resposta.headers

print("Cabeçalhos HTTP encontrados:")
for chave, valor in cabecalhos.items():
    print(f"{chave}: {valor}")

tecnologias_detectadas = []

if "X-Powered-By" in cabecalhos:
    tecnologias_detectadas.append(cabecalhos["X-Powered-By"])
if "Server" in cabecalhos:
    tecnologias_detectadas.append(cabecalhos["Server"])

html = resposta.text.lower()
if "wp-content" in html:
    tecnologias_detectadas.append("WordPress")
if "bootstrap" in html:
    tecnologias_detectadas.append("Bootstrap")
if "jquery" in html:
    tecnologias_detectadas.append("jQuery")

if tecnologias_detectadas:
    print("\nTecnologias possivelmente utilizadas:")
    for tech in tecnologias_detectadas:
        print(tech)
else:
    print("\nNenhuma tecnologia detectada.")

# Busca de E-mails na Página Principal
print("\nProcurando por e-mails na página...\n")
padrao_email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
emails_principais = re.findall(padrao_email, html)

if emails_principais:
    print("E-mails encontrados:")
    for email in set(emails_principais):
        print(email)
else:
    print("Nenhum e-mail encontrado.")

# Coleta de Meta Tags
print("\nColetando meta tags da página...\n")
meta_tags = soup.find_all("meta")

for tag in meta_tags:
    if tag.get("name") in ["description", "keywords", "author"]:
        print(f"{tag.get('name').capitalize()}: {tag.get('content')}")

# Exploração de Páginas Internas
print("\nExplorando páginas internas e coletando títulos...\n")
headers = {"User-Agent": "Mozilla/5.0"}

for link in links_internos:
    try:
        url = URL_BASE + link.lstrip("/")
        resposta_pagina = requests.get(url, headers=headers, timeout=5)
        soup_pagina = BeautifulSoup(resposta_pagina.text, "html.parser")
        titulo = soup_pagina.title.string.strip() if soup_pagina.title else "Sem título"
        print(f"{link} → {titulo}")
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao acessar {link}: {e}")

# Busca de E-mails nas Páginas Internas
print("\nBuscando e-mails nas páginas internas...\n")
emails_encontrados = set()

for link in links_internos:
    try:
        url = URL_BASE + link.lstrip("/")
        resposta_email = requests.get(url, headers=headers, timeout=5)
        html_email = resposta_email.text
        encontrados = re.findall(padrao_email, html_email)

        for email in encontrados:
            emails_encontrados.add(email)
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao acessar {link}: {e}")

if emails_encontrados:
    print("\nE-mails encontrados:")
    for email in emails_encontrados:
        print(email)
else:
    print("\nNenhum e-mail encontrado nas páginas.")
