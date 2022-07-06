from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ledger.serializers import RecordSummarySerializer
from ledger.models import Record
# Create your views here.

class RecordListView(viewsets.ViewSet):
    def list(self, request):
        records = Record.objects.all()
        serializer = RecordSummarySerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)