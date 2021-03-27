from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import main.models as m
from datetime import datetime
import datetime as d


class CouriersAndOrdersTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_run(self):
        self.couriers_creation()
        self.couriers_creation_not_valid()
        self.couriers_patch()
        self.couriers_patch_not_valid()
        self.orders_creation()
        self.couriers_creation_not_valid()
        self.orders_assign()
        self.orders_assign_not_valid()
        self.orders_complete()
        self.orders_complete_not_valid()
        self.couriers_get()

    def couriers_creation(self):
        url = reverse('main:couriers_post')
        data = {
            "data": [{
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 2, 3],
                "working_hours": ["08:00-22:00"]
            }]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(m.Courier.objects.count(), 1)

    def couriers_creation_not_valid(self):
        url = reverse('main:couriers_post')
        data = {
            "data": [{
                "courier_id": 99,
                "courier_type": "car",
                "regions": [1, 2],
                "working_hours": ["11:35-14:60", "09:00-11:00"]
            }]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def couriers_patch(self):
        url = reverse('main:couriers_patch_get', args=[1])
        data = {
            "courier_type": "bike",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['courier_type'], 'bike')

    def couriers_patch_not_valid(self):
        url = reverse('main:couriers_patch_get', args=[1])
        data = {
            "courier_type": "hola hola",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def orders_creation(self):
        url = reverse('main:orders_post')
        data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 1,
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": 2,
                    "weight": 0.5,
                    "region": 2,
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": 3,
                    "weight": 0.5,
                    "region": 3,
                    "delivery_hours": [
                        "09:00-12:00"
                    ]
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(m.Order.objects.count(), 3)

    def orders_creation_not_valid(self):
        url = reverse('main:orders_post')
        data = {
            "data": [
                {
                    "order_id": 50,
                    "weight": 9999,
                    "region": 12,
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": 51,
                    "weight": 14,
                    "region": 22,
                    "delivery_hours": [
                        "09:-18:90"
                    ]
                },
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def orders_assign(self):
        url = reverse('main:orders_assign')
        data = {
            "courier_id": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def orders_assign_not_valid(self):
        url = reverse('main:orders_assign')
        data = {
            "courier_id": 9999999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def orders_complete(self):
        url = reverse('main:orders_complete')
        data_50 = {
            "courier_id": 1,
            "order_id": 1,
            "complete_time": (datetime.now() + d.timedelta(minutes=5)).isoformat()
        }
        data_51 = {
            "courier_id": 1,
            "order_id": 2,
            "complete_time": (datetime.now() + d.timedelta(minutes=5)).isoformat()
        }
        data_52 = {
            "courier_id": 1,
            "order_id": 3,
            "complete_time": (datetime.now() + d.timedelta(minutes=5)).isoformat()
        }
        response = self.client.post(url, data_50, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data_51, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data_52, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def orders_complete_not_valid(self):
        url = reverse('main:orders_complete')
        data = {
            "courier_id": 330,
            "order_id": 990,
            "complete_time": "2021-03-26T21:10:59.325688"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def couriers_get(self):
        url = reverse('main:couriers_patch_get', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4.58)
        self.assertEqual(response.data['earnings'], 2500)
