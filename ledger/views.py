from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
)
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from ledger.serializers import (
    RecordSummarySerializer,
    LedgerDetailSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from ledger.models import Record
from ledger.ledger_api_params import record_post_params
from user.models import User
# Create your views here.

class RecordListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.get(email=request.user)
        records = Record.objects.all().filter(user=user)
        serializer = RecordSummarySerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=record_post_params)
    def post(self, request):
        serializer = LedgerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class DetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LedgerDetailSerializer

    def get(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        serializer = self.serializer_class(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        serializer = self.serializer_class(record)
        serializer.update(record, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        serializer = self.serializer_class(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeletedRecordListView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecordSummarySerializer

    def get(self, request):
        user = User.objects.get(email=request.user)
        records = Record.deleted_objects.all().filter(user=user)
        serializer = self.serializer_class(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeletedRecordDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LedgerDetailSerializer

    def get(self, request, pk):
        record = Record.deleted_objects.get(id=pk)
        serializer = self.serializer_class(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        record=Record.deleted_objects.get(id=pk)
        record.restore()
        serializer = self.serializer_class(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
