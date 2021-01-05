from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import  Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL=reverse ('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """test the publicly available ing. api"""
    def setUP(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is req to login"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTests(TestCase):
    """test ing. can be retrived by aut. user"""
    def setUp(self):
        self.client = APIClient()
        self.user=get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ing_list(self):
        """test retriving list ing."""
        Ingredient.objects.create(user=self.user, name='grah')
        Ingredient.objects.create(user=self.user, name = 'so')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """test that only ingredients for the aut. user are returned"""
        user2 =get_user_model().objects.create_user(
            'mirza@mirza.com',
            'mirzamirza'
        )
        Ingredient.objects.create(user=user2, name='kupus')
        ingredient = Ingredient.objects.create(user=self.user, name='rasol')

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredients_succes(self):
        """test successeful create new ingredient """
        payload = {'name':'kupus'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name = payload['name'],
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """test create invalid ingredient"""
        payload = {'name':''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)