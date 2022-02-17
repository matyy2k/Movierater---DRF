from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'films', views.FilmViewSet, basename='film')
router.register(r'reviews', views.ReviewsViewSet, basename='reviews')
router.register(r'actors', views.ActorViewSet, basename='actors')

urlpatterns = [
    path('', include(router.urls)),
]