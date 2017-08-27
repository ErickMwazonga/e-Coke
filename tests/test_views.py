from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from ecoke.models import Brand

def create_user():
    User = get_user_model()
    user = User(username='john', email='john@gmail.com', is_active=True)
    user.set_password('letmein')
    user.save()
    return user

class IndexTestCase(TestCase):
    def setUp(self):
        user = create_user()

        self.client = Client()
        self.client.force_login(user)

    def test_correct_template_used(self):
        url = reverse('ecoke:index')
        res = self.client.get(url)

        self.assertTemplateUsed(res, 'ecoke/index.html')
        self.assertIn('This is a e-Coke Application where you can collect data based on brands...', res.content)


class BrandTestCase(TestCase):
    def setUp(self):
        user = create_user()

        self.client = Client()
        self.client.force_login(user)

    def test_data_posted(self):
        url = reverse('ecoke:brand_create')
        data = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Matano Mane',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        res = self.client.post(url, data=data)
        self.assertEqual(Brand.objects.count(), 1)


    def test_data_update(self):
        data = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Matano Mane',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        brand = Brand.objects.create(**data)
        url = reverse('ecoke:brand_update', kwargs={'pk':brand.pk})
        data['collector_name'] = 'Biro'
        res = self.client.post(url, data=data)

        self.assertEqual(Brand.objects.first().collector_name, 'Biro')


    def test_data_delete(self):
        data = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Matano Mane',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        brand = Brand.objects.create(**data)
        self.assertEqual(Brand.objects.count(), 1)

        url = reverse('ecoke:brand_delete', kwargs={'pk':brand.pk})
        res = self.client.post(url)

        self.assertEqual(Brand.objects.count(), 0)
