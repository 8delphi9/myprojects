from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from ledger.serializers import (RecordSummarySerializer,
                                LedgerDetailSerializer)
from ledger.models import Record
# Create your views here.

class RecordListView(APIView):
    def get(self, request):
        records = Record.objects.all()
        serializer = RecordSummarySerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LedgerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class DetailAPIView(APIView):
    def get(self, request, pk):
        record=get_object_or_404(Record, id=pk)
        serializer=LedgerDetailSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

