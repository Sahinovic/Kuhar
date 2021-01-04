from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')
class PublicTagAPiTests(TestCase):
    """test the public available tags api"""
    def setUp(self):
        self.client = APIClient()
    def test_login_required(self):
        """test that login is required"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatTagAPITest(TestCase):
    """test the auth. user tags API"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'paspasss'
        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """test retriving tags"""
        Tag.objects.create(user=self.user, name = 'vegan')
        Tag.objects.create(user=self.user, name = 'mesar')
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags , many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags return are for authn. user"""
        user2 = get_user_model().objects.create_user(
            'mirza@mirza.com',
            'mirzaasss'
        )
        Tag.objects.create(user = user2, name = 'saha')
        tag = Tag.objects.create(user = self.user, name = 'hrana lijepa')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_succes(self):
        """test creating a new tag"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name = payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test creating new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

