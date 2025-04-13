import requests
import csv
from bs4 import BeautifulSoup


resposta = requests.get("https://google.com")
soup = BeautifulSoup(resposta.text, "html.parser")

links = soup.find_all("a")

links_externos = []
links_internos = []

for link in links:
    href = link.get("href")
    if href and href.startswith("http"):
        links_externos.append(href)
    elif href and href.startswith("/"):
        links_internos.append(href)

print("\nLinks Externos Encontrados:")
for externo in links_externos:
    print(externo)


print("\nLinks Internos Encontrados:")
for interno in links_internos:
    print(interno)

paragrafos = soup.select("p")
print("\nParágrafos Encontrados:")
for p in paragrafos:
    print(p.text.strip())    

titulos =  soup.select("h1")
print("\nTítulos h1 Encontrados:")
for titulo in titulos:
    print(titulo.text.strip())   

with open("links_e_titulos.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)

    escritor_csv.writerow(["URL", "Título", "H1", "H2"])

    print("\nArmazenando dados no arquivo CSV...\n")
    for interno in links_internos:
        url_completa = "https://google.com" + interno
        try:
            resposta_interna = requests.get(url_completa)
            soup_interna = BeautifulSoup(resposta_interna.text, "html.parser")

            titulo = soup_interna.title.string if soup_interna.title else "Sem Titulo"
            h1 = soup_interna.find_all("h1")
            h2 = soup_interna.find_all("h2")

            h1_texto = ", ".join([tag.get_text(strip=True) for tag in h1]) if h1 else "Nenhum H1"
            h2_texto = ", ".JOIN([tag.get_text(strip=True) for tag in h2]) if h2 else "Nenhum H2"

            escritor_csv.writerow([url_completa, titulo, h1_texto, h2_texto])

        except Exception as e:
            print(f"Erro ao acessar {url_completa}: {e}")

    print("\nDados armazenados com sucesso em 'links_e_titlutos.csv'.")