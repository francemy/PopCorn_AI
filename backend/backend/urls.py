from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import RefreshTokenObtainPairView, AuthenticationUserObtainPairView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from api.views import GenreListCreateView, GenreRetrieveUpdateDestroyView,PreferenceCreateView, PreferenceListView,MovieListCreateView,PreferenceViewSet, RatingListCreateView, MovieByGenreView, GenreListView ,UserCreateView,get_movie_recommendations

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
router = DefaultRouter()
router.register(r'preferences', PreferenceViewSet)

urlpatterns = [
   path('api/genres/', GenreListView.as_view(), name='genre-list'),
   path('api/movies/', MovieListCreateView.as_view(), name='movie-list-create'),
   path('movies/genre/<int:genre_id>/', MovieByGenreView.as_view(), name='movie-by-genre'),
   path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
   path('api/register/', UserCreateView.as_view(), name='user-register'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('api/token/', AuthenticationUserObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', RefreshTokenObtainPairView.as_view(), name='token_refresh'),
   path('api/precommendations/', get_movie_recommendations, name='movie_recommendations'),
   path('api/', include(router.urls)),
   path('preferences/', PreferenceListView.as_view(), name='preference-list'),
   path('preferences/create/', PreferenceCreateView.as_view(), name='preference-create'),
   path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
   path('genres/<int:pk>/', GenreRetrieveUpdateDestroyView.as_view(), name='genre-detail'),
]