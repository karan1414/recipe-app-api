""" Serializers for recipe api """

from core.models import Ingredients, Recipe, Tag
from rest_framework import serializers


class IngredientsSerializer(serializers.ModelSerializer):
    """ Serializers for Ingredients """
    class Meta:
        model = Ingredients
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerialzer(serializers.ModelSerializer):
    """ Serailizer for TAgs """

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for recipie """
    tags = TagSerialzer(many=True, required=False)
    ingredients = IngredientsSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handling getting ot creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)        

    def _get_or_create_ingredients(self, ingredients, recipie):
        """ Handle getting or creating ingredient as needed """

        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredients.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipie.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """ Create a recipe """
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Update a recipe """
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer for a recipe """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """ upload images to recipe """

    model = Recipe

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields =['id']
        extra_kwargs = {'image': {'required': True}}