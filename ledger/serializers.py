from rest_framework import serializers
from .models import *


class RecordSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'date', 'amount', 'in_ex']
    
