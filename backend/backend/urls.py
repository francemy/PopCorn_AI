from django.contrib import admin
from django.urls import path, include, re_path
from api.views import RefreshTokenObtainPairView, AuthenticationUserObtainPairView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from api.views import (VerifyTokenView,PersonalizedRecommendationsViewOrdeby,
                        DashboardView, MovieListCreateView, 
                       PreferenceCreateView, RatingCreateUpdateView, GenreListView, UserCreateView,
                       FavoriteMovieViewSet, WatchedMovieViewSet, LikeDislikeViewSet,PreferenceListView
                       )

# Gerador da documentação Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configuração do roteador
router = DefaultRouter()
router.register(r'preferences', PreferenceCreateView)
router.register(r'favorite_movies', FavoriteMovieViewSet, basename='favorite_movie')
router.register(r'watched_movies', WatchedMovieViewSet, basename='watched_movie')
router.register(r'like_dislike', LikeDislikeViewSet, basename='like_dislike')
# URLs da API
urlpatterns = [
    path('api/preferences/list', PreferenceListView.as_view(), name='preference-list'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/genres/', GenreListView.as_view(), name='genre-list'),
    path('api/movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('api/movies/recomendado/', PersonalizedRecommendationsViewOrdeby.as_view(), name='movie-recomendados'),
    path('api/ratings/create/', RatingCreateUpdateView.as_view(), name='rating-list-create'),
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/token/', AuthenticationUserObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', RefreshTokenObtainPairView.as_view(), name='token_refresh'),
    path('api/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('api/', include(router.urls)),
]
