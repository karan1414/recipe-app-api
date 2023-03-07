""" Views for recipe api """

from core.models import Ingredients, Recipe, Tag
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from recipe import serializers
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@extend_schema_view(
    list = extend_schema(
        parameters = [
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description="Comma seperated lists of ID to filter"
            ),
            OpenApiParameter(
                'ingredients', 
                OpenApiTypes.STR,
                description='list of comma seperated list of ingredient IDs to filter',
            )
        ]
    ) 
)


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for manage recpie apis """

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """ Convert a list of strings to integers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Retrive recipe for authenticated user """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tags_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)
        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)

        return queryset.filter(
            user=self.request.user
            ).order_by('-id').distinct()
        # return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return serializer class for request """
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """ Create a new recipe """
        serializer.save(user=self.request.user)
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters = [
                        OpenApiParameter(
                            'assigned_only',
                            OpenApiTypes.INT, enum=[0,1],
                            description="Filter by assinged to recipes"
                        )
                    ]
                )
            )
class BaseRecipeAttrViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ Base viewset for recipe ingredients and tags """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """ Retrive tags created by user """
        assigned_only = bool(
            int(
                self.request.query_params.get('assigned_only', 0)
            )
        )
        queryset = self.queryset
        if assigned_only:
            query_set = queryset.filter(recipe__isnull=False)
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()



class TagViewSet(BaseRecipeAttrViewSet):

    """ Manage tags in db """
    serializer_class = serializers.TagSerialzer
    queryset = Tag.objects.all()


class IngredientsViewSets(BaseRecipeAttrViewSet):
    """ Manage Ingredients in the db """
    serializer_class = serializers.IngredientsSerializer
    queryset = Ingredients.objects.all()


