from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
)
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from ledger.serializers import (
    RecordSummarySerializer,
    LedgerDetailSerializer,
    RecordModifySerializer,
)
from drf_yasg.utils import swagger_auto_schema
from ledger.models import Record
from ledger.ledger_api_params import (
    record_post_params,
    record_modify_params,
)

from user.models import User

# Create your views here.


class RecordListView(APIView):
    """
    author : 전재완
    co-author : 임혁, 이승민
    explanation
    get : 가계부 리스트 조회 api
    post : 가계부 기록 등록 api
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        author : 전재완
        co-author : 임혁
        param :
        return : 200 response
        explanation : 가계부 요약 정보 리스트 조회
        """
        user = User.objects.get(id=request.user.id)
        if user:
            records = Record.objects.all().filter(user=user)
            serializer = RecordSummarySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=record_post_params)
    def post(self, request):
        """
        author : 전재완
        co-author : 임혁
        param : request
        return : 200 response
        explanation : request 데이터로 새로운 가계부 생성
        """
        user = User.objects.get(id=request.user.id)
        if user:
            record = Record.objects.create(user=user, **request.data)
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailAPIView(APIView):
    """
    author : 임혁
    co-author : 전재완, 이승민
    explanation
    get : path variable에 해당하는 가계부 상세 기록 조회 api
    patch : 가계부 수정 api
    delete : 가계부 기록 삭제 api
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        author : 임혁
        co-author :
        param : request, pk
        return : 200/400 response
        explanation : 입력받은 가계부 내역 id로 가계부 상세내용 조회
        """
        record = Record.objects.get(id=pk)
        if record:
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=record_modify_params)
    def put(self, request, pk):
        """
        author : 전재완
        co-author : 임혁
        param : request, pk
        return : 200/400 response
        explanation : 입력받은 amount, memo로 가계부 상세 내역 변경
        """
        record = Record.objects.get(id=pk)
        if record:
            modifier_serializer = RecordModifySerializer(record)
            modifier_serializer.update(record, request.data)
            record = Record.objects.get(id=pk)
            detail_serializer = LedgerDetailSerializer(record)
            return Response(detail_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        author :
        co-author :
        param :
        return :
        explanation :
        """
        record = Record.objects.get(id=pk)
        if record:
            record.delete()
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletedRecordListView(APIView):
    """
    author : 전재완
    co-author : 이승민
    explanation
    get : 요청한 사용자의 삭제된 가계부 기록 조회 api
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        author : 전재완
        co-author : 임혁
        param : request
        return : 200/400 response
        explanation : request 보낸 사용자의 삭제 가계부 목록 조회
        """
        user = User.objects.get(id=request.user.id)
        if user:
            records = Record.deleted_objects.all().filter(user=user)
            serializer = RecordSummarySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletedRecordDetailView(APIView):
    """
    author : 전재완
    co-author : 임혁 이승민
    explanation
    get : 삭제된 가계부 상세 정보 조회 api
    put : 삭제된 가계부 복구 api
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        author : 전재완
        co-author : 임혁
        param : request, pk
        return : 200/400 response
        explanation : requset 보낸 사용자의 삭제된 pk 가계부 상세 조회
        """
        record = Record.deleted_objects.get(id=pk)
        if record:
            user = User.objects.get(id=request.user.id)
            if record.user.id == user.id:
                serializer = LedgerDetailSerializer(record)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        author : 전재완
        co-author : 임혁
        param : request, pk
        return : 200/400 response
        explanation : 삭제된 특정 가계부 내역 복원
        """
        record = Record.deleted_objects.get(id=pk)
        if record:
            record.restore()
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)