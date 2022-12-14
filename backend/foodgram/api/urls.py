from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientView, RecipeViewSet, TagView

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagView, basename='tags')
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientView, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
