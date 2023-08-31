from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime

from collections import defaultdict

from rest_framework import generics, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User, Subscribe
from recipe.models import (
    Recipe, Ingredient, Tag, Favorite, Shopping_Cart, IngredientRecipe
)
from api.pagination import RecipePagination
from api.permissions import IsAuthorActionOrAdminOrReadOnly
from api.filters import RecipeFilter, IngredientSearchFilter
from api.serializers import (
    RecipeReadSerializer, RecipeCreateSerializer,
    IngredientSerializer, TagSerializer, FavoritesSerializer,
    SubscribeSerializer, ShoppingCartSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthorActionOrAdminOrReadOnly,]
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = None
    filterset_class = IngredientSearchFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = None


class SubscriptionsView(generics.ListAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Subscribe.objects.filter(user=self.request.user)


class SubscribeView(APIView):

    def post(self, request, pk):
        subscription = get_object_or_404(User, pk=pk)
        serializer = SubscribeSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            try:
                serializer.save(user=request.user, subscription=subscription)
            except Exception:
                return Response(
                    {"errors": "Не правильная подписка"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        subscription = get_object_or_404(User, pk=pk)
        instance = Subscribe.objects.filter(
            user=request.user,
            subscription=subscription
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Отсутствует подписка"},
            status=status.HTTP_400_BAD_REQUEST
        )


class FavoriteView(APIView):

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user, favorites=recipe)
            except Exception:
                return Response(
                    {"errors": "Рецепт уже избранное"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        instance = Favorite.objects.filter(user=request.user, favorites=recipe)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Отсутствует рецепт в избранное"},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartView(APIView):

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user, favorites=recipe)
            except Exception:
                return Response(
                    {"errors": "Рецепт уже в корзине"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        instance = Shopping_Cart.objects.filter(
            user=request.user, favorites=recipe
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Отсутствует рецепт в корзине"},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartDownloadView(APIView):

    def get(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shoppingcart__user=request.user).values(
                'ingredient__name',
                'ingredient__measurement_unit',
                'amount').order_by('ingredient__name')
        data = defaultdict(int)
        today = datetime.today()

        for ingr in ingredients:
            key = (f'{ingr["ingredient__name"]} '
                   f'({ingr["ingredient__measurement_unit"]})')
            data[key] += ingr['amount']
        shopping_list = [
            f'Дата: {today:%Y-%m-%d}\n\n'
            'СПИСОК ПОКУПОК:\n'
        ]
        for key, value in data.items():
            shopping_list.append(f'- {key}: {value} \n')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format('shopping_list.txt')
        )
        return response
