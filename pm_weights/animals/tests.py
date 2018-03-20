from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Animal, AnimalWeight

from datetime import datetime

# Create your tests here.
class AnimalTestCase(APITestCase):
        
    @classmethod
    def setUpClass(cls):
        super(AnimalTestCase, cls).setUpClass()
        # create the class client
        client = APIClient()
        cls.client = client

    @classmethod
    def setUpTestData(cls):
        pass

    # test created data
    def test_create_animal(self):
        url = '/api/animal'

        # create an animal & verify existence
        data = {
            'id': 100,
            'external_id': 100
        }
        response = AnimalTestCase.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.filter(id=100).count(), 1)
        # attempt re-create
        response = AnimalTestCase.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Animal.objects.filter(id=100).count(), 1)

        # create an animal with a new ID & verify existence
        data = {
            'id': 99,
            'external_id': 99
        }
        response = AnimalTestCase.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.filter(id=99).count(), 1)

    def test_add_weights(self):
        url = '/api/animal'

        # create an animal & verify existence
        data = {
            'id': 100,
            'external_id': 100
        }
        response = AnimalTestCase.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.filter(id=100).count(), 1)
    
        # add weight & verify existence
        url = '/api/animal/100/weight'
        data = {
            'weight': 450,
            'weigh_date': datetime.now()
        }
        response = AnimalTestCase.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.get(id=100).animalweight_set.count(), 1)