import requests

# Chave da API e URL base da OMDb API
API_KEY = '609bf954'
BASE_URL = 'http://www.omdbapi.com/'

# Função para buscar um filme pelo título
def fetch_movie_by_title(title):
    params = {
        'apikey': API_KEY,
        't': title  # Título do filme
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Levanta um erro para status HTTP 4xx/5xx
        movie_data = response.json()  # Converte a resposta para um dicionário JSON
        return movie_data
    except requests.exceptions.RequestException as error:
        print(f"Erro ao buscar o filme: {error}")
        return None

# Exemplo de uso
movie = fetch_movie_by_title('Inception')
if movie:
    print(f"Titulo: {movie.get('Title')}")
    print(f"Ano: {movie.get('Year')}")
    print(f"Gênero: {movie.get('Genre')}")
    print(f"Sinopse: {movie.get('Plot')}")
else:
    print("Filme não encontrado.")


# Função para buscar filmes com base em um parâmetro (título, gênero, etc.)
def fetch_movies_by_genre(genre):
    params = {
        'apikey': API_KEY,
        's': genre  # Pesquisa por título ou palavra-chave (neste caso, gênero)
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Levanta um erro para status HTTP 4xx/5xx
        movie_data = response.json()  # Converte a resposta para um dicionário JSON
        if movie_data.get('Response') == 'True':
            return movie_data['Search']  # Retorna uma lista de filmes
        else:
            print(f"Erro: {movie_data.get('Error')}")
            return []
    except requests.exceptions.RequestException as error:
        print(f"Erro ao buscar filmes: {error}")
        return []

# Função para recomendar filmes baseados em gênero
def recommend_movies(genre):
    print(f"Recomendando filmes do gênero '{genre}':\n")
    movies = fetch_movies_by_genre(genre)
    
    if movies:
        for idx, movie in enumerate(movies, 1):
            print(f"{idx}. Título: {movie.get('Title')} - Ano: {movie.get('Year')} - Tipo: {movie.get('Type')}")
    else:
        print("Nenhum filme encontrado.")

