from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets,generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import authenticate
import pandas as pd
from .models import Movie, Rating, Genre,Preference,LikeDislike,WatchedMovie,FavoriteMovie
from .serializers import (
    UserSerializer,
    MovieSerializer,
    GenreSerializer,
    RatingSerializer,
    PreferenceSerializer,
    FavoriteMovieSerializer,
    WatchedMovieSerializer,
    LikeDislikeSerializer,
    PreferenceListSerializer
)
from .utils import create_response,get_movie_interactions,get_user_interactions,adjust_user_preferences,calculate_movie_score,get_user_favorite_genre_ids  # Importando a função
from django.db.models import Avg,Count,Q,F

class MoviePagination(PageNumberPagination):
    """
    Configuração de paginação personalizada.
    """
    page_size = 10  # Número de filmes por página
    page_size_query_param = 'page_size'  # Permitir que o cliente ajuste o tamanho
    max_page_size = 100  # Limite máximo para o tamanho da página
class PreferenceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Preference.objects.all()  # ou qualquer filtro que você precise
    serializer_class = PreferenceListSerializer


class PreferenceCreateView(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Garante que somente usuários autenticados possam acessar as preferências

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para associar a preferência
        ao usuário autenticado. O Django REST já valida a autenticação, então
        não há necessidade de uma validação explícita de 'is_authenticated'.
        """
        user = self.request.user
        # Salva a preferência associada ao usuário autenticado
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método create para personalizar a resposta
        quando uma nova preferência for criada.
        """
        # Valida os dados do serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
               message="Preferência criada com sucesso.",
                    data=serializer.data
              ,
                status_code=201
            )

        # Se o serializer não for válido, retorna os erros
        return create_response(message="Erro na criação da preferência."+str(serializer.errors),
            status_code=400
        )

class UserCreateView(APIView):
    """
    View para criação de usuários.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Ajusta os dados para enviar apenas os campos necessários
        data = request.data
        serializer = UserSerializer(data={
            'username': data.get('username'),
            'email': data.get('email'),
            'password': data.get('password'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
        })
        
        if serializer.is_valid():
            # Salva o usuário
            user = serializer.save()

            return create_response(
                message="Usuário criado com sucesso.",
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                status_code=201,  # Código de sucesso para criação
            )

        # Caso o serializer não seja válido, retorna erro com as falhas
        return create_response(
            message="Erro na criação do usuário.",
            data=serializer.errors,
            status_code=400,  # Código de erro para falha na validação
        )

class VerifyTokenView(APIView):
    """
    View para verificar se o token de acesso é válido.
    """
    def get(self, request):
        # Obtém o token do cabeçalho de autorização
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Token não fornecido ou inválido.")

        token = auth_header.split(' ')[1]  # Extrai o token
        try:
            # Valida o token
            access_token = AccessToken(token)
            return create_response(message="feito",data={"isValid": True}, status_code=200)
        except Exception as e:
            return create_response(message="feito",data={"isValid": False}, status_code=401)

class RefreshTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("Chegou na view CustomTokenObtainPairView")
        response = super().post(request, *args, **kwargs)
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            print("Usuário não autenticado")
            raise AuthenticationFailed("Usuário não autenticado")
        try:
            print("Usuário autenticado, criando o refresh token",request.user)
            refresh = RefreshToken.for_user(request.user)
            response.data['custom_data'] = {
                'message': 'Token gerado com sucesso',
                'user_id': request.user.id,
                'username': request.user.username
            }
            response.data['refresh'] = str(refresh)
            return create_response(message="",data=response.data, status_code=200)
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
            return create_response(message={'detail': str(e)}, status_code=400)
        
class AuthenticationUserObtainPairView(APIView):
    """
    View personalizada para autenticação de usuários e obtenção de tokens JWT.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return create_response(message="Username e senha são obrigatórios.", status_code=400)

        user = authenticate(username=username, password=password)
        if not user:
            return create_response(message="Credenciais inválidas.", status_code=401)

        refresh = RefreshToken.for_user(user)
        return create_response(
            "Login bem-sucedido.",
            {
                "user_id": user.id,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "custom_data": {
                    "role": getattr(user, "profile.role", "user"),
                    "last_login": user.last_login,
                },
            },
            200,
        )

class RatingCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que o usuário esteja autenticado

    def post(self, request, *args, **kwargs):
        """
        Cria ou atualiza uma avaliação para o filme.
        Se a avaliação já existir, atualiza a avaliação, caso contrário, cria uma nova.
        Além disso, ajusta a preferência do usuário com base na avaliação.
        """
        movie_id = request.data.get('movie')
        user = request.user
        rating_value = request.data.get('rating')  # Exemplo de valor da avaliação (de 1 a 5)

        # Verifica se o usuário já avaliou esse filme
        existing_rating = Rating.objects.filter(user=user, movie_id=movie_id).first()

        # Função para ajustar as preferências com base na avaliação
        def adjust_preferences_based_on_rating(action, weight):
            try:
                movie = Movie.objects.get(id=movie_id)
                adjust_user_preferences(user, movie.genres.all(), action, weight)  # Ajusta a preferência do usuário
            except Movie.DoesNotExist:
                pass

        # Se já existe uma avaliação, atualiza a avaliação
        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                updated_rating = serializer.save()  # Atualiza a avaliação com os novos dados

                # Ajusta a preferência baseada na avaliação
                if rating_value >= 3:
                    adjust_preferences_based_on_rating('favorite', 1)
                elif rating_value <= 2:
                    adjust_preferences_based_on_rating('avoid', -1)

                return create_response(
                    message='Avaliação atualizada com sucesso.',
                    data=serializer.data,
                    status_code=200
                )
            else:
                return create_response(
                    message='Erro na atualização da avaliação.',
                    data=serializer.errors,
                    status_code=400
                )
        
        # Se não existe avaliação, cria uma nova
        else:
            request.data['user'] = user.id  # Associando automaticamente o usuário autenticado
            serializer = RatingSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                created_rating = serializer.save()  # Cria a nova avaliação

                # Ajusta a preferência baseada na avaliação
                if rating_value >= 4:
                    adjust_preferences_based_on_rating('favorite', 1)
                elif rating_value <= 2:
                    adjust_preferences_based_on_rating('avoid', -1)

                return create_response(
                    message='Avaliação criada com sucesso.',
                    data=serializer.data,
                    status_code=201
                )
            else:
                return create_response(
                    message='Erro na criação da avaliação.',
                    data=serializer.errors,
                    status_code=400
                )

class MovieListCreateView(APIView):
    """
    View para listar e criar filmes com suporte à paginação.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get(self, request):
        user = request.user  # Pega o usuário logado
        movies = Movie.objects.all()

        # Filtrar por gênero, se fornecido
        genre_id = request.query_params.get("genre")
        if genre_id:
            try:
                genre_id = int(genre_id)  # Tenta converter para inteiro
                movies = movies.filter(genres__id=genre_id)
            except ValueError:
                # Se o gênero não for válido, retorna todos os filmes sem filtro
                movies = Movie.objects.all()
            except Movie.DoesNotExist:
                # Caso o gênero não exista na base de dados, retorna todos os filmes
                movies = Movie.objects.all()

        # Aplicar paginação
        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, request)

        movie_data = []

        # Adicionando interações personalizadas para o usuário logado
        for movie in paginated_movies:
            movie_info = MovieSerializer(movie).data  # Serializa os dados básicos do filme
            interactions = get_movie_interactions(movie)  # Obtém as interações gerais
            user_interactions = get_user_interactions(movie, user)  # Obtém as interações do usuário logado

            # Atualiza as interações específicas do usuário
            movie_info['user_interactions'] = user_interactions
            # Atualiza as interações gerais no filme
            movie_info.update(interactions)

            movie_data.append(movie_info)

        # Retorna a resposta paginada
        return paginator.get_paginated_response(movie_data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            genre_ids = request.data.get("genres", [])
            if not genre_ids:
                return create_response(
                    "Pelo menos um gênero é necessário.", None,
                    status_code=400,
                )

            serializer.save()
            return create_response(
                message="Filme criado com sucesso.",
                data=serializer.data,
                status_code=201
            )

        return create_response(message=serializer.errors, status_code=400)


class GenreListView(APIView):
    """
    View para listar todos os gêneros de filmes.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        genres = Genre.objects.all()
        if not genres.exists():
            return create_response(message="Nenhum gênero encontrado.", status_code=204)

        serializer = GenreSerializer(genres, many=True)
        return create_response(message="Lista de gêneros recuperada com sucesso.", data=serializer.data)


class DashboardView(APIView):
    """
    View para retornar os dados consolidados do dashboard.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obter todos os  e gêneros
        genres = Genre.objects.all()

        # Serializar  e gêneros
        genre_serializer = GenreSerializer(genres, many=True)

        # Avaliações médias por gênero
        avg_ratings = (
            Rating.objects.values("movie__genres__name")
            .annotate(avgRating=Avg("rating"))
            .distinct()
        )
        ratings_by_genre = [
            {"genre": r["movie__genres__name"], "avgRating": r["avgRating"]}
            for r in avg_ratings
        ]

        # Contagem de interações (likes, dislikes, favoritos e assistidos)
        interactions = {
            "likes": LikeDislike.objects.filter(action="like").count(),
            "dislikes": LikeDislike.objects.filter(action="dislike").count(),
            "favorites": FavoriteMovie.objects.count(),
            "watched": WatchedMovie.objects.count(),
        }

        # Distribuição de filmes por gênero
        genre_distribution = (
            Movie.objects.values("genres__name")
            .annotate(value=Count("id"))
        )
        genre_distribution_data = [
            {"name": g["genres__name"], "value": g["value"]} for g in genre_distribution
        ]
        
        preferences = Preference.objects.all()
        lista_preferences = []

        for preference in preferences:
            serialized_data = PreferenceSerializer(preference).data  # Serializa a preferência atual
            
            # Adiciona informações relacionadas
            serialized_data['genre'] = GenreSerializer(preference.genre).data  # Serializa o gênero associado
            serialized_data['username'] = preference.user.username  # Adiciona o nome do usuário

            lista_preferences.append(serialized_data)

        # Dados consolidados para o dashboard
        dashboard_data = {
            
            "genres": genre_serializer.data,
            "ratings": ratings_by_genre,
            "interactions": interactions,
            "genreDistribution": genre_distribution_data,
            "preferences": lista_preferences
        }

        return create_response(
            message="Dados consolidados do dashboard",
            data=dashboard_data
        )
    
# class PersonalizedRecommendationsViewOrdeby(APIView):
#     """
#     Gera recomendações de filmes personalizadas no formato esperado.
#     """
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         # 1. Obter gêneros favoritos do usuário
#         favorite_genre_ids = Preference.objects.filter(user=user, preference_type="favorite")\
#                                                  .order_by('-priority')\
#                                                  .values_list('genre_id', flat=True)

#         # 2. Excluir filmes já assistidos ou avaliados negativamente
#         watched_movie_ids = WatchedMovie.objects.filter(user=user).values_list('movie_id', flat=True)
#         disliked_movie_ids = LikeDislike.objects.filter(user=user, action="dislike").values_list('movie_id', flat=True)

#         # Combine os dois conjuntos no Python
#         excluded_movie_ids = set(watched_movie_ids) | set(disliked_movie_ids)

#         # 3. Buscar filmes baseados nos gêneros favoritos e excluir os já assistidos/avaliados
#         movies = Movie.objects.filter(
#             Q(genres__id__in=favorite_genre_ids)
#         ).exclude(
#             id__in=excluded_movie_ids
#         ).distinct()
#         movie_list = []
#         for movie in movies:
#             movie_info = MovieSerializer(movie).data  # Serializa os dados básicos do filme
#             interactions = get_movie_interactions(movie)  # Obtém as interações gerais
#             user_interactions = get_user_interactions(movie, user)  # Obtém as interações do usuário logado
#             # Atualiza as interações específicas do usuário
#             movie_info['user_interactions'] = user_interactions
#             # Atualiza as interações gerais no filme
#             movie_info.update(interactions)

#             movie_list.append(movie_info)

#         # 5. Retornar a lista de filmes
#         return create_response(
#             message="Recomendações personalizadas com base nas suas preferências.",
#             data=movie_list,
#             status_code=200
#         )


class PersonalizedRecommendationsViewOrdeby(APIView):
    """
    Gera recomendações de filmes personalizadas no formato esperado.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Obter gêneros favoritos do usuário, considerando prioridades e intensidade de preferência
        favorite_genre_ids = Preference.objects.filter(user=user, preference_type="favorite")\
                                                 .order_by('-priority')\
                                                 .values_list('genre_id', flat=True)

        # 2. Obter gêneros secundários ou similares, se o usuário tem filmes avaliados positivamente em outros gêneros
        secondary_genre_ids = Preference.objects.filter(user=user, preference_type="favorite")\
                                                 .exclude(genre_id__in=favorite_genre_ids)\
                                                 .values_list('genre_id', flat=True)

        # 3. Excluir filmes já assistidos ou avaliados negativamente
        watched_movie_ids = WatchedMovie.objects.filter(user=user).values_list('movie_id', flat=True)
        disliked_movie_ids = LikeDislike.objects.filter(user=user, action="dislike").values_list('movie_id', flat=True)
        
        # Combine os dois conjuntos no Python
        excluded_movie_ids = set(watched_movie_ids) | set(disliked_movie_ids)

        # 4. Buscar filmes baseados nos gêneros favoritos e secundários e excluir os já assistidos/avaliados
        movies = Movie.objects.filter(
            Q(genres__id__in=favorite_genre_ids) | Q(genres__id__in=secondary_genre_ids)
        ).exclude(
            id__in=excluded_movie_ids
        ).distinct()

        # 5. Calcular a pontuação para cada filme, com base na interação do usuário
        movie_list = []
        for movie in movies:
            movie_info = MovieSerializer(movie).data  # Serializa os dados básicos do filme
            interactions = self.get_movie_interactions(movie)  # Obtém as interações gerais do filme
            user_interactions = self.get_user_interactions(movie, user)  # Obtém as interações do usuário com o filme

            # Ajuste da pontuação do filme
            movie_score = self.calculate_movie_score(movie, user, favorite_genre_ids, secondary_genre_ids)  # Função para calcular a pontuação

            # Atualiza as interações e a pontuação do filme
            movie_info['user_interactions'] = user_interactions
            movie_info.update(interactions)
            movie_info['score'] = movie_score

            movie_list.append(movie_info)

        # Paginação usando a classe personalizada
        paginator = MoviePagination()
        result_page = paginator.paginate_queryset(movie_list, request)

        # Retorna a resposta paginada
        return paginator.get_paginated_response(result_page)

    def calculate_movie_score(self, movie, user, favorite_genre_ids, secondary_genre_ids):
        """
        Função para calcular a pontuação do filme baseada nas preferências de gênero e interações do usuário.
        """
        score = 0

        # Pontuação baseada nos gêneros favoritos, com pesos de prioridade
        for genre in movie.genres.all():
            if genre.id in favorite_genre_ids:
                # Peso maior para gêneros favoritos
                preference = Preference.objects.get(user=user, genre=genre)
                score += 2 * preference.priority  # Prioridade influencia o peso

            if genre.id in secondary_genre_ids:
                # Peso menor para gêneros secundários
                score += 1  # Peso básico

        # Pontuação baseada nas interações do usuário
        user_interactions = self.get_user_interactions(movie, user)
        if user_interactions.get('liked'):
            score += 3  # Aumenta a pontuação se o usuário gostou
        elif user_interactions.get('disliked'):
            score -= 3  # Diminui a pontuação se o usuário não gostou

        return score

    def get_movie_interactions(self, movie):
        """
        Função para retornar interações gerais com o filme.
        """
        likes = LikeDislike.objects.filter(movie=movie, action="like").count()
        dislikes = LikeDislike.objects.filter(movie=movie, action="dislike").count()
        return {"likes": likes, "dislikes": dislikes}

    def get_user_interactions(self, movie, user):
        """
        Função para obter as interações específicas do usuário com o filme.
        """
        like = LikeDislike.objects.filter(movie=movie, user=user, action="like").exists()
        dislike = LikeDislike.objects.filter(movie=movie, user=user, action="dislike").exists()
        return {"liked": like, "disliked": dislike}
  


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Recuperar detalhes do FavoriteMovie incluindo o usuário e o filme
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Pega o FavoriteMovie pela chave primária (ID)
        serializer = self.get_serializer(instance)

        # Adiciona detalhes do usuário e do filme no response
        data = serializer.data
        data['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        data['movie'] = {
            'id': instance.movie.id,
            'title': instance.movie.title,
            'description': instance.movie.description,
            'release_date': instance.movie.release_date,
            'duration': instance.movie.duration,
            'image_url': instance.movie.image_url,
        }
        
        return create_response(message="feito", data=data)

    @action(detail=False, methods=['post'])
    def favorite_movie_action(self, request):
        """
        Ação para adicionar/remover filme dos favoritos do usuário.
        """
        movie_id = request.data.get('movie_id')
        user = request.user

        # Verifica se o filme existe
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return create_response({'message': 'Filme não encontrado'}, status=404)

        # Cria ou atualiza o registro de favorito
        favorite_movie, created = FavoriteMovie.objects.get_or_create(user=user, movie=movie)

        if created:
            # Ajusta as preferências do usuário para os gêneros do filme favoritado
            adjust_user_preferences(user, movie.genres.all(), action='favorite', weight=1)
            return create_response(message='Filme adicionado aos favoritos com sucesso.', status_code=201)
        else:
            return create_response(message='O filme já está nos favoritos.', status_code=200)


class WatchedMovieViewSet(viewsets.ModelViewSet):
    queryset = WatchedMovie.objects.all()
    serializer_class = WatchedMovieSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Recuperar detalhes do WatchedMovie incluindo o usuário e o filme
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Pega o WatchedMovie pela chave primária (ID)

        # Verifica se o filme pertence ao usuário autenticado
        if instance.user != request.user:
            return create_response(message='Acesso negado', status_code=403)

        serializer = self.get_serializer(instance)

        # Adiciona detalhes do usuário e do filme no response
        data = serializer.data
        data['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        data['movie'] = {
            'id': instance.movie.id,
            'title': instance.movie.title,
            'description': instance.movie.description,
            'release_date': instance.movie.release_date,
            'duration': instance.movie.duration,
            'image_url': instance.movie.image_url,
        }

        return create_response(message="feito", data=data)

    @action(detail=False, methods=['post'])
    def mark_as_watched(self, request):
        """
        Ação para marcar um filme como assistido pelo usuário.
        """
        movie_id = request.data.get('movie_id')
        user = request.user

        # Verifica se o filme existe
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return create_response(message='Filme não encontrado', status_code=404)

        # Marca o filme como assistido ou atualiza o contador
        watched_movie, created = WatchedMovie.objects.get_or_create(user=user, movie=movie)

        if created:
            # Se o filme for marcado pela primeira vez como assistido
            watched_movie.watch_count = 1
            watched_movie.save()

            # Ajusta as preferências do usuário para os gêneros do filme assistido
            adjust_user_preferences(user, movie.genres.all(), action='favorite', weight=1)
            return create_response(message='Filme marcado como assistido com sucesso.', status_code=201)
        else:
            # Se o filme já foi assistido, incrementa o contador
            watched_movie.watch_count += 1
            watched_movie.save()
            return create_response(message='O filme já foi assistido. Contador incrementado.', status_code=200)



class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Recuperar detalhes do LikeDislike incluindo o usuário e o filme
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Pega o LikeDislike pela chave primária (ID)
        serializer = self.get_serializer(instance)

        # Adiciona detalhes do usuário e do filme no response
        data = serializer.data
        data['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        data['movie'] = {
            'id': instance.movie.id,
            'title': instance.movie.title,
            'description': instance.movie.description,
            'release_date': instance.movie.release_date,
            'duration': instance.movie.duration,
            'image_url': instance.movie.image_url,
        }
        
        return create_response(message="feito", data=data)

    @action(detail=False, methods=['post'])
    def like_dislike_action(self, request):
        """
        Esta ação permite alternar entre like, dislike e none.
        """
        movie_id = request.data.get('movie_id')
        action = request.data.get('action')
        user = request.user

        # Garantir que o filme exista
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return create_response(
                message="Filme não encontrado.",
                status_code=404
            )

        # Garantir que a ação seja válida
        if action not in ['like', 'dislike', 'none']:
            return create_response(
                message="Ação inválida. Escolha entre 'like', 'dislike' ou 'none'.",
                status_code=400
            )

        # Verifica se já existe uma interação para esse usuário e filme
        like_dislike_instance, created = LikeDislike.objects.update_or_create(
            user=user, movie=movie,
            defaults={'action': action}
        )

        # Ajustar preferências do usuário com base na ação
        if action == 'like':
            adjust_user_preferences(user, movie.genres.all(), action='favorite', weight=1)
        elif action == 'dislike':
            adjust_user_preferences(user, movie.genres.all(), action='avoid', weight=-1)

        message = "Ação de like/dislike realizada com sucesso."
        return create_response(message=message, data=LikeDislikeSerializer(like_dislike_instance).data, status_code=200)
