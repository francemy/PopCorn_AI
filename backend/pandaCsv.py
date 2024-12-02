import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # Substitua 'myproject' pelo nome do seu projeto Django

import django
django.setup()
import pandas as pd
import ast
from datetime import datetime
from api.models import Movie, Genre, User  # Substitua 'myapp' pelo nome real do seu app Django
from django.utils.text import slugify

# Carregar o arquivo CSV sem forçar o tipo de dados
df = pd.read_csv('./movies_metadata.csv', low_memory=False)

# Converter as colunas 'budget' e 'revenue' para números, substituindo os valores inválidos por NaN
# df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
# df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# Verifique se a conversão foi bem-sucedida
# print("Verifique se a conversão foi bem-sucedida: ",df[['budget', 'revenue']].head())

# print("Verificar valores nulos em todas as colunas:",df.isnull().sum())


# Substituir NaN por 0
# df.fillna(0, inplace=True)

# # Calcular a média de budget e revenue
# print(f'Média do orçamento: {df["budget"].mean()}')
# print(f'Média da receita: {df["revenue"].mean()}')

def extract_genres(genre_column):
    try:
        genres = ast.literal_eval(genre_column)  # Converte a string em lista de dicionários
        return ', '.join([genre['name'] for genre in genres])  # Extrai e junta os nomes dos gêneros
    except:
        return None  # Caso não seja possível converter ou não haja gêneros

# Aplicar a função para extrair os gêneros
#df['genres_list'] = df['genres'].apply(extract_genres)

# Exibir os títulos dos filmes e seus gêneros
#print(df[['title', 'genres_list']].head(30))

# num_colunas = len(df.columns)
# print(f'Número de colunas: {num_colunas}')

# # Exibir os nomes das colunas
# print('Nomes das colunas:')
# print(df.columns.tolist())



df_movies = df.head(30)
# Função para criar filmes no banco de dados
def create_movie(movie_data):
    # Atribuindo valores aos campos
    title = movie_data['title']
    description = movie_data['overview'] if isinstance(movie_data['overview'], str) else ""
    release_date = datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date()
    duration = int(movie_data['runtime']) if pd.notna(movie_data['runtime']) else 0
    image_url = movie_data['poster_path'] if pd.notna(movie_data['poster_path']) else None
    
    # Criando ou buscando os gêneros
    genres_data = eval(movie_data['genres'])  # Isso converte a string de lista de dicionários em uma lista de objetos
    genres = []
    for genre in genres_data:
        genre_name = genre['name']
        genre, created = Genre.objects.get_or_create(name=genre_name)
        genres.append(genre)
    
    # Criando o filme
    movie = Movie(
        title=title,
        slug=slugify(title),
        description=description,
        release_date=release_date,
        duration=duration,
        image_url=image_url
    )
    movie.save()  # Salva o filme no banco de dados
    
    # Atribuindo os gêneros ao filme
    movie.genres.set(genres)
    movie.save()

    return movie

# Criar 30 filmes
for index, row in df_movies.iterrows():
    create_movie(row) 


# Função para exibir título e os dados do filme conforme o modelo
def show_movie_details():
    for index, row in df_movies.iterrows():
        title = row['title']
        slug = slugify(title)  # Gerando o slug automaticamente
        description = row['overview']
        release_date = row['release_date']
        duration = row['runtime']
        image_url = row['poster_path']
        
        # Verificando se a data está no formato correto (ano-mês-dia)
        try:
            release_date = datetime.strptime(str(release_date), "%Y-%m-%d").date()
        except:
            release_date = "Data não disponível"
        
        # Extraindo os gêneros da lista
        genres = row['genres']
        genre_names = []
        try:
            genre_list = eval(genres)  # Converte a string para lista de dicionários
            genre_names = [genre['name'] for genre in genre_list]
        except:
            genre_names = ["Gênero não disponível"]

        print(f"Title: {title} \n")
        print(f"Slug: {slug}\n")
        print(f"Description: {description}\n")
        print(f"Release Date: {release_date}\n")
        print(f"Duration: {duration} minutos\n")
        print(f"Image URL: {image_url}")
        print(f"Genres: {', '.join(genre_names)}\n")
        print("-" * 80)
        print("\n")

# Exibir os detalhes do filme
show_movie_details()