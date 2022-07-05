from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Record
from .serializers import LedgerDetailSerializer



# Create your views here.
class DetailAPIView(APIView):
    def get(self, request, pk):
        record=get_object_or_404(Record, id=pk)
        serializer=LedgerDetailSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

