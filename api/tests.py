from rest_framework.test import (APITestCase, APIClient) 
from rest_framework import status
from datetime import date

import json

# Create your tests here.

class RecordListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_record_list(self):
        result = self.client.get('http://127.0.0.1:8000/api/ledgers', content_type='application/json')
        print(result.content)
        result_content = json.loads(result.content.decode('utf-8'))
        print(result)
        
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(type(result_content), type([]))

    def test_post_record(self):
        data = {
            'date': date.today(),
            'amount': 20000,
            'in_ex': 'expense',
            'method': 'cash',
        }
        
        result = self.client.post('http://127.0.0.1:8000/api/ledgers/', data, content_type='application/json')
        
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        
        