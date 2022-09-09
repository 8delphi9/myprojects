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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            records = Record.objects.all().filter(user=user)
            serializer = RecordSummarySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=record_post_params)
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            record = Record.objects.create(user=user, **request.data)
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        record = Record.objects.get(id=pk)
        if record:
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=record_modify_params)
    def put(self, request, pk):
        record = Record.objects.get(id=pk)
        if record:
            modifier_serializer = RecordModifySerializer(record)
            modifier_serializer.update(record, request.data)
            record = Record.objects.get(id=pk)
            detail_serializer = LedgerDetailSerializer(record)
            return Response(detail_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        record = Record.objects.get(id=pk)
        if record:
            record.delete()
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletedRecordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            records = Record.deleted_objects.all().filter(user=user)
            serializer = RecordSummarySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletedRecordDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        record = Record.deleted_objects.get(id=pk)
        if record:
            user = User.objects.get(id=request.user.id)
            if record.user.id == user.id:
                serializer = LedgerDetailSerializer(record)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        record = Record.deleted_objects.get(id=pk)
        if record:
            record.restore()
            serializer = LedgerDetailSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)