# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from ecoke.models import Brand


class ModelTestCase(TestCase):
    '''This class defines the test suite for the Brand model.'''

    def setUp(self):
        '''Defines the test client and other test variables.'''
        self.brand = Brand(
            collector_name = 'Chepe',
            respondent_name = 'Chitalo',
            respondent_city = 'Matano Mane',
            favourite_drink = 'Fuze',
            date_of_collection = timezone.now().date()
        )

    def test_model_can_create_a_brand(self):
        '''Test the Brand model can create a brand'''
        old_count = Brand.objects.count()
        self.brand.save()
        new_count = Brand.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(APITestCase):
    '''Test suite for the api views'''

    # def setUp(self):
    #     """Define the test client and other test variables"""
    #     user = User.objects.create(username="erick")
    #
    #     # Initialize client and force it to use authentication
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=user)
    #
    #     # Since use model instance is not serializable, use Id/PK
    #     self.brand_data = {
    #         'collector_name':'Chepe',
    #         'respondent_name':'Chitalo',
    #         'respondent_city':'Matano Mane',
    #         'favourite_drink':'FZ',
    #         'date_of_collection':timezone.now().date()
    #     }
    #     self.response = self.client.post(
    #         reverse('create'),
    #         self.brand_data,
    #         format='json'
    #     )

    def setUp(self):
        '''Define the test client and other test variables'''
        self.brand_data = {
            'collector_name':'Chepe',
            'respondent_name':'Chitalo',
            'respondent_city':'Matano Mane',
            'favourite_drink':'FZ',
            'date_of_collection':timezone.now().date()
        }

        self.username = "keffa"
        self.email = 'keffa@de.com'
        self.password = 'bushbaby'

        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_brand(self):
        self.response = self.client.post(reverse('api:create'), self.brand_data, format='json')
        self.assertEqual(self.response.status_code, 201)

    def test_user_todos(self):
        """
        Test to verify user brands list
        """
        Brand.objects.create(**self.brand_data)
        response = self.client.get(reverse('api:create'))
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(Brand.objects.get().collector_name, 'Chepe')

    def test_api_authorization_is_enforced(self):
        '''Test that the api has user authorization'''
        new_client = APIClient()
        response = new_client.get('/api/brands/', format='json')
        self.assertEqual(response.status_code, 401)

    def test_api_authorized_user_can_get_a_single_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get(id=brand.id)
        response = self.client.get(
            '/api/brands/',
            kwargs={'pk': single_brand.id},
            format='json'
        )
        self.assertContains(response, 'Chitalo')
        self.assertEqual(response.status_code, 200)

    def test_api_unauthorized_user_can_get_a_single_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get(id=brand.id)
        new_client = APIClient()
        response = new_client.get(
            '/api/brands/',
            kwargs={'pk': single_brand.id},
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_api_authorized_user_can_update_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get(id=brand.id)
        change_brand_data = {
            'collector_name':'Chepe',
            'respondent_name':'Kaadzo',
            'respondent_city':'Matano Mane',
            'favourite_drink':'FZ',
            'date_of_collection':timezone.now().date()
        }
        put_response = self.client.put(
            reverse('api:details', kwargs={'pk': single_brand.id}),
            change_brand_data,
            format='json',
        )
        patch_response = self.client.patch(
            reverse('api:details', kwargs={'pk': single_brand.id}),
            change_brand_data,
            format='json',
        )
        self.assertContains(put_response, 'Kaadzo')
        self.assertContains(patch_response, 'Kaadzo')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 200)

    def test_api_unauthorized_user_can_update_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get(id=brand.id)
        change_brand_data = {
            'collector_name':'Chepe',
            'respondent_name':'Kaadzo',
            'respondent_city':'Matano Mane',
            'favourite_drink':'FZ',
            'date_of_collection':timezone.now().date()
        }
        new_client = APIClient()
        put_response = new_client.put(
            reverse('api:details', kwargs={'pk': single_brand.id}),
            change_brand_data,
            format='json',
        )
        self.assertEqual(put_response.status_code, 401)

    def test_authorized_user_api_can_delete_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get()
        response = self.client.delete(
            reverse('api:details', kwargs={'pk': single_brand.id}),
            format="json",
            follow=True
        )
        # 204 -No content
        self.assertEquals(response.status_code, 204)

    def test_unauthorized_user_api_can_delete_brand(self):
        brand = Brand.objects.create(**self.brand_data)
        single_brand = Brand.objects.get()
        new_client = APIClient()
        response = new_client.delete(
            reverse('api:details', kwargs={'pk': single_brand.id}),
            format="json",
            follow=True
        )
        self.assertEquals(response.status_code, 401)
