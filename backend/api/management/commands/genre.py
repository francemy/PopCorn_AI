import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import IntegrityError
from api.models import Movie, Genre
import ast
import math
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa filmes e seus gêneros a partir de um arquivo CSV.'

    def get_or_create_genres(self, genres_list):
        """
        Função que obtém ou cria gêneros para o filme a partir de uma lista de gêneros.
        Garante que o slug dos gêneros seja único.
        """
        genres = []
        for genre_name in genres_list:
            genre_name = genre_name.strip()  # Remove espaços extras
            if genre_name:
                # Gera o slug do gênero
                slug = slugify(genre_name)

                # Garantir que o slug seja único
                original_slug = slug
                counter = 1
                while Genre.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1

                # Cria o gênero ou pega o existente
                genre, created = Genre.objects.get_or_create(name=genre_name, defaults={'slug': slug})
                genres.append(genre)
        return genres

    def create_or_update_movie_with_genres(self, row):
        """
        Função que cria ou atualiza um filme e associa gêneros a ele.
        """
        title = row['title']
        description = row['overview']
        release_date = row['release_date']
        image_url = row['poster_path']
        genres_str = row['genres']  # Ajuste dependendo da estrutura dos dados no CSV
        # Converte a string de gêneros (presumindo que seja uma lista de gêneros separada por vírgulas)
        # Verifica se a variável 'genres' é uma string
        if isinstance(genres_str, str):
            # Converte a string de gêneros (presumindo que seja uma lista de gêneros separada por vírgulas)
            try:
                genre_vector = ast.literal_eval(genres_str)
                genres_list = [genre['name'] for genre in genre_vector]  # Extraindo os nomes dos gêneros
                self.stdout.write(self.style.SUCCESS(f'1 _ {genres_list}'))
            except (ValueError, SyntaxError) as e:
                self.stdout.write(self.style.ERROR(f'Erro ao converter a string de gêneros: {e}'))
        elif isinstance(genres_str, list):
            # Se for uma lista de dicionários, extraímos o 'name' de cada gênero
            genres_list = [genre['name'] for genre in genres_str]
            self.stdout.write(self.style.SUCCESS(f'2 _ {genres_list}'))
        # Verifica e ajusta a duração
        try:
            duration = float(row['runtime']) if row['runtime'] and not math.isnan(row['runtime']) else 1
        except ValueError:
            duration = 1  # Se não for um número válido, define como None

        # Verifica e ajusta a data de lançamento (release_date)
        try:
            if isinstance(release_date, str) and release_date.strip():  # Verifica se é uma string não vazia
                release_date = datetime.fromisoformat(release_date)  # Converte para um objeto datetime
            else:
                release_date = datetime.now()  # Se inválido ou ausente, define como None
        except ValueError:
            release_date = datetime.now()  # Se a data estiver no formato inválido, define como None

        # Gera o slug para o título do filme
        slug = slugify(title)

        # Garantir que o slug seja único
        original_slug = slug
        counter = 1
        while Movie.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Cria ou obtém o filme
        movie, created = Movie.objects.get_or_create(
            title=title,
            slug=slug,
            defaults={
                'description': description,
                'release_date': release_date,
                'duration': duration,
                'image_url': image_url,
            }
        )

        # Cria ou obtém os gêneros e associa ao filme
        genres = self.get_or_create_genres(genres_list)
        movie.genres.set(genres)
        movie.save()

    def handle(self, *args, **kwargs):
        # Define o caminho fixo para o arquivo CSV
        file_path = 'movies_metadata.csv'  # Caminho para o arquivo CSV
        #Movie.objects.update(genre=None)  # Aqui, você desvincula todos os filmes de seus gêneros

            # Agora, você pode excluir todos os objetos de Genre
        Genre.objects.all().delete() 
        try:
            # Lê o arquivo CSV
            df = pd.read_csv(file_path, low_memory=False)
            df_movies = df.head(10000)  # Limita a 10000 filmes para a importação
            
            for _, row in df_movies.iterrows():
                # Cria ou atualiza o filme com seus gêneros
                self.create_or_update_movie_with_genres(row)

            self.stdout.write(self.style.SUCCESS(f'{len(df_movies)} filmes foram importados com sucesso!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {file_path}'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro de integridade: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar filmes: {str(e)}'))
