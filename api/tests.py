from django.test import TestCase
from rest_framework.test import (APITestCase,
                                 APIClient) 
from rest_framework import status
from datetime import date

import json

# Create your tests here.

class RecordListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_record_list(self):
        #Given
        
        #When
        result = self.client.get('http://127.0.0.1:8000/api/ledgers/')
        
        #Then   
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_post_record(self):
        #Given
        data = {
            "date": "2022-07-06",
            "amount": 30000,
            "in_ex": "expense",
            "method": "cash",
            "memo": "test"
            }
        
        #When
        result = self.client.post('http://127.0.0.1:8000/api/ledgers/', json.dumps(data), content_type='application/json')
        #Then
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    
    def test_patch_record(self):
        #Given
        data = {
            "amount":  40000,
            "memo": "test"
        }
        
        #When
        result = self.client.patch('http://127.0.0.1:8000/api/ledgers/1', data, content_type='application/json')
        result_content = json.loads(result.content.decode('utf-8'))
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
    
        
