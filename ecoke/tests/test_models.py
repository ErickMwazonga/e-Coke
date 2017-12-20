# from datetime import date

from django.test import TestCase
from django.utils import timezone

from ecoke.models import Brand


class BrandModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        data = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Matano Mane',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        Brand.objects.create(**data)

    def setUp(self):
        self.brand = Brand.objects.get(id=1)

    def test_collector_name_label(self):
        field_label = self.brand._meta.get_field('collector_name').verbose_name
        self.assertEquals(field_label, 'collector name')

    def test_collector_name_max_length(self):
        max_length = self.brand._meta.get_field('collector_name').max_length
        self.assertEquals(max_length, 255)

    def test_respondent_name_label(self):
        field_label = self.brand._meta.get_field('respondent_name').verbose_name
        self.assertEquals(field_label, 'respondent name')

    def test_respondent_name_max_length(self):
        max_length = self.brand._meta.get_field('respondent_name').max_length
        self.assertEquals(max_length, 255)

    def test_respondent_city_label(self):
        field_label = self.brand._meta.get_field('respondent_city').verbose_name
        self.assertEquals(field_label, 'respondent city')

    def tsT_respondent_city_max_length(self):
        max_length = self.brand._meta.get_field('respondent_city').max_length
        self.assertEquals(max_length, 255)

    def test_favourite_drink_label(self):
        field_label = self.brand._meta.get_field('favourite_drink').verbose_name
        self.assertEquals(field_label, 'favourite drink')

    def test_favourite_drink_name_max_length(self):
        max_length = self.brand._meta.get_field('favourite_drink').max_length
        self.assertEquals(max_length, 20)

    def test_date_of_collection_label(self):
        field_label = self.brand._meta.get_field('date_of_collection').verbose_name
        self.assertEquals(field_label, 'date of collection')

    # test default value
    def test_date_of_collection_default(self):
        todays_date = timezone.now().date()
        default = self.brand._meta.get_field('date_of_collection').default
        self.assertEquals(todays_date, default)

    def test_object_name_is_respondent_name_favourite_drink(self):
        expected_object_name = '{}-{}'.format(self.brand.respondent_name, self.brand.favourite_drink)
        self.assertEquals(expected_object_name, str(self.brand))

    # test absolute urls
    # def test_get_absolute_url(self):
    #     self.assertEquals(self.brand.get_absolute_url(), '/brand/1')
