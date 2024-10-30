from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

# URLs dos três arquivos JSON
json_urls = [
    'https://www.dropbox.com/scl/fi/qrkoyvv0p6pu12hpmdey2/filmes.json?rlkey=62xtwp9y6xzwvdna5kngqdakz&st=p4dez1sw&dl=1',
    'https://www.dropbox.com/scl/fi/rzgdke7vi50wh6fxope5a/NETFLIX.json?rlkey=xveqhvf6l1p8if6ywr14u9rco&st=xtbfgjyt&dl=1',
    'https://www.dropbox.com/scl/fi/74tnl8qk4pwrs883x6ld6/series.json?rlkey=90jeiwtfn8bze7gf8k26lraeq&st=q7movfg6&dl=1'
]

def carregar_dados_json():
    dados_completos = []
    for url in json_urls:
        try:
            # Fazer o download do arquivo JSON
            response = requests.get(url)
            if response.status_code == 200:
                # Carregar o conteúdo JSON e adicionar aos dados completos
                dados = json.loads(response.content)
                dados_completos.extend(dados)
            else:
                print(f"Erro ao carregar JSON de {url}")
        except Exception as e:
            print(f"Erro ao carregar JSON de {url}: {e}")
    return dados_completos

@app.route('/api/venus', methods=['GET'])
def filmes_series():
    # Carregar dados dos três JSONs
    data = carregar_dados_json()

    # Retornar os dados combinados
    return jsonify({
        'total': len(data),
        'data': data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
