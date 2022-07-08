from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from user.models import User
from .models import Record
# Create your tests here.


class WithoutLoginLedgerApiTest(TestCase):
    """
    author : 전재완
    explanation : 로그인 하지 않은 상태로 가계부 api 호출하는 testcases
    """
    def setUp(self):
        client = APIClient()
        
    def test_post_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 등록 api 테스트 -> 401 반환
        """
        #Given
        data = {
            "user": 1,
            "date": "2022-07-06",
            "amount": 300000,
            "in_ix": "income",
            "method": "cash",
            "memo": "this  is test"
        }
        
        #When
        result = self.client.post('http://127.0.0.1:8000/api/ledgers/', data=data)
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
            
    def test_get_record_list(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 기록 리스트 조회 api -> 401 반환
        """
        #When
        result = self.client.get('http://127.0.0.1:8000/api/ledgers/')
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_record_detail(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 상세 조회 api -> 401 반환
        """
        #Given
        user = User.objects.create_user('testuser@email.com', 'nickname', 'password@')
        record = Record.objects.create(user=user, date='2022-07-05', amount=30000, in_ex='expense', method='cash', memo='test')
        record_id = record.id
        
        #When
        result = self.client.get(f"http://127.0.0.1:8000/api/ledgers/{record_id}/")
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_modify_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 수정 api -> 401 반환
        """
        #Given
        user = User.objects.create_user('testuser@email.com', 'nickname', 'password@')
        record = Record.objects.create(user=user, date='2022-07-05', amount=30000, in_ex='expense', method='cash', memo='test')
        record_id = record.id
        data = {
            "amount":100000,
            "memo": "record modify test"
        }
        
        #When
        result = self.client.patch(f"http://127.0.0.1:8000/api/ledgers/{record_id}/", data=data)
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 기록 삭제 api -> 401 반환
        """
        #Given
        user = User.objects.create_user('testuser@email.com', 'nickname', 'password@')
        record = Record.objects.create(user=user, date='2022-07-05', amount=30000, in_ex='expense', method='cash', memo='test')
        record_id = record.id

        #When
        result = self.client.delete(f"http://127.0.0.1:8000/api/ledgers/{record_id}/")
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_deleted_record_list(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 리스트 조회 api -> 401 반환
        """
        #When
        result = self.client.get('http://127.0.0.1:8000/api/bin/')
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_deleted_record_detail(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 상세 조회 api -> 401 반환
        """
        #Given
        user = User.objects.create_user('testuser@email.com', 'nickname', 'password@')
        record = Record.objects.create(user=user, date='2022-07-05', amount=30000, in_ex='expense', method='cash', memo='test')
        record.delete()
        record_id = record.id
        
        #When
        result = self.client.get(f"http://127.0.0.1:8000/api/bin/{record_id}/")
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_restore_deleted_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 복구 api -> 401 반환
        """
        #Given
        user = User.objects.create_user('testuser@email.com', 'nickname', 'password@')
        record = Record.objects.create(user=user, date='2022-07-05', amount=30000, in_ex='expense', method='cash', memo='test')
        record.delete()
        record_id = record.id
        
        #When
        result = self.client.put(f"http://127.0.0.1:8000/api/bin/{record_id}/")
        
        #Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)