from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from user.models import User
from .models import Record
import json

# Create your tests here.
class LedgerApiTest(APITestCase):
    client = APIClient()
    user = None

    def setUp(self):
        headers = {}
        user = User.objects.create_user("testuser@gmail.com", "usertest", "Testtest1@")
        data = {"email": "testuser@gmail.com", "password": "Testtest1@"}
        response = self.client.post(
            "/api/user/login/", json.dumps(data), content_type="application/json"
        )
        token_access = response.data["token"]["access"]
        headers = {"HTTP_Authorization": "Bearer " + token_access}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_access}")

    def test_post_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation
        가계부 등록 api 테스트
        status code, 등록된 정보 일치 확인
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }

        # When
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        result_content = json.loads(result.content.decode("utf-8"))

        # Then
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result_content["date"], data["date"])
        self.assertEqual(result_content["amount"], data["amount"])
        self.assertEqual(result_content["in_ex"], data["in_ex"])
        self.assertEqual(result_content["method"], data["method"])
        self.assertEqual(result_content["memo"], data["memo"])

    def test_get_record_list(self):
        """
        author : 전재완
        param : none
        return : none
        explanation
        가계부 기록 리스트 조회 api 테스트
        status code와 반환 데이터 타입 검사
        """
        # When
        result = self.client.get("http://127.0.0.1:8000/api/ledgers/")
        result_content = json.loads(result.content.decode("utf-8"))

        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(type(result_content), type(list()))

    def test_get_record_detail(self):
        """
        author : 전재완
        param : none
        return : none
        explanation
        가계부 상세 조회 api 테스트
        status code와 등록된 데이터 값 검사
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.get(f"http://127.0.0.1:8000/api/ledgers/{record_id}/")
        result_content = json.loads(result.content.decode("utf-8"))

        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result_content["id"], record_id)
        self.assertEqual(result_content["date"], data["date"])
        self.assertEqual(result_content["amount"], data["amount"])
        self.assertEqual(result_content["in_ex"], data["in_ex"])
        self.assertEqual(result_content["method"], data["method"])
        self.assertEqual(result_content["memo"], data["memo"])

    def test_modify_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation
        가계부 내역 수정 api
        status code와 수정된 데이터 값 검사
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.put(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )
        result_content = json.loads(result.content.decode("utf-8"))

        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result_content["id"], record_id)
        self.assertEqual(result_content["amount"], data["amount"])
        self.assertEqual(result_content["memo"], data["memo"])

    def test_delete_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation
        가계부 내역 삭제 api
        status code 검사
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.delete(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )

        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_get_deleted_record_list(self):
        """
        author : 임혁
        param : none
        return : none
        explanation
        삭제된 가계부 기록 리스트 조회 api 테스트
        status code와 반환 데이터 타입 검사
        """
        # Given
        data = {
            "date": "2022-07-07",
            "amount": 500000,
            "in_ex": "expense",
            "method": "transfer",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]
        result = self.client.delete(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )
        # When
        result = self.client.get(f"http://127.0.0.1:8000/api/bin/")
        result_content = json.loads(result.content.decode("utf-8"))
        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(type(result_content), type(list()))
    
    def test_get_deleted_record_detail(self):
        """
        author : 임혁
        param : none
        return : none
        explanation
        삭제된 가계부 기록 상세 조회 api 테스트
        status code와 삭제된 내역 데이터 검사
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 200000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.delete(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.get(f"http://127.0.0.1:8000/api/bin/{record_id}/")
        result_content = json.loads(result.content.decode("utf-8"))
        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result_content["id"], record_id)
        self.assertEqual(result_content["date"], data["date"])
        self.assertEqual(result_content["amount"], data["amount"])
        self.assertEqual(result_content["in_ex"], data["in_ex"])
        self.assertEqual(result_content["method"], data["method"])
        self.assertEqual(result_content["memo"], data["memo"])

    def test_restore_deleted_record(self):
        """
        author : 임혁
        param : none
        return : none
        explanation
        삭제된 가계부 기록 복구 api 테스트
        status code 검사
        """
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }
        result = self.client.post(
            "http://127.0.0.1:8000/api/ledgers/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]

        # When
        result = self.client.delete(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )
        record_id = json.loads(result.content.decode("utf-8"))["id"]
        result = self.client.patch(
            f"http://127.0.0.1:8000/api/bin/{record_id}/",
            json.dumps(data),
            content_type="application/json",
        )
        # Then
        self.assertEqual(result.status_code, status.HTTP_200_OK)


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
        # Given
        data = {
            "date": "2022-07-06",
            "amount": 300000,
            "in_ex": "income",
            "method": "cash",
            "memo": "This is test ledger history.",
        }

        # When
        result = self.client.post("http://127.0.0.1:8000/api/ledgers/", data=data)

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_record_list(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 기록 리스트 조회 api -> 401 반환
        """
        # When
        result = self.client.get("http://127.0.0.1:8000/api/ledgers/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_record_detail(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 상세 조회 api -> 401 반환
        """
        # Given
        user = User.objects.create_user("testuser@email.com", "nickname", "password@")
        record = Record.objects.create(
            user=user,
            date="2022-07-05",
            amount=30000,
            in_ex="expense",
            method="cash",
            memo="This is test ledger history.",
        )
        record_id = record.id

        # When
        result = self.client.get(f"http://127.0.0.1:8000/api/ledgers/{record_id}/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 수정 api -> 401 반환
        """
        # Given
        user = User.objects.create_user("testuser@email.com", "nickname", "password@")
        record = Record.objects.create(
            user=user,
            date="2022-07-05",
            amount=30000,
            in_ex="expense",
            method="cash",
            memo="This is test ledger history.",
        )
        record_id = record.id
        data = {"amount": 100000, "memo": "record modify test"}

        # When
        result = self.client.put(
            f"http://127.0.0.1:8000/api/ledgers/{record_id}/", data=data
        )

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 가계부 기록 삭제 api -> 401 반환
        """
        # Given
        user = User.objects.create_user("testuser@email.com", "nickname", "password@")
        record = Record.objects.create(
            user=user,
            date="2022-07-05",
            amount=30000,
            in_ex="expense",
            method="cash",
            memo="This is test ledger history.",
        )
        record_id = record.id

        # When
        result = self.client.delete(f"http://127.0.0.1:8000/api/ledgers/{record_id}/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_deleted_record_list(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 리스트 조회 api -> 401 반환
        """
        # When
        result = self.client.get("http://127.0.0.1:8000/api/bin/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_deleted_record_detail(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 상세 조회 api -> 401 반환
        """
        # Given
        user = User.objects.create_user("testuser@email.com", "nickname", "password@")
        record = Record.objects.create(
            user=user,
            date="2022-07-05",
            amount=30000,
            in_ex="expense",
            method="cash",
            memo="This is test ledger history.",
        )
        record.delete()
        record_id = record.id

        # When
        result = self.client.get(f"http://127.0.0.1:8000/api/bin/{record_id}/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_deleted_record(self):
        """
        author : 전재완
        param : none
        return : none
        explanation : 삭제된 가계부 기록 복구 api -> 401 반환
        """
        # Given
        user = User.objects.create_user("testuser@email.com", "nickname", "password@")
        record = Record.objects.create(
            user=user,
            date="2022-07-05",
            amount=30000,
            in_ex="expense",
            method="cash",
            memo="This is test ledger history.",
        )
        record.delete()
        record_id = record.id

        # When
        result = self.client.patch(f"http://127.0.0.1:8000/api/bin/{record_id}/")

        # Then
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
