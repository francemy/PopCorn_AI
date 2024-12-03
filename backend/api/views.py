from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets,generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view

from .machineLern import build_interaction_matrix, build_knn_model, recommend_movies_collaborative
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
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
    LikeDislikeSerializer
)
from .utils import get_movie_interactions, get_user_interactions,create_response  # Importando a função
from django.db.models import Avg,Count,Q
from .machineLern import build_interaction_matrix, build_knn_model, recommend_movies_collaborative, recommend_movies_content_based, recommend_movies_user_based

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
    #authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return create_response(
                message="Usuário criado com sucesso.",
                data={
                    "username": user.username,
                    "email": user.email,
                },
                status_code=200,
            )
        return create_response(message="Erro na criação do usuário.",data=serializer.errors, status_code=400)
    
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
        """
        movie_id = request.data.get('movie')
        user = request.user
        
        # Verifica se o usuário já avaliou esse filme
        existing_rating = Rating.objects.filter(user=user, movie_id=movie_id).first()

        # Se já existe uma avaliação, atualiza a avaliação
        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # Atualiza a avaliação com os novos dados
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
                serializer.save()  # Cria a nova avaliação
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
    View para listar e criar filmes.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get(self, request):
        user = request.user  # Pega o usuário logado
        movies = Movie.objects.all()
        movie_data = []

        # Adicionando interações personalizadas para o usuário logado
        for movie in movies:
            movie_info = MovieSerializer(movie).data  # Serializa os dados básicos do filme
            interactions = get_movie_interactions(movie)  # Obtém as interações gerais
            user_interactions = get_user_interactions(movie, user)  # Obtém as interações do usuário logado
            # Atualiza as interações específicas do usuário
            movie_info['user_interactions'] = user_interactions
            # Atualiza as interações gerais no filme
            movie_info.update(interactions)

            movie_data.append(movie_info)

        return create_response(message="Lista de filmes recuperada com sucesso.", data=movie_data, status_code=200)

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

class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()  # Retorna todos os gêneros
    serializer_class = GenreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Validação de dados antes de criar um novo gênero
        genre_name = serializer.validated_data.get('name', '').strip()
        if not genre_name:
            raise ValidationError({"message": "O nome do gênero é obrigatório."})

        # Verificar se o nome do gênero já existe
        if Genre.objects.filter(name=genre_name).exists():
            raise ValidationError({"message": "Já existe um gênero com esse nome."})

        # Se tudo estiver certo, cria o gênero
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve a função de criação para retornar uma resposta personalizada.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return create_response(message="Erro de validação", data=e.detail, status_code=400)
        except Exception as e:
            return create_response(message=f"Erro ao criar o gênero: {str(e)}", status_code=500)

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve a função de listagem para retornar uma resposta personalizada.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return create_response(message="Lista de gêneros carregada com sucesso.", data=serializer.data,status_code=200)
        except Exception as e:
            return create_response(message=f"Erro ao carregar os gêneros: {str(e)}", status_code=500)


class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()  # Gêneros disponíveis para edição e exclusão
    serializer_class = GenreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Sobrescreve a função de atualização para retornar uma resposta personalizada.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return create_response(message="Gênero atualizado com sucesso.", data=serializer.data,status_code=200)
        except ValidationError as e:
            return create_response(message="Erro de validação", data=e.detail, status_code=400)
        except Exception as e:
            return create_response(message=f"Erro ao atualizar o gênero: {str(e)}", status_code=500)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve a função de exclusão para retornar uma resposta personalizada.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return create_response(message="Gênero excluído com sucesso.", status_code=204)
        except Exception as e:
            return create_response(message=f"Erro ao excluir o gênero: {str(e)}", status_code=500)
        


class DashboardView(APIView):
    """
    View para retornar os dados consolidados do dashboard.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obter todos os filmes e gêneros
        movies = Movie.objects.all()
        genres = Genre.objects.all()

        # Serializar filmes e gêneros
        movie_serializer = MovieSerializer(movies, many=True)
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

        # Dados consolidados para o dashboard
        dashboard_data = {
            "movies": movie_serializer.data,
            "genres": genre_serializer.data,
            "ratings": ratings_by_genre,
            "interactions": interactions,
            "genreDistribution": genre_distribution_data,
        }

        return create_response(
            message="Dados consolidados do dashboard",
            data=dashboard_data
        )
    
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
            return create_response({'message': 'Filme não encontrado'}, status=404)

        # Marca o filme como assistido ou atualiza o contador
        watched_movie, created = WatchedMovie.objects.get_or_create(user=user, movie=movie)

        if created:
            # Se o filme for marcado pela primeira vez como assistido
            watched_movie.watch_count = 1  # Inicializa o contador de assistências
            watched_movie.save()
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
        
        return create_response(message="feito",data=data)

    @action(detail=False, methods=['post'])
    def like_dislike_action(self, request):
        """
        Esta ação permite alternar entre like, dislike e none.
        """
        movie_id = request.data.get('movie_id')
        action = request.data.get('action')
        user = request.user

        # Garantir que a ação seja válida
        if action not in ['like', 'dislike', 'none']:
            return create_response(message="error Ação inválida.", status_code=400)

        # Verifica se já existe uma interação para esse usuário e filme
        like_dislike_instance, created = LikeDislike.objects.update_or_create(
            user=user, movie_id=movie_id,
            defaults={'action': action}
        )

        return create_response(message="Ação de like/dislike realizada com sucesso.", data=LikeDislikeSerializer(like_dislike_instance).data, status_code=200)


class PersonalizedRecommendationsViewOrdeby(APIView):
    """
    Gera recomendações de filmes personalizadas no formato esperado.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Obter gêneros favoritos do usuário
        favorite_genres = Preference.objects.filter(user=user, preference_type="favorite").order_by('-priority')
        favorite_genre_ids = [pref.genre.id for pref in favorite_genres]

        # 2. Excluir filmes já assistidos ou avaliados negativamente
        watched_movie_ids = WatchedMovie.objects.filter(user=user).values_list('movie_id', flat=True)
        disliked_movie_ids = LikeDislike.objects.filter(user=user, action="dislike").values_list('movie_id', flat=True)
        excluded_movie_ids = set(watched_movie_ids).union(disliked_movie_ids)

        # 3. Filtrar filmes baseados nos gêneros favoritos e excluir os já assistidos/avaliados
        movies = (
            Movie.objects.filter(
                Q(genres__id__in=favorite_genre_ids)
            )
            .exclude(id__in=excluded_movie_ids)
            .distinct()
            .annotate(
                likes_count=Count('likes_disliked_by', filter=Q(likes_disliked_by__action="like")),
                dislikes_count=Count('likes_disliked_by', filter=Q(likes_disliked_by__action="dislike")),
                favorite_count=Count('favorited_by'),
                watched_count=Count('users_watched'),
                avg_rating=Avg('ratings__rating'),  # Média das avaliações
            )
            .prefetch_related('genres')  # Otimiza a busca dos gêneros relacionados
            .order_by(
                F('avg_rating').desc(nulls_last=True),  # Ordena por rating (nulos vão para o final)
                F('watched_count').desc(),             # Depois por número de assistências
                F('likes_count').desc()                # Depois por likes
            )
        )

        # 4. Preparar o formato esperado
        liked_disliked_movies = LikeDislike.objects.filter(user=user)
        favorited_movies = FavoriteMovie.objects.filter(user=user)
        watched_movies = WatchedMovie.objects.filter(user=user)

        movie_list = []
        for movie in movies:
            # Obter interações do usuário logado com o filme
            user_liked_disliked = liked_disliked_movies.filter(movie=movie).first()
            user_favorited = favorited_movies.filter(movie=movie).exists()
            user_watched = watched_movies.filter(movie=movie).first()

            user_interactions = {
                "liked": user_liked_disliked.action if user_liked_disliked else "none",
                "favorited": user_favorited,
                "watched": user_watched.watch_count if user_watched else 0,
            }

            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "duration": movie.duration,
                "image_url": movie.image_url,
                "genres": [genre.name for genre in movie.genres.all()],
                "likes_count": movie.likes_count,
                "dislikes_count": movie.dislikes_count,
                "favorite_count": movie.favorite_count,
                "watched_count": movie.watched_count,
                "user_interactions": user_interactions,
                "rating": movie.avg_rating,
            }

            movie_list.append(movie_data)

        # 5. Retornar a lista de filmes no formato esperado
        return create_response(
            message="Recomendações personalizadas com base nas suas preferências.",
            data=movie_list,
            status_code=200
        )


class CollaborativeRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user=request.user
        # Carregar a matriz de interações
        interaction_matrix = build_interaction_matrix()
        
        # Construir o modelo KNN
        knn = build_knn_model(interaction_matrix)
        
        # Obter as recomendações colaborativas
        
        recommended_movie_ids = [movie_id for movie_id in recommended_movie_ids if isinstance(movie_id, int)]

        
        liked_disliked_movies = LikeDislike.objects.filter(user=user)
        favorited_movies = FavoriteMovie.objects.filter(user=user)
        watched_movies = WatchedMovie.objects.filter(user=user)
        # Criar a resposta com as informações detalhadas dos filmes recomendados
        movie_list = []
        for movie in Movie.objects.filter(id__in=recommended_movie_ids):
            user_liked_disliked = liked_disliked_movies.filter(movie=movie).first()
            user_favorited = favorited_movies.filter(movie=movie).exists()
            user_watched = watched_movies.filter(movie=movie).first()

            user_interactions = {
                "liked": user_liked_disliked.action if user_liked_disliked else "none",
                "favorited": user_favorited,
                "watched": user_watched.watch_count if user_watched else 0,
            }
            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "duration": movie.duration,
                "image_url": movie.image_url,
                "genres": [genre.name for genre in movie.genres.all()],
                "likes_count": movie.likes_count,
                "dislikes_count": movie.dislikes_count,
                "favorite_count": movie.favorite_count,
                "watched_count": movie.watched_count,
                "user_interactions": user_interactions,
                "rating": movie.avg_rating,
            }
            movie_list.append(movie_data)
        
        # Retornar a resposta no formato desejado
        return create_response(
            message="Recomendações personalizadas com base nas suas preferências.",
            data=movie_list,
            status_code=200
        )


class ContentBasedRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Carregar os filmes e calcular similaridades
        user = request.user
        movie_id = 1
        movies_data = []
        for movie in Movie.objects.all():
            genres_str = ', '.join([genre.name for genre in movie.genres.all()])
            movie_id = movie.id
            movies_data.append({'movie_id': movie.id, 'title': movie.title, 'genres': genres_str})
        
        movies_df = pd.DataFrame(movies_data)
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Obter as recomendações baseadas em conteúdo
        recommended_movies = recommend_movies_content_based(movie_id, cosine_sim, movies_df)

        liked_disliked_movies = LikeDislike.objects.filter(user=user)
        favorited_movies = FavoriteMovie.objects.filter(user=user)
        watched_movies = WatchedMovie.objects.filter(user=user)
        # Criar a resposta com as informações detalhadas dos filmes recomendados
        movie_list = []
        for movie in Movie.objects.filter(id__in=recommended_movies):
            user_liked_disliked = liked_disliked_movies.filter(movie=movie).first()
            user_favorited = favorited_movies.filter(movie=movie).exists()
            user_watched = watched_movies.filter(movie=movie).first()

            user_interactions = {
                "liked": user_liked_disliked.action if user_liked_disliked else "none",
                "favorited": user_favorited,
                "watched": user_watched.watch_count if user_watched else 0,
            }
            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "duration": movie.duration,
                "image_url": movie.image_url,
                "genres": [genre.name for genre in movie.genres.all()],
                "likes_count": movie.likes_count,
                "dislikes_count": movie.dislikes_count,
                "favorite_count": movie.favorite_count,
                "watched_count": movie.watched_count,
                "user_interactions": user_interactions,
                "rating": movie.avg_rating,
            }
            movie_list.append(movie_data)
        
        # Retornar a resposta no formato desejado
        return create_response(
            message="Recomendações personalizadas com base nas suas preferências.",
            data=movie_list,
            status_code=200
        )

class ContentBasedRecommendationsView1(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # Obter os filmes curtidos pelo usuário
        liked_movies = LikeDislike.objects.filter(user=user, action='like').values_list('movie_id', flat=True)

        if liked_movies.exists():
            # Usar os filmes curtidos para calcular recomendações
            movies_data = []
            for movie in Movie.objects.all():
                genres_str = ', '.join([genre.name for genre in movie.genres.all()])
                movies_data.append({'movie_id': movie.id, 'title': movie.title, 'genres': genres_str})
            
            movies_df = pd.DataFrame(movies_data)
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

            # Gerar as recomendações para todos os filmes curtidos
            recommended_movie_ids = set()
            for liked_movie_id in liked_movies:
                recommended_ids = recommend_movies_content_based(liked_movie_id, cosine_sim, movies_df)
                recommended_movie_ids.update(recommended_ids)
        else:
            # Caso não existam filmes curtidos, recomendar filmes populares ou genéricos
            recommended_movie_ids = Movie.objects.order_by('-likes_count')[:10].values_list('id', flat=True)

        # Criar a resposta com os dados dos filmes recomendados
        recommended_movies = Movie.objects.filter(id__in=recommended_movie_ids).distinct()
        liked_disliked_movies = LikeDislike.objects.filter(user=user)
        favorited_movies = FavoriteMovie.objects.filter(user=user)
        watched_movies = WatchedMovie.objects.filter(user=user)

        movie_list = []
        for movie in recommended_movies:
            user_liked_disliked = liked_disliked_movies.filter(movie=movie).first()
            user_favorited = favorited_movies.filter(movie=movie).exists()
            user_watched = watched_movies.filter(movie=movie).first()

            user_interactions = {
                "liked": user_liked_disliked.action if user_liked_disliked else "none",
                "favorited": user_favorited,
                "watched": user_watched.watch_count if user_watched else 0,
            }
            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "duration": movie.duration,
                "image_url": movie.image_url,
                "genres": [genre.name for genre in movie.genres.all()],
                "likes_count": movie.likes_count,
                "dislikes_count": movie.dislikes_count,
                "favorite_count": movie.favorite_count,
                "watched_count": movie.watched_count,
                "user_interactions": user_interactions,
                "rating": movie.avg_rating,
            }
            movie_list.append(movie_data)
        
        # Retornar a resposta no formato desejado
        return create_response(
            message="Recomendações personalizadas com base em suas interações.",
            data=movie_list,
            status_code=200
        )
class HybridRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # Carregar a matriz de interações e o modelo KNN
        interaction_matrix = build_interaction_matrix()  # Matriz de interações do sistema
        knn = build_knn_model(interaction_matrix)  # Modelo KNN para usuários

        # Obter preferências do usuário logado
        liked_movies = LikeDislike.objects.filter(user=user, action='like').values_list('movie_id', flat=True)
        preferred_genres = Preference.objects.filter(user=user).values_list('genre', flat=True)

        # Filmes recomendados por conteúdo e gêneros
        movies_data = []
        for movie in Movie.objects.all():
            genres_str = ', '.join([genre.name for genre in movie.genres.all()])
            movies_data.append({'movie_id': movie.id, 'title': movie.title, 'genres': genres_str})

        movies_df = pd.DataFrame(movies_data)
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Combinar métodos: híbrido (KNN + Conteúdo)
        recommended_movies = set()

        if liked_movies.exists():
            # Recomendações baseadas no conteúdo
            for liked_movie_id in liked_movies:
                content_recommendations = recommend_movies_content_based(
                    liked_movie_id, cosine_sim, movies_df
                )
                recommended_movies.update(content_recommendations)

            # Recomendações baseadas no usuário (KNN)
            user_based_recommendations = recommend_movies_user_based(
                user.id, interaction_matrix, knn
            )
            recommended_movies.update(user_based_recommendations)
        else:
            # Caso não haja interações, sugerir filmes com base nos gêneros favoritos ou populares
            if preferred_genres:
                recommended_movies = set(
                    Movie.objects.filter(genres__in=preferred_genres).order_by('-likes_count')[:10].values_list('id', flat=True)
                )
            else:
                recommended_movies = set(Movie.objects.order_by('-likes_count')[:10].values_list('id', flat=True))

        # Organizar interações do usuário (evitar múltiplas consultas no banco dentro do loop)
        liked_disliked_movies = LikeDislike.objects.filter(user=user)
        favorited_movies = FavoriteMovie.objects.filter(user=user)
        watched_movies = WatchedMovie.objects.filter(user=user)

        # Organizando os dados de interações em dicionários para consulta eficiente
        liked_disliked_dict = {ld.movie_id: ld.action for ld in liked_disliked_movies}
        favorited_dict = {fm.movie_id: fm for fm in favorited_movies}
        watched_dict = {wm.movie_id: wm for wm in watched_movies}

        # Buscar filmes recomendados do banco de dados
        recommended_movies_queryset = Movie.objects.filter(id__in=recommended_movies).distinct()

        movie_list = []
        for movie in recommended_movies_queryset:
            user_liked_disliked = liked_disliked_dict.get(movie.id, 'none')
            user_favorited = favorited_dict.get(movie.id, False)
            user_watched = watched_dict.get(movie.id, None)

            user_interactions = {
                "liked": user_liked_disliked,
                "favorited": user_favorited,
                "watched": user_watched.watch_count if user_watched else 0,
            }

            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "duration": movie.duration,
                "image_url": movie.image_url,
                "genres": [genre.name for genre in movie.genres.all()],
                "likes_count": movie.likes_count,
                "dislikes_count": movie.dislikes_count,
                "favorite_count": movie.favorite_count,
                "watched_count": movie.watched_count,
                "user_interactions": user_interactions,
                "rating": movie.avg_rating,
            }
            movie_list.append(movie_data)

        # Retornar a resposta
        return create_response(
            message="Recomendações personalizadas com base nas suas preferências e interações.",
            data=movie_list,
            status_code=200
        )
