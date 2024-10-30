from flask import Flask, jsonify, request
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
            # Fazer o download do arquivo JSON com timeout
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados = json.loads(response.content)
                if isinstance(dados, list):
                    dados_completos.extend(dados)
                else:
                    print(f"O JSON de {url} não é uma lista e será ignorado.")
            else:
                print(f"Erro ao carregar JSON de {url} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar JSON de {url}: {e}")
    return dados_completos

@app.route('/api/venus', methods=['GET'])
def filmes_series():
    # Carregar dados dos três JSONs
    data = carregar_dados_json()
    
    # Paginação
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))  # Limitar a 50 itens por página
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    # Retornar os dados paginados
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(data),
        'data': paginated_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
