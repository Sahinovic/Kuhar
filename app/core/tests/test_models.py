from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test create user with an email successful"""
        email = "test@test.com"
        password = "testtest"
        user = get_user_model().objects.create_user(
            email = email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email for a new user is normaized"""

        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(
            email, 'test123'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invlid_email(self):
        """test creating user with no email raises eror"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """test creating new super user"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ngredient_str(self):
        """test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name = "kukuruz"
        )
        self.assertEqual(str(ingredient), ingredient.name)