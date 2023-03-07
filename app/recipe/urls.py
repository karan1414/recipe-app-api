""" Url mapping for recipe app """

from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientsViewSets)


app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]