
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """base viewset for user owndef recipe"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        """return objects for the current auth. user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """sreate new tag"""
        serializer.save(user = self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer



class IngredientViewSet(BaseRecipeAttrViewSet):
    """manage ingredient in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

