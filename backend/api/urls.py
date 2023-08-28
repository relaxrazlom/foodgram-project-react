from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewSet, SubscriptionsView, SubscribeView, IngredientViewSet,
    TagViewSet, FavoriteView, ShoppingCartView, ShoppingCartDownloadView
)


router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tag')


urlpatterns = [
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('users/<int:pk>/subscribe/',  SubscribeView.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
    path('recipes/download_shopping_cart/',
         ShoppingCartDownloadView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
