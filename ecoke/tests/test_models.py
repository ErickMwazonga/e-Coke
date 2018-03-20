# from datetime import date

from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from ecoke.models import Brand


class BrandModelTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     # Set up non-modified objects used by all test methods
    #
    #     Brand.objects.create(**data)

    def setUp(self):
        data = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Matano Mane',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        data1 = {
            'collector_name': 'Linkoln',
            'respondent_name': 'Loop',
            'respondent_city': 'Kalos',
            'favourite_drink': 'Sprite',
            'date_of_collection': (timezone.now()+timezone.timedelta(days=1)).date()
        }
        data2 = {
            'collector_name': 'Sunday',
            'respondent_name': 'May',
            'respondent_city': 'Kalos',
            'favourite_drink': 'Sprite',
            'date_of_collection': (timezone.now()+timezone.timedelta(days=3)).date()
        }
        self.brand = Brand.objects.create(**data)
        self.brand1 = Brand.objects.create(**data1)
        self.brand2 = Brand.objects.create(**data2)

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

    def test_uniqueness(self):
        data_duplicate = {
            'collector_name': 'Chepe',
            'respondent_name': 'Chitalo',
            'respondent_city': 'Kunde',
            'favourite_drink': 'Fuze',
            'date_of_collection': timezone.now().date()
        }
        with self.assertRaises(IntegrityError):
            Brand.objects.create(**data_duplicate)

    # def test_favourite_drink_choices(self):
    #     data_with_wrong_choice = {
    #         'collector_name': 'Singo',
    #         'respondent_name': 'Dila',
    #         'respondent_city': 'Matano Mane',
    #         'favourite_drink': 'Wrong choice',
    #         'date_of_collection': timezone.now().date()
    #     }
    #     with self.assertRaises(ValidationError):
    #         Brand.objects.create(**data_with_wrong_choice)

    def test_ordering(self):
        self.assertEquals(list(Brand.objects.all()), [self.brand2, self.brand1, self.brand])

    # test absolute urls
    # def test_get_absolute_url(self):
    #     self.assertEquals(self.brand.get_absolute_url(), '/brand/1')

    # test item is related to a list
    # def test_item_is_related_to_list(self):
    #     list_ = List.objects.create()
    #     item = Item()
    #     item.list = list_
    #     item.save()
    #     self.assertIn(item, list_.item_set.all())


class ProfileModelTest(TestCase):
    pass
