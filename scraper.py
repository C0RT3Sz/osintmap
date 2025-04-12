import requests
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
