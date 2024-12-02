from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status, viewsets,generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
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
from .utils import get_movie_interactions, get_user_interactions  # Importando a função

# Utilitário para respostas uniformes
def create_response(message, data=None, status_code=status.HTTP_200_OK):
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return Response(response, status=status_code)

class PreferenceCreateView(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
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
            return Response(
                {
                    "message": "Preferência criada com sucesso.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        # Se o serializer não for válido, retorna os erros
        return Response(
            {
                "message": "Erro na criação da preferência.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



class UserCreateView(APIView):
    """
    View para criação de usuários.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return create_response(
                "Usuário criado com sucesso.",
                {
                    "username": user.username,
                    "email": user.email,
                },
                status.HTTP_201_CREATED,
            )
        return create_response("Erro na criação do usuário.",None, serializer.errors, status.HTTP_400_BAD_REQUEST)

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
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthenticationUserObtainPairView(APIView):
    """
    View personalizada para autenticação de usuários e obtenção de tokens JWT.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return create_response(message="Username e senha são obrigatórios.", status_code=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return create_response(message="Credenciais inválidas.", status_code=status.HTTP_401_UNAUTHORIZED)

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
            status.HTTP_200_OK,
        )


class RatingListCreateView(APIView):
    """
    View para listar e criar avaliações de filmes.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return create_response(message="Lista de avaliações recuperada com sucesso.", data=serializer.data, status_code=200)

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response(message="Avaliação criada com sucesso.",data=serializer.data,status_code=status.HTTP_201_CREATED)
        return create_response(message="Erro ao criar avaliação.",data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class MovieByGenreView(APIView):
    """
    View para listar filmes por gênero.
    """
    permission_classes = [AllowAny]

    def get(self, request, genre_id):
        try:
            genre = Genre.objects.get(id=genre_id)
            movies = Movie.objects.filter(genres=genre)
            serializer = MovieSerializer(movies, many=True)
            return create_response(message="Filmes encontrados para o gênero.", data=serializer.data,status_code=200)
        except Genre.DoesNotExist:
            return create_response(message="Gênero não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


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

        return create_response(message="Lista de filmes recuperada com sucesso.", data=movie_data, status_code=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            genre_ids = request.data.get("genres", [])
            if not genre_ids:
                return create_response(
                    "Pelo menos um gênero é necessário.", None,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return create_response(
                message="Filme criado com sucesso.",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return create_response(message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)



class GenreListView(APIView):
    """
    View para listar todos os gêneros de filmes.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        genres = Genre.objects.all()
        if not genres.exists():
            return create_response(message="Nenhum gênero encontrado.", status_code=status.HTTP_204_NO_CONTENT)

        serializer = GenreSerializer(genres, many=True)
        return create_response(message="Lista de gêneros recuperada com sucesso.", data=serializer.data)
    
@api_view(['GET'])
def get_movie_recommendations(request):
    authentication_classes = [JWTAuthentication]
    user_id = request.query_params.get('user_id', None)
    if user_id is None:
        return create_response("User ID is required", status_code=400)

    # Pegando os filmes e avaliações do banco de dados
    movies = Movie.objects.all()
    ratings = Rating.objects.filter(user_id=user_id)

    # Convertendo filmes e avaliações para DataFrame do Pandas
    movie_data = pd.DataFrame(list(movies.values()))
    rating_data = pd.DataFrame(list(ratings.values()))

    # Se o usuário tem avaliações, filtramos com base nas avaliações dele
    if not rating_data.empty:
        # Calculando a média das avaliações dos filmes
        rating_avg = rating_data.groupby('movie_id')['rating'].mean().reset_index()
        
        # Juntando as informações de filmes com a média de avaliação
        movie_data = movie_data.merge(rating_avg, how='left', left_on='id', right_on='movie_id')
        
        # Filtrando filmes com a melhor média de avaliações
        recommendations = movie_data.sort_values(by='rating', ascending=False).head(10)
    else:
        # Caso o usuário não tenha feito avaliações, recomendamos os 10 filmes mais populares (pode ser ajustado)
        recommendations = movie_data.head(10)

    # Convertendo os dados de volta para uma lista de títulos
    movie_titles = recommendations['title'].tolist()

    return create_response(message="Recomendações de filmes",data=movie_titles)


@api_view(['GET'])
def get_movie_recommendations2(request):
    user_id = request.query_params.get('user_id', None)
    if user_id is None:
        return create_response("User ID is required", status_code=400)

    # Pegando os filmes e avaliações do banco de dados
    movies = Movie.objects.all()
    ratings = Rating.objects.filter(user_id=user_id)

    # Convertendo filmes e avaliações para DataFrame do Pandas
    movie_data = pd.DataFrame(list(movies.values()))
    rating_data = pd.DataFrame(list(ratings.values()))

    # Inicializando as recomendações
    movie_titles = []

    # Agente 1 - Recomendação com base nas avaliações do usuário
    if not rating_data.empty:
        # Calculando a média das avaliações dos filmes
        rating_avg = rating_data.groupby('movie_id')['rating'].mean().reset_index()

        # Juntando as informações de filmes com a média de avaliação
        movie_data = movie_data.merge(rating_avg, how='left', left_on='id', right_on='movie_id')

        # Ordenando por classificação e selecionando os 10 melhores filmes
        agent_1_recommendations = movie_data.sort_values(by='rating', ascending=False).head(10)
        movie_titles.extend(agent_1_recommendations['title'].tolist())
    else:
        movie_titles.extend(movie_data.head(10)['title'].tolist())

    # Agente 2 - Recomendação com base na popularidade (filmes mais avaliados)
    movie_rating_counts = rating_data.groupby('movie_id').size().reset_index(name='count')
    movie_data = movie_data.merge(movie_rating_counts, how='left', left_on='id', right_on='movie_id')

    # Ordenando por número de avaliações e selecionando os 10 mais populares
    agent_2_recommendations = movie_data.sort_values(by='count', ascending=False).head(10)
    movie_titles.extend(agent_2_recommendations['title'].tolist())

    # Remover filmes duplicados (caso haja)
    movie_titles = list(dict.fromkeys(movie_titles))

    return create_response(message="Recomendações de filmes",data= movie_titles)

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
            return create_response(message="Erro de validação", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return create_response(message=f"Erro ao criar o gênero: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        """
        Sobrescreve a função de listagem para retornar uma resposta personalizada.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return create_response(message="Lista de gêneros carregada com sucesso.", data=serializer.data,status_code=200)
        except Exception as e:
            return create_response(message=f"Erro ao carregar os gêneros: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()  # Gêneros disponíveis para edição e exclusão
    serializer_class = GenreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

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
            return create_response(message="Erro de validação", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return create_response(message=f"Erro ao atualizar o gênero: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve a função de exclusão para retornar uma resposta personalizada.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return create_response(message="Gênero excluído com sucesso.", status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return create_response(message=f"Erro ao excluir o gênero: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer
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
        
        return Response(data)

# views.py

class WatchedMovieViewSet(viewsets.ModelViewSet):
    queryset = WatchedMovie.objects.all()
    serializer_class = WatchedMovieSerializer
    permission_classes = [IsAuthenticated]

    # Recuperar detalhes do WatchedMovie incluindo o usuário e o filme
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Pega o WatchedMovie pela chave primária (ID)
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
        
        return Response(data)
# views.py

class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
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
        
        return Response(data)
