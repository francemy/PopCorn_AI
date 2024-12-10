from django.core.management.base import BaseCommand
from api.models import Movie  # Certifique-se de importar corretamente seus modelos
from api.OMDbAPI import fetch_movie_by_title  # Certifique-se de que esse arquivo está correto

class Command(BaseCommand):
    help = 'Atualiza a imagem do filme baseado no título, somente se a URL contiver "m.media-amazon.com/images/"'

    def handle(self, *args, **kwargs):
        # Buscar todos os filmes na base de dados
        movies = Movie.objects.all()
        
        for movie in movies:
            # Verificar se a URL da imagem não contém a string desejada
            if movie.image_url and "m.media-amazon.com/images/" not in movie.image_url:
                # Buscar dados do filme pela API usando o título do filme
                movie_data_response = fetch_movie_by_title(movie.title)
                
                if movie_data_response and movie_data_response.get('Response') == 'True':
                    # Obter a URL da imagem
                    image_url = movie_data_response.get('Poster')
                    
                    # Atualizar a imagem no banco de dados, se a URL não estiver vazia
                    if image_url:
                        movie.image_url = image_url
                        movie.save()
                        self.stdout.write(self.style.SUCCESS(f"Imagem do filme '{movie.title}' atualizada com sucesso."))
                    else:
                        self.stdout.write(self.style.ERROR(f"Imagem não encontrada para o filme '{movie.title}'."))
                else:
                    self.stdout.write(self.style.ERROR(f"Erro ao buscar dados para o filme '{movie.title}'."))
            else:
                self.stdout.write(self.style.SUCCESS(f"A imagem do filme '{movie.title}' já está correta."))
