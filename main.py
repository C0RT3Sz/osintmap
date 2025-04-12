import requests

resposta = requests.get("https://google.com")

print("Requisição Funcionando", resposta.status_code)
