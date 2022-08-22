import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Favorite, Ingredient, Recipe,
    RecipeIngredient, ShoppingCart, Tag
)
from .filters import IngredientFilter, RecipeFilter
from .paginations import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer,
    RecipeFullSerializer, RecipeSerializer,
    ShoppingCartSerializer, TagSerializer
)


class TagView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class IngredientView(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeFullSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeFullSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        serializer_class=FavoriteSerializer
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            user = request.user
            data = {
                'recipe': pk,
                'user': user.id
            }
            serializer = FavoriteSerializer(
                data=data,
                context={'request': request}
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            obj = Favorite.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален из списка избранного'
            }, status=status.HTTP_400_BAD_REQUEST)
        return None

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        serializer_class=ShoppingCartSerializer
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            user = request.user
            data = {
                'recipe': pk,
                'user': user.id
            }
            context = {'request': request}
            serializer = ShoppingCartSerializer(
                data=data,
                context=context
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            obj = ShoppingCart.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален из списка покупок'
            }, status=status.HTTP_400_BAD_REQUEST)
        return None

    def get_ingridients_list(self, user):
        return RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=user
        ).values(
            'ingredient__name',
        ).order_by(
            'ingredient__name'
        ).annotate(
            amount_sum=Sum('amount'),
        ).values(
            'ingredient__name', 'ingredient__measurement_unit', 'amount_sum'
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = self.get_ingridients_list(request.user)
        today = datetime.date.today()
        shopping_cart = (
            'Необходимо купить:\n\n'
            '------------------------------\n\n'
        ) + '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["amount_sum"]}'
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ]) + (
            '\n\n------------------------------\n\n'
            f'Всегда к Вашим услугам\nПродуктовый помощник {today.year}'
        )
        return HttpResponse(shopping_cart, 'Content-Type: text/plain')
