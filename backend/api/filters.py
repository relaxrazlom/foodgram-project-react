from django_filters import rest_framework as filters

from recipe.models import Recipe, Tag
from users.models import User


class RecipeFilter(filters.FilterSet):
    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited', method='filter_nonmodel_fields')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_nonmodel_fields')

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def filter_nonmodel_fields(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if name == 'is_in_shopping_cart' and value:
            return queryset.filter(
                shopping_cart__user=self.request.user)
        if name == 'is_favorited' and value:
            return queryset.filter(
                favorites__user=self.request.user)
        return queryset
